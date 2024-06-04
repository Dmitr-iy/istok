from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm


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
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Эта электронная почта уже используется')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number.startswith('+7'):
            phone_number = phone_number[1:]
        if not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        if len(phone_number) != 11:
            raise forms.ValidationError("Номер телефона должен состоять из 11 цифр")
        if phone_number.startswith('8') or phone_number.startswith('7'):
            phone_number = '+7' + phone_number[1:]
        else:
            raise forms.ValidationError("Номер телефона должен начинаться с 8, 7 или +7")
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Этот номер телефона уже используется")
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
            'renovation_location', 'subscription_consent'
        ]
        widgets = {
            'renovation_location': forms.CheckboxSelectMultiple
        }

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label="Email или телефон")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
