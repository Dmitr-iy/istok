from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view
from rest_framework import serializers, status
from django.contrib.auth.models import User

from .models import UserProfile, RenovationLocation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['has_children', 'renovation_plan', 'renovation_location', 'subscription_consent',
                            'last_name', 'surname', 'date_of_birth']

    def validate_phone_number(self, value):
        if value.startswith('+7'):
            value = value[1:]
        if not value.isdigit():
            raise serializers.ValidationError('Номер телефона должен состоять только из цифр')
        if len(value) != 11:
            raise serializers.ValidationError("Номер телефона должен состоять из 11 цифр")
        if value.startswith('7') or value.startswith('8'):
            value = '+7' + value[1:]
        else:
            raise serializers.ValidationError("Номер телефона должен начинаться с +7, 7 или 8")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RenovationLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenovationLocation
        fields = '__all__'
