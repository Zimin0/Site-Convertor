from django.db import models
from convert_order.models import ConvertOrder

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

    def __str__(self) -> str:
        return f'{self.file}'

    order = models.ForeignKey(ConvertOrder, null=True, verbose_name="Заказ", on_delete=models.SET_NULL, related_name='files')
    file = models.FileField(verbose_name="Файл", upload_to="%d/%m/%Y/")
    file_type = models.CharField(max_length=2, choices=TYPE, default='0', verbose_name="Тип файла (1, 2 или 3)")
