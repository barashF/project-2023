from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    
    def clean_password2(self):
        cd = self.cleaned_data
        error_password = ''
        if cd['password1'] != cd['password2']:
            error_password = 'Пароли не совпадают'
        return error_password
    def clean_username(self):
        email = self.cleaned_data
        if User.objects.filter(email=email.get('email')).exists():
            email.add_error ('email', "Эта почта уже зарегестрированна")
        return email
        
class RegistrForm(UserCreationForm):
  # Добавляем новое поле Email
  email = forms.EmailField(max_length=254, help_text='This field is required')
  
  # Создаём класс Meta
  class Meta:
    # Свойство модели User
    model = User
    # Свойство назначения полей
    fields = ('username', 'email', 'password1', 'password2',)

    def clean(self):
        cleaned_data = super().clean(self)
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError('email', "Эта почта уже зарегестрированна")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfiledataForm(ModelForm):

    class Meta:
        model = Profile

        fields = ('email', 'def_address')
