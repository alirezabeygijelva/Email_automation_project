from django.apps import AppConfig


class EmailautomationbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EmailAutomationBot'

    def ready(self):
        from . import signals
