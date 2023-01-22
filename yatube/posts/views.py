from calendar import c
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Follow
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


def news(request):
    latest = Post.objects.order_by("-pub_date").all()
    return render(request, 'news.html', {'posts': latest})

@login_required
def new_post(request):
    error = ''
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if request.method == "POST" and form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('news')
        else:
            error = 'Некоректный ввод'


    form = PostForm

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'new_post.html', data)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    latest = Post.objects.filter(author_id=profile).order_by("-pub_date").all()
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = False
    follow_check = Follow.objects.filter(user=user.id, author=author.id).count()
    followers = Follow.objects.filter(author=author.id).count()
    if follow_check == 0 and author.id != user.id:
        follow = False
    else:
        follow = True
    user_posts = len(latest)
    context = {
        'profile': profile,
        'posts': latest,
        'user_posts': user_posts,
        'follow': follow,
        'followers': followers
    }
    return render(request, 'profile.html', context)

def post(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).order_by("-created").all()
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect("post", username=request.user.username, post_id=post_id)
    latest = Post.objects.get(pk=post.pk)
    context = {
        'profile': profile,
        'post': latest,
        'form':form,
        'comments':comments
    }
    return render(request, 'post.html', context)

@login_required
def post_edit(request, username, post_id):
    error = ''
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    if request.user != user:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        post.pub_date = datetime.datetime.now()
        post.save()
        return redirect('news')
    else:
        error = 'Некоректный ввод'
    return render(request, "post_edit.html", {"form": form, "post": post, "error": error})
    
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect("post", username=request.user.username, post_id=post_id)
    return render(request, 'comments.html', {"form":form})


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow_check = Follow.objects.filter(user=user.id, author=author.id).count()
    if follow_check == 0 and author.id != user.id:
        Follow.objects.create(user=request.user, author=author)
    return redirect("profile", username=username)

@login_required
def profile_unfollow(request, username):
    user = request.user.id
    author = get_object_or_404(User, username=username)
    follow_check = Follow.objects.filter(user=user, author=author.id).count()
    if follow_check == 1:
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("profile", username=username)