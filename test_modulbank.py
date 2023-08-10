from modulbank.client import ModulbankClient
import modulbank.structs as structs
import requests

r = requests.post("https://api.modulbank.ru/v1/" + 'account-info', json={}, headers={'Authorization': 'Bearer ' + 'C287F0E42A45F9DC25678ACF5531C085'})
new = requests.post('https://api.modulbank.ru/v1/account-info/balance/'+'d94a5235-7a7f-4524-a160-9f4af4bd15c8',  json={}, headers={'Authorization': 'Bearer ' + 'C287F0E42A45F9DC25678ACF5531C085'})
print(new)
сlient = ModulbankClient(token='C287F0E42A45F9DC25678ACF5531C085', sandbox_mode=True)

#print(client.accounts())