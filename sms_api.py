import requests
import json
import random 


url = 'https://admin.p1sms.ru/apiSms/create'

headers = {
    'Content-Type': 'application/json'
}

text = ''' Код подтверждения: %w
Интернет-конвертор файлов 
'''
text = text.replace('%w', str(random.randint(1000,9999)))
print(text)
nikita_phone = '79313661220'

data = {
  "apiKey": "ELpxOigS8MnuhzF9Io9sJyM8BthMkcR5FMYMlJ7b3eOR0EU41HGo83LvnldH",
  "webhookUrl": "https://admin.p1sms.ru/apiSms/create",
  "sms": [
    {
      "channel": "char",
      "phone": nikita_phone
      ,
      "text": text,
      "sender": "Зименков Никита Вячеславович"
    }
  ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.text)
