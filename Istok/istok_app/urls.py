from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'renovation-location', views.RenovationLocationViewSet, basename='renovation')

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', index, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include(router.urls)),

    path("chat/<str:room_name>/", views.room, name="room"),
]
