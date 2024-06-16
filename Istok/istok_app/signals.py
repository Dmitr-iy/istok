import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
bx24_token = 'your_bitrix24_token'
bx24_domain = 'your_bitrix24_domain'


@receiver(post_save, sender=UserProfile)
def send_user_data_to_bitrix24(sender, instance, created, **kwargs):
    if created:
        lead_data = {
            'fields': {
                'TITLE': instance.first_name,
                'NAME': instance.first_name,
                'PHONE': [{'VALUE': instance.phone_number, 'VALUE_TYPE': 'WORK'}],
                'EMAIL': [{'VALUE': instance.user.email, 'VALUE_TYPE': 'WORK'}],
            }
        }
        try:
            response = requests.post(
                f'{settings.BITRIX_WEBHOOK_URL}/crm.lead.add.json',
                json=lead_data
            )
            response.raise_for_status()
            print(f"Lead created successfully: {lead_data}")
        except requests.exceptions.RequestException as e:
            print(f"Error creating lead: {e}")
