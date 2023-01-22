from dataclasses import field
from django.forms import ModelForm, TextInput, Textarea, ImageField
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("title", "description", "text", "image")

        
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название поста'
            }),
            "description": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            "text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст поста'
            })
        }
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите комментарий...'
            })
        }