from django.db import models
from convert_order.models import ConvertOrder
import datetime

class File(models.Model):
    """ Файлы для конвертации """
    class Meta:
        verbose_name = "Загруженный файл"
        verbose_name_plural = "Загруженные файлы"

    TYPE = (
        ('0','Неизвестный тип'),
        ('1','Исходный №1'),
        ('2','Исходный №2'),
        ('3','Конвертированный'),
    )

    def generate_result_name(self):
        """ Возварщает имя файла в формате Result{год}{месяц}{день}{часы}{минуты}{секунды}"""
        current_datetime = datetime.datetime.now()
        result_string = f"Result{current_datetime.year}{current_datetime.month:02d}{current_datetime.day:02d}{current_datetime.hour:02d}{current_datetime.minute:02d}{current_datetime.second:02d}"
        return result_string

    def __str__(self) -> str:
        return f'{self.file}'

    order = models.ForeignKey(ConvertOrder, null=True, verbose_name="Заказ", on_delete=models.SET_NULL, related_name='files')
    file = models.FileField(verbose_name="Файл", upload_to="%Y/%m/%d/")
    file_type = models.CharField(max_length=2, choices=TYPE, default='0', verbose_name="Тип файла (1, 2 или 3)")
