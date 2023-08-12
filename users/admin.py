from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('phone', 'get_first_name', 'get_last_name', 'get_email', 'user', 'phone_is_confirmed', 'amount_of_converts')
    list_filter = ('phone_is_confirmed', 'amount_of_converts')
    search_fields = ('phone', 'get_first_name', 'get_email', 'get_last_name', 'user', 'phone_is_confirmed', 'amount_of_converts')
    # actions = ['delete_model']
    def delete_queryset(self, request, queryset):
        """ Вызывается при удалении в админке - выбор нескольких - удалить выбранные """
        print("Deleting queryset!")
        for m in queryset:
            saved_user = m.user
            m.user = None
            saved_user.delete()
        queryset.delete()

    def delete_model(self, request, object):
        """ Вызывается при удалении в админке - переход на страницу объекта - удалить """
        print("Deleting one model!")
        saved_user = object.first().user # first() because of "object" is also queryset, but contain only one element
        object.user = None
        saved_user.delete()
        object.delete()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 

