# from modulbank.client import ModulbankClient
# import modulbank.structs as structs

import base64
import hashlib
 
 
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
    '''Двойное шифрование sha1 на основе секретного ключа'''
    sha1_hex = lambda s: hashlib.sha1(s.encode('utf-8')).hexdigest()
    digest = sha1_hex(secret_key + sha1_hex(secret_key + data))
    return digest
 

def get_signature(secret_key: str, params: dict) -> str:
    '''
    Вычисляем подпись (signature). Подпись считается на основе склеенной строки из отсортированного массива параметров, исключая из расчета пустые поля и элемент "signature" 
    Определяем словарь с параметрами для расчета.
    В этот массив должны войти все параметры, отправляемые в вашей форме (за исключением самого поля signature, значение которого вычисляем).
    Получив вашу форму, система ИЭ аналогичным образом вычислит из ее параметров signature и сравнит значение с вычисленным на стороне вашего магазина.
    Подставьте ваш секретный ключ вместо 00112233445566778899aabbccddeeff 
    '''
    return double_sha1(secret_key, get_raw_signature(params))

import requests
import hashlib
import time
import json

# Параметры
success_url = "https://pay.modulbank.ru/success"
secret_key = "C287F0E42A45F9DC25678ACF5531C085"

# Опциональные параметры
testing = 1
client_email = "nik.zimenkov.00@inbox.ru"
client_name = "Имя Фамилия"
custom_order_id = "order123"
lifetime = 604800
send_letter = 1
receipt_contact = "nik.zimenkov.00@inbox.ru"
receipt_items = json.dumps([{"name": "item1", "price": "100.00", "quantity": 2, 'sno':'sno', 'payment_object':'commodity '}])
salt = "random_salt"

# Формирование подписи
#signature_string = f"{merchant}{amount}{description}{unix_timestamp}{salt}{secret_key}"
signature = 'C287F0E42A45F9DC25678ACF5531C085' # hashlib.sha1(signature_string.encode()).hexdigest()

# Формирование данных для POST-запроса
data = {
    "merchant": "d94a5235-7a7f-4524-a160-9f4af4bd15c8",
    "amount": "918.45",
    "description": "Описание платежа",
    "unix_timestamp": int(time.time()),
    "testing": 1,
    "success_url": 'https://pay.modulbank.ru/success',
    "signature": '', # В тестовом режиме используйте тестовый секретный ключ. C287F0E42A45F9DC25678ACF5531C085  '78d9e7d4ec844885790f185ce0e7a60374d01cbc'
    # Опциональные параметры
    
    # "client_email": client_email,
    # "client_name": client_name,
    # "custom_order_id": custom_order_id,
    # "lifetime": lifetime,
    # "send_letter": send_letter,
    # "receipt_items": receipt_items,
    # "salt": salt
}

data['signature'] = get_signature('C287F0E42A45F9DC25678ACF5531C085', data)

# URL API
url = "https://pay.modulbank.ru/api/v1/bill/"

# Отправка POST-запроса
response = requests.post(url, json=data)

# Обработка ответа
if response.status_code == 200:
    print("Успешный запрос!")
    print(response.json())
else:
    print(f"Ошибка: {response.status_code}")
print(response.text)
