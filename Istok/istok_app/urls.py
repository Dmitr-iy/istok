from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', index, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('profile/<str:username>/order_history/', order_history, name='order_history'),
    path('profile/<str:username>/favorites/', favorites, name='favorites'),
    path('profile/<str:username>/bonus_program/', bonus_program, name='bonus_program'),
]