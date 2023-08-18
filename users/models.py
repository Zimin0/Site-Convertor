from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, pre_delete 
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.contrib import admin

from production_settings.models import ProductionSettings

def get_convertation_amount():
    amount_settings = get_object_or_404(ProductionSettings, slug='CONVERT_AMOUNT')
    return int(amount_settings.value)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True, unique=True, help_text='Номер телефона в формате +79112345678')
    phone_is_confirmed = models.BooleanField(verbose_name="Телефон подтвержден", default=False)
    amount_of_converts = models.IntegerField(verbose_name="Кол-во конвертаций", default=get_convertation_amount, validators=[MinValueValidator(0)])
    
    def __str__(self): # Надо поменять 
        return f'Профиль пользователя {self.user}' 
    
    def delete(self, *args, **kwargs):
        """ При удалении профиля - удаляет самого юзерв. Вызывается только в коде. """
        print("Удален Profile. Удаляю юзера.")
        saved_user = self.user 
        self.user = None
        saved_user.delete()
        super(Profile, self).delete(*args, **kwargs)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    
    @admin.display(description="Почта")
    def get_email(self):
        return self.user.email
    
    @admin.display(description="Имя")
    def get_first_name(self):
        return self.user.first_name
    
    @admin.display(description="Фамилия")
    def get_last_name(self):
        return self.user.last_name
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
