from django.test import TestCase
from production_settings.models import ProductionSettings

data = [
    {
       'name': 'Почта техподдержки для получения писем',
       'slug': 'TECH_EMAIL_TO',
       'value':  'nikzim2004@gmail.com'
    }, 
    {
       'name': 'Ключ приложения от почты gmail',
       'slug': 'GMAIL_APP_KEY',
       'value': 'value' 
    }, 
    {
       'name': 'Цена в рублях',
       'slug': 'RUBLE_PRICE',
       'value': '310' 
    },     {
       'name': 'Кол-во бесплатных конвертаций',
       'slug': 'CONVERT_AMOUNT',
       'value': '2' 
    },     {
       'name': 'Почта техподдержки для отправки писем',
       'slug': 'TECH_EMAIL_FROM',
       'value': 'nikzim2004@gmail.com' 
    }, 
]

for setting in data:
    exists_in_db = ProductionSettings.objects.filter(name=setting['name']).exists()
    
    if not exists_in_db:
        print(f"Настройка '{setting['name']}' еще не добавлена!")
        s = ProductionSettings.objects.create(
            name=setting['name'],
            slug=setting['slug'],
            value=setting['value'],
        )
        s.save()
    else:
        print(f"Настройка {setting['name']} уже существует!")
