from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import  *
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required


def index(request):
    user_form = UserLoginForm()
    return render(request, 'index.html', {'user_form': user_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return JsonResponse({'success': True})
        else:
            errors = user_form.errors.as_json()
            return JsonResponse({'success': False, 'errors': user_form.errors})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'user_form': user_form})


def login(request):
    if request.method == 'POST':
        user_form = UserLoginForm(request, data=request.POST)
        if user_form.is_valid():
            user = user_form.get_user()
            auth_login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/'})
        else:
            # Извлечение не полевых ошибок
            errors = user_form.errors.get('__all__', user_form.errors)
            return JsonResponse({'success': False, 'errors': errors})
    else:
        user_form = UserLoginForm()
    return render(request, 'auth/login.html', {'user_form': user_form})


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('user_profile', username=request.user.username)
    
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, instance=user.profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('user_profile', username=user.username)
    else:
        user_profile_form = UserProfileForm(instance=user.profile)
    
    return render(request, 'profile/profile.html', {'user_profile_form': user_profile_form, 'user': user})

@login_required
def order_history(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('user_profile', username=request.user.username)
    orders = Order.objects.filter(user=user) 
    return render(request, 'profile/order_history.html', {'orders': orders})

@login_required
def favorites(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('user_profile', username=request.user.username)
    favorites = Favorite.objects.filter(user=user)  
    return render(request, 'profile/favorites.html', {'favorites': favorites})

@login_required
def bonus_program(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('user_profile', username=request.user.username)
    bonus_info = BonusProgram.objects.filter(user=user)  
    return render(request, 'profile/bonus_program.html', {'bonus_info': bonus_info})



