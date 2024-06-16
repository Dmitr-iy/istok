from django.apps import AppConfig


class IstokAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'istok_app'

    def ready(self):
        import istok_app.signals
