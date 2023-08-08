from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from production_settings.models import ProductionSettings
from django.shortcuts import get_object_or_404

def get_convertation_amount():
    amount_settings = get_object_or_404(ProductionSettings, slug='CONVERT_AMOUNT')
    return amount_settings.value

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', null=True, blank=True, unique=True, help_text='Номер телефона в формате +79112345678')
    phone_is_confirmed = models.BooleanField(verbose_name="Телефон подтвержден", default=False)
    amount_of_converts = models.IntegerField(verbose_name="Кол-во конвертаций", default=10, validators=[MinValueValidator(0)])
    
    def __str__(self): # Надо поменять 
        return f'Профиль пользователя {self.user}' 
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    