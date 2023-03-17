from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, RegistrForm, LoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

def register(request):
    data = {}
    users = User.objects.all()
    emails = []
    for i in users:
        emails.append(i.email)
    if request.method == 'POST':
        form = RegistrForm(request.POST)
        
        if form.is_valid() and form.cleaned_data.get("email") not in emails:  
            form.save()
            data['form'] = form
            data['res'] = "Всё прошло успешно"
            return redirect("market")
        else:
            data['form'] = form
            password_error = ''
            if form.password2.errors != '':
                password_error = form.password2.errors
            return render(request, 'signup_test.html', data, {'password_error':password_error})
    else: 
        form = RegistrForm()
        data['form'] = form
        return render(request, 'signup_test.html', data)

def check_email(request):
    users = User.objects.all()
    emails = []

    for i in users:
        emails.append(i.email)
    return JsonResponse({'emails':emails})

def check_username(request):
    users = User.objects.all()
    usernames = []

    for i in users:
        usernames.append(i.username)
    return JsonResponse({'usernames':usernames})

def user_login(request):
    data = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email_check = User.objects.filter(email=cd['email']).count()
            if email_check != 0:
                username = User.objects.get(email=cd['email'])
                user = authenticate(username=username.username, password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect("market")
                    else:
                        return HttpResponse('Disabled account')
                    
                else:
                    data['error_pass'] = 'пороль неверный'
                    data['form'] = form
                    return render(request, 'login.html', data)

            else:
                data['error_email'] = 'почта не зарегистрирована'
                data['form'] = form
                return render(request, 'login.html', data)
            
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})