from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', index, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]