from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_username/', views.check_username, name='check_username')
]