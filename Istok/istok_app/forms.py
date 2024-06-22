from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError



class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=25, label="Ваше имя")
    email = forms.EmailField(required=True, label="Электронная почта")
    phone_number = forms.CharField(max_length=15, required=True, label="Номер телефона")
    consent_to_data_processing = forms.BooleanField(required=True, label="Согласие на обработку персональных данных")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'phone_number', 'consent_to_data_processing', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Данный email уже зарегистрирован")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Данный номер телефона уже зарегистрирован")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserProfile.objects.create(
                first_name=self.cleaned_data['first_name'],
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email'],
                consent_to_data_processing=self.cleaned_data['consent_to_data_processing']
            )
        return user
    
#Не трогать это поля для лояльности 
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'first_name', 'consent_to_data_processing',
            'last_name', 'surname', 'date_of_birth', 'email',
            'has_children', 'renovation_plan',
            'renovation_location', 'subscription_consent',
            'gender','ren_planned',

        ]
        widgets = {
            'renovation_location': forms.CheckboxSelectMultiple,
            'ren_planned': forms.RadioSelect(attrs={'class' :'form-check-input'}),
            'gender': forms.RadioSelect(attrs={'class' :'form-check-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'has_children': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'renovation_plan': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'subscription_consent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'consent_to_data_processing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label="Email или телефон")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)