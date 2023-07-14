from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class ConvertOrder(models.Model):
    class Meta:
        verbose_name = "Заказ на конвертацию"
        verbose_name_plural = "Заказы на конвертацию"

    STATUS = (
        ('OC', 'Заказ создан'),
        ('CS', 'Конвертация успешна'),
        ('CF', 'Конвертация провалена'),
        ('LI', 'Пользователь зашел под номером телефона'),
        ('WP', 'Ожидает оплаты'),
        ('PE', 'Ошибка оплаты'),
        ('SU', 'Заказ оплачен'),
        ('FD', 'Файл скачан'),
    )

    user = models.ForeignKey(User, verbose_name="Пользователь", null=True, related_name='convert_orders', on_delete=models.SET_NULL)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    current_status = models.CharField(max_length=2, choices=STATUS, verbose_name='Статус', default='OC')
    #phone_is_confirmed = models.BooleanField(verbose_name="Телефон подтвержден", default=False)
    need_to_pay = models.BooleanField(verbose_name="Нужно ли оплатить", default=False)
    paid = models.BooleanField(verbose_name="Оплачено", default=False)

    def get_formatted_creation_date(self):
        """ Возвращает отформатированную дату создания в виде: 13_07_13_15:53 """
        return datetime.strftime(self.creation_date, "%d_%m_%Y_%H:%M")

    def __str__(self) -> str:
        return f'Конвертация №{self.id}'
