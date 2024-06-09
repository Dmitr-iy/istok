from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view, OpenApiParameter, OpenApiResponse
from rest_framework import generics, viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login

from .serializers import UserSerializer, UserProfileSerializer, RenovationLocationSerializer


def index(request):
    user_form = UserLoginForm()
    return render(request, 'index.html', {'user_form': user_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
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


@extend_schema(tags=["profile"])
@extend_schema_view(
    create=extend_schema(
        summary="Создать нового пользователя",
        examples=[
            OpenApiExample(
                "Post example",
                description="Тестовый пример для метода post",
                value={
                    "user": {
                        "username": "login",
                        "password": "password"
                    },
                    "phone_number": "+71111111111",
                    "first_name": "Ivan",
                    "consent_to_data_processing": 'true',
                    "email": "user@example.com"
                },
                status_codes=[str(status.HTTP_200_OK)],
            ),
        ]
    ),
    list=extend_schema(
            summary="Получить список пользователей",
    ),
    retrieve=extend_schema(
        summary="Получить пользователя",
    ),
    update=extend_schema(
        summary="Обновить пользователя",
    ),
    partial_update=extend_schema(
        summary="Частичное обновление пользователя",
    ),
    destroy=extend_schema(
        summary="Удалить пользователя",
    ),
)
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone_number', 'email']

    @extend_schema(
        summary="Получить пользователя по номеру телефона",
    )
    @action(methods=['get'], detail=False, url_path='by-phone-number/(?P<phone_number>\+7[0-9]+)')
    def get_by_phone_number(self, request, phone_number):
        try:
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Пользователь с таким номером телефона не найден'}, status=404)

@extend_schema(tags=["renovation"])
class RenovationLocationViewSet(viewsets.ModelViewSet):
    queryset = RenovationLocation.objects.all()
    serializer_class = RenovationLocationSerializer
