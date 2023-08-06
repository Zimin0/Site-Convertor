from django.db import models
from django.contrib.auth.models import User

class SupportRequest(models.Model):
    PRIORITY = (
        ('HIGH', 'Высокий'),
        ('NORMAL', 'Средний'),
        ('LOW', 'Низкий'),
    )

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.SET_NULL, help_text="Пользователь, обратившийся в поддержку", null=True, blank=False)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=False)
    email = models.CharField(max_length=100, verbose_name="Эл.почта", blank=True)
    priority_rate = models.CharField(max_length=10, choices=PRIORITY, verbose_name="Приоритет")
    message = models.TextField(verbose_name="Текст", blank=False)
    datetime = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        print(f"Создан/обновлен запрос в техподрежку №{self.id}: {self.datetime}")
        super(SupportRequest, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'