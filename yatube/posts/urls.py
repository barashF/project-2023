from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name="news"),
    path('new/', views.new_post, name="new_post"),
    path('<str:username>/follow/', views.profile_follow, name="profile_follow"),
    path('<str:username>/unfollow/', views.profile_unfollow, name="profile_unfollow"),
    path('<str:username>/<int:post_id>/', views.post, name="post"),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name="post_edit"),
    path('<str:username>/<int:post_id>/comment', views.add_comment, name="add_comment")
]