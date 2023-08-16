import requests
import hashlib
import time
import json
import base64
import string
import random

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
    {"name": "Convertation", "price": "100.00", "quantity": 1, "sno": "osn", "payment_object": "service", 'payment_method': 'full_prepayment', 'vat':'none', }
]
merchant = "d94a5235-7a7f-4524-a160-9f4af4bd15c8"
success_url = "https://pay.modulbank.ru/success"
secret_key = "C287F0E42A45F9DC25678ACF5531C085"
data = {
    "merchant": merchant,
    "amount": get_amount(receipt_items),
    "description": "Конвертация на сайте SAP-XML-Generator-Converter",
    "unix_timestamp": int(time.time()),
    "testing": 1, # !!!!!!!!!!!!!!!!!!!!!!!!
    "reusable": 1,
    "callback_url": "https://85c6-185-211-159-37.ngrok-free.app/payment/catch-payment/", # !!!!!!!!!!!!!!!!!!!!!!!!
    "salt": generate_salt(),
    "success_url": "https://85c6-185-211-159-37.ngrok-free.app", # !!!!!!!!!!!!!!!!!!!!!!!!
    "custom_order_id": "1234",
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
print(response.text)

class ModulBankPayment:
    def __init__(self, merchant:str, secret_key:str, test_mode:bool):
        self.merchant = merchant
        self.secret_key = secret_key
        self.test_mode = test_mode
        self.success_url = '' 
    
    def create_payment_order(self):
        status = True
        return status