from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import random


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

    phone = models.CharField(max_length=100, verbose_name="Номер телефона пользователя", null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    slug = models.CharField(max_length=100, verbose_name="Слаг для url", unique=True, null=True, blank=True)
    modulbank_transaction_id = models.CharField(max_length=200, verbose_name="ID в модульбанке", blank=True, null=True)
    current_status = models.CharField(max_length=2, choices=STATUS, verbose_name='Статус', default='OC')
    need_to_pay = models.BooleanField(verbose_name="Нужно ли оплатить", default=False)
    paid = models.BooleanField(verbose_name="Оплачено", default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            super(ConvertOrder, self).save(*args, **kwargs)
            self.slug = self.__crypt_id(self.id)
        super(ConvertOrder, self).save(*args, **kwargs) ### ПЕРЕГРУЖАЕТ СИСТЕМУ !!!!
        

    def get_formatted_creation_date(self):
        """ Возвращает отформатированную дату создания в виде: 13_07_13_15:53 """
        return datetime.strftime(self.creation_date, "%d_%m_%Y_%H:%M")
    
    @staticmethod
    def __crypt_id(id):
        """ Переводит id заказа в строку для url ("шифрует").\n
        Что-то типо хэша, но только можно расшифровать обратно."""
        id_new_str = str(id)
        letters = 'abcdefghijklmnopqrstuvwxyz'
        NUM_OF_LETTERS = 7
        for _ in range(NUM_OF_LETTERS):
            random_index = random.randint(0, len(str(id_new_str))-1)
            id_new_str = id_new_str[:random_index] + random.choice(letters) + id_new_str[random_index:]
        return id_new_str
    
    @staticmethod
    def decrypt_id(crypted_id):
        """ Расшифровывает id заказа, зашифрованный функцией crypt_id() """
        letters = 'abcdefghijklmnopqrstuvwxyz'
        decrypted_id = ''
        for letter in crypted_id:
            if letter not in letters:
                decrypted_id += letter
        return decrypted_id

    def __str__(self) -> str:
        return f'Конвертация №{self.id}'
