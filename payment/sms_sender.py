import requests
import json
import random 

def __generate_sms_code() -> int:
    """ Генерирует смс код (int) """
    return random.randint(1_000, 9_999+1)

def send_confiramtion_code(phone) -> int:
    """ Возвращает код подтверждения"""
    url = 'https://admin.p1sms.ru/apiSms/create'
    headers = {
        'Content-Type': 'application/json'
    }
    code = __generate_sms_code()
    text = f"""Код подтверждения для входа на сайт SAPXMLVersionUP.ru: {code}""" 
    data = {
    "apiKey": "LqipzI6SfjigFgVxUjCkXeQFnFLIPkzYjlIfnta3EKgYIwDKkOwEK6WczrQy",
    "webhookUrl": "https://admin.p1sms.ru/apiSms/create",
    "sms": [
        {
        "channel": "char",
        "phone": phone,
        "text": text,
        "sender": "VIRTA"
        }
    ]
    }
    # response = requests.post(url, headers=headers, data=json.dumps(data))
    # print(response.text)
    print(f'code = {code}')
    return code

"""
мультиязычость 
появляющиеся стрелки 
привязывать номер телефона
куда вставить ролик
телефон в базе данных 
поменять названия ( в телеграмме )
"""