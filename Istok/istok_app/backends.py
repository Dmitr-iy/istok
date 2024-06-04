from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                if username.startswith('8') or username.startswith('7'):
                    username = '+7' + username[1:]
                    user = User.objects.get(profile__phone_number=username)
                elif username.startswith('+7'):
                    username = username
                    user = User.objects.get(profile__phone_number=username)
                else:
                    raise forms.ValidationError('Invalid username')
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
