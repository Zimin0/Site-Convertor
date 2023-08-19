from production_settings.models import ProductionSettings
import requests
import hashlib
import time
import json
import base64
import string
import random
import ast

class ModulBankPayment:
    def __init__(self, merchant:str, secret_key:str, test_mode:int, success_url:str="https://pay.modulbank.ru/success"):
        self.merchant = merchant # внести в натсройку в адимин панель
        self.secret_key = secret_key # идентично вынести 
        self.test_mode = test_mode
        self.success_url = '' 
        self.success_url = success_url
    
    def create_payment_order(self, custom_order_id:str, client_email:str=None, client_name:str='User', description:str='Конвертация на сайте SAP-XML-Generator-Converter'):
        """ 
        Создает счет на оплату.
        https://modulbank.ru/support/creating_invoice_for_payment
        * custom_order_id - Слаг заказа на конвертацию из БД 
        * client_name - Имя клиента из User БД
        * client_email - Почта клиента из User БД
        """
        url = "https://pay.modulbank.ru/api/v1/bill/"
        receipt_items = self.__get_receipt_items()
        callback_url = "https://938a-91-238-229-3.ngrok-free.app/ru/payment/catch-payment/"

        data = {
            # Статические 
            "amount": self.__get_amount(receipt_items), 
            "description": description,
            "unix_timestamp": int(time.time()),
            "callback_url": callback_url,
            "success_url": self.success_url, # "https://938a-91-238-229-3.ngrok-free.app/ru/payment/catch-payment/", 
            "salt": ModulBankPayment.__generate_salt(),
            "reusable": 0,
            "lifetime": 20*60, # Срок актуальности счета в секундах. По истечению счет будет недоступен к оплате # __Необязательное__ 
            "send_letter": 1, # Флаг отправки письма с уведомлением о выставленном счете # __Необязательное__
            "callback_on_failure" : 1, # Включение/отключение отправки уведомления, когда операция завершилась неуспешно # __Необязательное__
            # Динамические (Брать из БД) 
            "merchant": self.merchant, # настройки admin 
            "testing": self.test_mode,# настройки settings
            "custom_order_id": custom_order_id, # брать из таблицы ConvertOrder # __Необязательное__
            "client_name": client_name, # Брать из базы данных # __Необязательное__
            #"client_email": client_email, # Если указано это поле и передано "send_letter"=1, то клиенту будет отправлено письмо с уведомлением о выставлении счета # __Необязательное__
            #"receipt_contact": client_email, # Еmail получателя чека # __Необязательное__
        }

        data['receipt_items'] = json.dumps(receipt_items)
        data['signature'] = ModulBankPayment.get_signature(self.secret_key, data)
        if client_email:
            data['client_email'] = client_email
            data['receipt_contact'] = client_email
        else:
            data['client_email'] = ''
            data['receipt_contact'] = ''
         
        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("Успешный запрос в Модульбанк!")
            print(response.json())
        else:
            print(f"Ошибка запроса в Модульбанк!: {response.status_code}\n {response.text}")
            return {'payment_confirmed':False}
        string_data = response.text 
        string_data = string_data.replace("'", '"')

        data_js =  json.loads(string_data)
        data = {
            'payment_confirmed': True,
            'url': data_js['bill']['url'], # url оплаты
            #'id': custom_order_id, # !!!!!!!!!!!!!!!!!!!!!!! meta: {"bill_id": "JhA7sewdkjoaysjR0O1Im1"}
        }
        return data
    
    def __get_amount(self, receipt_items:list) -> str:
        """ Возвращает суммарную стоимость товаров в словаре. """
        price_sum = 0
        for prod in receipt_items:
            price_sum += float(prod['price'])
        return str(price_sum)

    def __get_receipt_items(self, amount:int=1, name:str='Convertation'):
        receipt_items = [
            {'name': name, 
             'price': ModulBankPayment.__get_convertation_price(), 
             'quantity': str(amount), 
             'sno': 'osn', 
             'payment_object': 'service', 
             'payment_method': 'full_prepayment', 
             'vat':'none', }
        ]
        return receipt_items
    
    @staticmethod
    def __get_convertation_price() -> str:
        """ Достает из БД стоимость 1 конвертации. """
        price = ProductionSettings.objects.filter(slug='RUBLE_PRICE')
        if price.exists():
            return str(price.first().value)
        else:
            raise NoDBSettingsField('RUBLE_PRICE')
        
    @staticmethod
    def __generate_salt(length:int=32) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        salt = ''.join(random.choice(characters) for i in range(length))
        return salt

    def __get_raw_signature(self, params:dict):
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

    def __double_sha1(self, data:str):
        sha1_hex = lambda s: hashlib.sha1(s.encode('utf-8')).hexdigest()
        digest = sha1_hex(self.secret_key + sha1_hex(self.secret_key + data))
        return digest

    def __get_signature(self, params:dict) -> str:
        return self.__double_sha1(self.__get_raw_signature(params))

    @staticmethod
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
    @staticmethod
    def double_sha1(secret_key, data):
        sha1_hex = lambda s: hashlib.sha1(s.encode('utf-8')).hexdigest()
        digest = sha1_hex(secret_key + sha1_hex(secret_key + data))
        return digest
    @staticmethod
    def get_signature(secret_key: str, params: dict) -> str:
        return ModulBankPayment.double_sha1(secret_key, ModulBankPayment.get_raw_signature(params))
    @staticmethod
    def get_amount(receipt_items:list) -> str:
        price_sum = 0
        for prod in receipt_items:
            price_sum += float(prod['price'])
        return str(price_sum)
    @staticmethod
    def generate_salt(length=32):
        characters = string.ascii_letters + string.digits + string.punctuation
        salt = ''.join(random.choice(characters) for i in range(length))
        return salt

class NoDBSettingsField(Exception):
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(self.message)

    @property
    def message(self):
        return f"В базе данных нет поля {self.field_name}. Создайте его через админ панель Django."

# mb_object = ModulBankPayment(
#     merchant="d94a5235-7a7f-4524-a160-9f4af4bd15c8",
#     secret_key="C287F0E42A45F9DC25678ACF5531C085",
#     test_mode=1,
#     success_url= "https://938a-91-238-229-3.ngrok-free.app/ru/payment/catch-payment/"
# )
# response = mb_object.create_payment_order(
#     custom_order_id="1223",
#     client_name='Никита'
#     )
# print(response)