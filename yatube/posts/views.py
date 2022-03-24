from django.shortcuts import render, get_object_or_404
from .models import Post, Group

COUNT_POSTS = 10


def index(request):
    main_page = True
    posts = Post.objects.order_by('-pub_date')[:COUNT_POSTS]
    context = {
        'main_page': main_page,
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all().order_by('-pub_date')[:COUNT_POSTS]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)
