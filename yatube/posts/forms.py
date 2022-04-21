from django import forms
from django.forms import Textarea
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        labels = {'text': 'Текст поста', 'group': 'Группа'}
        fields = ('text', 'group')
        help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        widgets = {
            'text': Textarea(attrs={'cols': 40, 'rows': 10}),
        }
