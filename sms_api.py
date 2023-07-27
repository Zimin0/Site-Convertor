import requests
import json
import random 


url = 'https://admin.p1sms.ru/apiSms/create'

headers = {
    'Content-Type': 'application/json'
}

text = '''Код подтверждения для входа на сайт SAPXMLVersionUP.ru: %w'''
text = text.replace('%w', str(random.randint(1000,9999)))
print(text)
nikita_phone = '79313661220'

data = {
  "apiKey": "LqipzI6SfjigFgVxUjCkXeQFnFLIPkzYjlIfnta3EKgYIwDKkOwEK6WczrQy",
  "webhookUrl": "https://admin.p1sms.ru/apiSms/create",
  "sms": [
    {
      "channel": "char",
      "phone": nikita_phone
      ,
      "text": text,
      "sender": "VIRTA"
    }
  ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.text)
