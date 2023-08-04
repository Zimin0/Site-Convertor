from django.apps import AppConfig

class ProductionSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'production_settings'
    verbose_name = 'Настройки сайта'
