from django.contrib import admin
from production_settings.models import ProductionSettings

class ProductionSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'value')

admin.site.register(ProductionSettings, ProductionSettingsAdmin)
