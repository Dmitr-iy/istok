from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import  *
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login


def index(request):
    user_form = UserLoginForm()
    return render(request, 'index.html', {'user_form': user_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # login(request, user) 
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'user_form': user_form})


def login(request):
    if request.method == 'POST':
        user_form = UserLoginForm(request, data=request.POST)
        if user_form.is_valid():
            user = user_form.get_user()
            auth_login(request, user)
            return HttpResponseRedirect('/') 
        else:
            return JsonResponse({'errors': user_form.errors}, status=400)
    else:
        user_form = UserLoginForm()
    return render(request, 'auth/login.html', {'user_form': user_form})
