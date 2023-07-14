import requests

answer = requests.get('http://192.168.48.11/test.php')
print(answer.text)