from modulbank.client import ModulbankClient
import modulbank.structs as structs
import requests

# r = requests.post("https://api.modulbank.ru/v1/" + 'account-info', json={}, headers={'Authorization': 'Bearer ' + 'C287F0E42A45F9DC25678ACF5531C085'})
# new = requests.post('https://api.modulbank.ru/v1/account-info/balance/'+'d94a5235-7a7f-4524-a160-9f4af4bd15c8',  json={}, headers={'Authorization': 'Bearer ' + 'C287F0E42A45F9DC25678ACF5531C085'})
# print(new.json())
 сlient = ModulbankClient(token='C287F0E42A45F9DC25678ACF5531C085', sandbox_mode=True)

# #print(client.accounts())

# # "https://api.modulbank.ru/v1/account-info', json={}, headers={'Authorization': 'Bearer ' + 'C287F0E42A45F9DC25678ACF5531C085'}


req = requests.Request('POST', "https://api.modulbank.ru/v1/" + 'account-info', json={}, headers={'Authorization': 'Bearer ' + 'C287F0E42A45F9DC25678ACF5531C085'})
prepared = req.prepare()


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

pretty_print_POST(prepared)
s = requests.Session()
print(s.send(prepared))