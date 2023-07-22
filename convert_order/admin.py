from django.contrib import admin
from convert_order.models import ConvertOrder
from files.models import File

class FileAdminStacked(admin.StackedInline):
    model = File

class ConvertOrderAdmin(admin.ModelAdmin):
    class Meta:
        model = ConvertOrder
    list_display = ('get_pretty_str', 'user', 'slug', 'current_status', 'need_to_pay', 'paid', 'creation_date')
    list_filter = [ 'user', 'creation_date', 'current_status', 'need_to_pay', 'paid']
    ordering = ['-creation_date',]
    search_fields = ['pk', 'user', 'creation_date']
    inlines = [FileAdminStacked]

    def get_pretty_str(self, obj):
        return f'Конвертация №{obj.id}'

    get_pretty_str.short_description  = "Название"

admin.site.register(ConvertOrder, ConvertOrderAdmin)


