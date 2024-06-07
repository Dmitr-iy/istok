from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', unique=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    consent_to_data_processing = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')
    
    # Второстепенные поля для нашей лояльности пока их не трогаем 
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', null=True, blank=True)
    surname = models.CharField(max_length=100, verbose_name='Отчество', null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    email = models.EmailField(verbose_name='Почта', null=True, blank=True, unique=True)
    has_children = models.CharField(max_length=3, choices=[('yes', 'Да'), ('no', 'Нет')], verbose_name='Наличие детей', default='no')
    renovation_plan = models.CharField(max_length=100, verbose_name='Планируется ли ремонт?', choices=[
        ('already_ongoing', 'Уже идет'),
        ('starting_soon', 'Скоро приступаем'),
        ('within_half_year', 'В течение полугода'),
        ('within_year', 'В течение года'),
    ], null=True, blank=True)
    renovation_location = models.ManyToManyField('RenovationLocation', verbose_name='Где планируется ремонт?', blank=True)
    subscription_consent = models.BooleanField(default=False, verbose_name='Согласие на рассылку')

class RenovationLocation(models.Model):
    name = models.CharField(max_length=50, verbose_name='Место ремонта')

    def __str__(self):
        return self.name

