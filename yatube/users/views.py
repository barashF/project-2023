from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, RegistrForm, LoginForm, ProfiledataForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from .models import Profile, Code
from .sender import sender_mail
import random

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
            Profile.objects.create(user=User.objects.get(email=form.cleaned_data.get("email")), email=form.cleaned_data.get("email"))
            Code.objects.create(user=User.objects.get(email=form.cleaned_data.get("email")), code='')
            data['form'] = form
            data['res'] = "Всё прошло успешно"
            return redirect("market")
        else:
            password_error = ''
            if len(form.cleaned_data["password1"]) < 8:
                password_error = 'пароль слишком короткий'
            elif (any(c.isupper() for c in form.cleaned_data["password1"]) and any(c.islower() for c in form.cleaned_data["password1"])) == False or any(char.isdigit() for char in form.cleaned_data["password1"]) == False:
                password_error = 'пароль ненадёжный'
            elif form.cleaned_data["password1"] != form.cleaned_data["password2"]:
                password_error = 'пароли не совпадают'
                
            return render(request, 'signup_test.html', {'form':form, 'password_error':password_error})
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
                    data['error_pass'] = 'пароль неверный'
                    data['form'] = form
                    return render(request, 'login.html', data)

            else:
                data['error_email'] = 'почта не зарегистрирована'
                data['form'] = form
                return render(request, 'login.html', data)
            
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def clean_email(form, check):
        inemail = form.cleaned_data.get('email')

        existing_users = Profile.objects.filter(email=inemail)
        if existing_users.exists() and existing_users[0].id != form.instance.id:

            check = False
            return check
        
        check = True

        return check
        
def profile_edit(request):
    prof_data = get_object_or_404(Profile, user=request.user)
    form = ProfiledataForm(request.POST or None, files=request.FILES or None, instance=prof_data)
    if request.method == 'POST':
        check = False
        if form.is_valid() and clean_email(form, check) == True:
            form.save()
            user = request.user
            user.email = Profile.objects.get(user=request.user).email
            user.save()
            form.email_confirmation = False
            form.save()

            end = 'сохранено'
            conf_mail = form.email_confirmation
            return render(request, 'profile_data.html', {'form':form, 'end':end, 'conf_mail':conf_mail})
            
        else:
            error_email = ''
            if clean_email(form, check) == False:
                error_email = 'данная почта уже зарегистрирована'
            else:
                error_email = 'ошибка заполнения'
            return render(request, 'profile_data.html', {'form':form, 'error_email':error_email})

    else:
        prof = Profile.objects.get(user=request.user).email_confirmation
        return render(request, 'profile_data.html', {'form':form, 'conf_mail':prof})

def new_code(request):
    code = ''
    new_code = Code.objects.get(user=request.user)

    for i in range(6):
        code += str(random.randint(0, 9))
    
    setattr(new_code, 'code', code)
    new_code.save()

def sender_code(request):
    new_code(request)
    code = Code.objects.get(user=request.user).code
    sender_mail(request.user.email, "Подтверждение почты", "Код подтверждения: " + code)

def mail_confirmation(request):
    if request.method == 'POST':
        code = Code.objects.get(user=request.user).code

        if request.POST.get('code') == code:

            profile = Profile.objects.get(user=request.user)
            setattr(profile, 'email_confirmation', True)
            profile.save()

            return redirect('profile_edit')
        
        else:
            error = 'неверный код'
            return render(request, 'email_code.html', {'error':error})
        
    else:
        sender_code(request)
        return render(request, 'email_code.html')
