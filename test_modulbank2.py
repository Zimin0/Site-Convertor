import requests
import hashlib
import time
import json
import base64
import string
import random
import ast

def create_test_modulbank_order(custom_order_id):
    def get_raw_signature(params):
        chunks = []
        for key in sorted(params.keys()):
            if key == 'signature':
                continue
            value = params[key]
            if isinstance(value, str):
                value = value.encode('utf8')
            else:
                value = str(value).encode('utf-8')
            if not value:
                continue
            value_encoded = base64.b64encode(value)
            chunks.append('%s=%s' % (key, value_encoded.decode()))
        raw_signature = '&'.join(chunks)
        return raw_signature

    def double_sha1(secret_key, data):
        sha1_hex = lambda s: hashlib.sha1(s.encode('utf-8')).hexdigest()
        digest = sha1_hex(secret_key + sha1_hex(secret_key + data))
        return digest

    def get_signature(secret_key: str, params: dict) -> str:
        return double_sha1(secret_key, get_raw_signature(params))

    def get_amount(receipt_items:list) -> str:
        price_sum = 0
        for prod in receipt_items:
            price_sum += float(prod['price'])
        return str(price_sum)

    def generate_salt(length=32):
        characters = string.ascii_letters + string.digits + string.punctuation
        salt = ''.join(random.choice(characters) for i in range(length))
        return salt

    receipt_items = [
        {"name": "Convertation", "price": "100.00", "quantity": "1", "sno": "osn", "payment_object": "service", 'payment_method': 'full_prepayment', 'vat':'none', }
    ]
    merchant = "d94a5235-7a7f-4524-a160-9f4af4bd15c8"
    success_url = "https://pay.modulbank.ru/success"
    secret_key = "C287F0E42A45F9DC25678ACF5531C085"
    data = {
        # Статические 
        "amount": get_amount(receipt_items), 
        "description": "Конвертация на сайте SAP-XML-Generator-Converter",
        "unix_timestamp": int(time.time()),
        "callback_url": "https://85c6-185-211-159-37.ngrok-free.app/ru/payment/catch-payment/",
        "success_url": "https://85c6-185-211-159-37.ngrok-free.app/ru/payment/catch-payment/", 
        "salt": generate_salt(),
        "reusable": 0,
        "lifetime": 20*60, # Срок актуальности счета в секундах. По истечению счет будет недоступен к оплате # __Необязательное__ 
        "send_letter": 1, # Флаг отправки письма с уведомлением о выставленном счете # __Необязательное__
        "callback_on_failure" : 1, # Включение/отключение отправки уведомления, когда операция завершилась неуспешно # __Необязательное__
        # Динамические (Брать из БД) 
        "merchant": merchant, # настройки admin 
        "testing": 1,# настройки settings
        "custom_order_id": custom_order_id, # брать из таблицы ConvertOrder # __Необязательное__
        "client_name": "Test Test", # Брать из базы данных # __Необязательное__
        #"client_email": "nik.zimenkov.00@inbox.ru", # Если указано это поле и передано "send_letter"=1, то клиенту будет отправлено письмо с уведомлением о выставлении счета # __Необязательное__
        #"receipt_contact": "nik.zimenkov.00@inbox.ru", # Еmail получателя чека # __Необязательное__
    }

    data['receipt_items'] = json.dumps(receipt_items)
    data['signature'] = get_signature(secret_key, data)

    url = "https://pay.modulbank.ru/api/v1/bill/"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Успешный запрос!")
        print(response.json())
    else:
        print(f"Ошибка: {response.status_code}")
    string_data = response.text # ['bill']['url']
    string_data = string_data.replace("'", '"')  # Заменяем одинарные кавычки на двойные

    data_js =  json.loads(string_data)
    data = {
        'url': data_js['bill']['url'], 
        'id': custom_order_id, # !!!!!!!!!!!!!!!!!!!!!!! meta: {"bill_id": "JhA7sewdkjoaysjR0O1Im1"}
    }
    return data


# create_test_modulbank_order() # sOJVYBMm6geOXMyb4wVm0H

class ModulBankPayment:
    url = "https://pay.modulbank.ru/api/v1/bill/"
    success_url = "https://pay.modulbank.ru/success"

    def __init__(self, merchant:str, secret_key:str, test_mode:bool):
        self.merchant = merchant
        self.secret_key = secret_key
        self.test_mode = test_mode
        self.success_url = '' 
    
    def create_payment_order(self):
        status = True
        return status

