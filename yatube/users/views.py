from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, RegistrForm
from django.contrib.auth.models import User
from django.http import JsonResponse

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