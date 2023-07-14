from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator

# Create your models here.
class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self): # Надо поменять 
        return f'Профиль пользователя {self.user}' 
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', null=True, unique=True, help_text='Номер телефона в формате +79112345678')
    phone_is_confirmed = models.BooleanField(verbose_name="Телефон подтвержден", default=False)
    convert_already = models.BooleanField(verbose_name="Была ли хотя бы 1 конвертация ", default=False)
    amount_of_converts = models.IntegerField(verbose_name="кол-во конвертаций", default=0, validators=[MinValueValidator(0  )])

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()