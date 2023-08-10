from django.contrib import admin
from .models import Profile

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('phone', 'get_first_name', 'get_last_name', 'get_email', 'user', 'phone_is_confirmed', 'amount_of_converts')
    list_filter = ('phone_is_confirmed', 'amount_of_converts')
    search_fields = ('phone', 'get_first_name', 'get_email', 'get_last_name', 'user', 'phone_is_confirmed', 'amount_of_converts')

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

