from django.contrib import admin
from support.models import SupportRequest

class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('phone', 'user', 'email', 'priority_rate', 'datetime')
    list_filter = ('phone', 'email', 'priority_rate', 'datetime')
    search_fields = ('phone', 'user', 'email', 'datetime')

admin.site.register(SupportRequest, SupportRequestAdmin)
