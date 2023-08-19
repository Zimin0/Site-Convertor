from django.db import models

class ProductionSettings(models.Model):
    """ Модель насроек сайта для админов. """
    name = models.CharField(max_length=300, blank=False, verbose_name="Название/описание настройки")
    slug = models.SlugField(max_length=20, verbose_name="Слаг", blank=False, editable=False, help_text="краткий слаг для разработчиков!!!")
    value = models.CharField(max_length=300, verbose_name="Значение", blank=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"