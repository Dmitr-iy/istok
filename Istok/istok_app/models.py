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

class Catalog(models.Model):
    CATEGORY_CHOICES = (
        ('Кухня', 'Кухня'),
        ('Гардероб', 'Гардероб'),
        ('Прихожая', 'Прихожая'),
        ('Комод', 'Комод'),
        ('Стеллаж', 'Стеллаж')
    )
    PURPOSE_CHOICES = (
        ('Домой', 'Домой'),
        ('Офис', 'Офис'),
        ('Детская', 'детская'),
    )
    SHAPE_CHOICES = (
        ('Прямой(ая)', 'Прямой(ая)'),
        ('Угловой(ая)', 'Угловой(ая)'),
        ('П-образный(ая)', 'П-образный(ая)'),
        ('Г-образный(ая)', 'Г-образный(ая)'),
        ('Скрытый(ая)', 'Скрытый(ая)'),
    )
    KITCHEN_CHOICES = (
        ('С барной стойкой', 'С барной стойкой'),
        ('С островом', 'С островом'),
    )
    FASADE_MATERIAL = (
        ('ЛДСП', 'ЛДСП'),
        ('Пленка ПВХ', 'Пленка ПВХ'),
        ('Пластик AGT', 'Пластик AGT'),
        ('Пластик Fenix', 'Пластик Fenix'),
        ('Эмаль', 'Эмаль'),
    )
    TABLE_TOP_MATERIAL = (
        ('Столешница ДСП с покрытием HPL', 'Столешница ДСП с покрытием HPL'),
        ('Столешница компакт-ламинат', 'Столешница компакт-ламинат'),
        ('Кварцевые столешницы', 'Кварцевые столешницы'),
        ('Акриловые столешницы', 'Акриловые столешницы'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True)
    shape = models.CharField(max_length=100, choices=SHAPE_CHOICES, null=True, blank=True)
    kitchen = models.CharField(max_length=100, choices=KITCHEN_CHOICES, null=True, blank=True)
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES)
    facade_material = models.CharField(max_length=100, choices=FASADE_MATERIAL, null=True, blank=True)
    Table_top_material = models.CharField(max_length=100, choices=TABLE_TOP_MATERIAL, null=True, blank=True)
    image = models.ImageField()

    # для 3D модели
    # model_file = models.FileField(upload_to='models/')

    def __str__(self):
        return self.name
