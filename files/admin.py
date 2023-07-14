from django.contrib import admin
from files.models import File
import os


class FileAdmin(admin.ModelAdmin):
    list_display = ('get_pretty_str','order', 'file_type', 'file')
    list_filter = ['order', 'file_type']
    search_fields = ['pk', 'file']

    def get_pretty_str(self, obj):
        return f'({obj.id}) {os.path.basename(obj.file.name)}'
        
    get_pretty_str.short_description  = "Файл"

admin.site.register(File, FileAdmin)

