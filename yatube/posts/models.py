from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    title = models.CharField("Заголовок", max_length=150)
    description = models.CharField("Описание публикации", max_length=400)
    text = models.TextField("Текст поста")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_comments")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")