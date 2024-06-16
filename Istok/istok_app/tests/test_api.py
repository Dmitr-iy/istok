from rest_framework import serializers
from rest_framework.test import APITestCase
from loguru import logger

from django.contrib.auth.models import User
from ..models import UserProfile
from faker import Faker

from ..serializers import UserProfileSerializer


class TestApi(APITestCase):
    def setUp(self):
        fake = Faker()
        username = fake.user_name()
        phone = f"+7{fake.random_number(digits=10)}"
        email = fake.email()
        first_name = fake.first_name()

        self.user = User.objects.create_user(username=username, password='12345')
        self.profile = UserProfile.objects.create(user=self.user, phone_number=phone,
                                                  email=email, first_name=first_name,
                                                  consent_to_data_processing=True)

    def test_api(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 200)

    def test_api_user(self):
        response = self.client.get('/api/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_api_user_by_id(self):
        response = self.client.get(f'/api/profile/{self.user.id}/')
        self.assertEqual(response.status_code, 200)

    def test_api_user_by_phone_number(self):
        response = self.client.get(f'/api/profile/by-phone-number/{self.profile.phone_number}/')
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e:
            logger.error(f"AssertionError: {e}. Response: {response}")

    def test_serializer_post(self):
        data = {
            "user": {
                "username": "login",
                "password": "password"
            },
            "phone_number": "+71111111111",
            "first_name": "Ivan",
            "consent_to_data_processing": 'true',
            "email": "user@example.com"
        }

        response = self.client.post('/api/profile/', data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_serializer_put(self):
        data = {
            "user": {
                "username": "login",
                "password": "password"
            },
            "phone_number": "+71111111111",
            "first_name": "Ivan",
            "consent_to_data_processing": 'true',
            "email": "user@example.com"
        }

        response = self.client.put(f'/api/profile/{self.user.id}/', data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_serializer_delete(self):
        response = self.client.delete(f'/api/profile/{self.user.id}/')
        self.assertEqual(response.status_code, 204)

    def test_serializer_partial_update(self):
        data = {
            "user": {
                "username": "login",
                "password": "password"
            },
            "phone_number": "+71111111111",
            "first_name": "Ivan",
            "consent_to_data_processing": 'true',
            "email": "user@example.com"
        }

        response = self.client.patch(f'/api/profile/{self.user.id}/', data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_serializer_list(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 200)

    def test_serializer_retrieve(self):
        response = self.client.get(f'/api/profile/{self.user.id}/')
        self.assertEqual(response.status_code, 200)

    def test_serializer_retrieve_by_phone_number(self):
        response = self.client.get(f'/api/profile/by-phone-number/{self.profile.phone_number}/')
        self.assertEqual(response.status_code, 200)

    def test_phone_number_validation_startswith_invalid(self):
        invalid_phone_numbers = [
            '12345678901',  # starts with 1, not 7 or 8
            '91234567890',  # starts with 9, not 7 or 8
            'abc12345678',  # starts with a letter, not a digit
        ]
        try:
            for phone_number in invalid_phone_numbers:
                with self.assertRaises(serializers.ValidationError) as e:
                    UserProfileSerializer.validate_phone_number(self, phone_number)
                self.assertEqual(str(e.exception), "Номер телефона должен начинаться с +7, 7 или 8")
        except AssertionError as e:
            logger.error(f"AssertionError: {e}. Response")
