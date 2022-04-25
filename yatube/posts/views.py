from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User
from .forms import PostForm
from .utils import paginate_page


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    page_obj = paginate_page(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().order_by('-pub_date')
    page_obj = paginate_page(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = User.objects.get(username=username)
    post_list = Post.objects.filter(author=user)
    count_posts = user.posts.count()
    page_obj = paginate_page(request, post_list)
    context = {
        'user': user,
        'page_obj': page_obj,
        'count_posts': count_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.select_related('author', 'group').get(pk=post_id)
    post_list = Post.objects.filter(author=post.author)
    count_posts = post_list.count()
    context = {
        'post': post,
        'count_posts': count_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    is_edit = True
    post_url = f'posts/{post_id}/edit'
    if post.author != request.user:
        return redirect('posts:detail', post_id=post.id)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save()
            return redirect('posts:post_detail', post_id=post.id)
    return render(request, 'posts/create_post.html', {'form': form,
                                                      'is_edit': is_edit,
                                                      'post_url': post_url,
                                                      })
