from django.urls import path
from django.contrib.auth import views as authViews


from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('profile_edit/mail_confirmation/', views.mail_confirmation, name='mail_confirmation'),
    path('login/', views.user_login, name='login'),
    path('logout/', authViews.LogoutView.as_view(next_page="market"), name='logout'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_username/', views.check_username, name='check_username')
]