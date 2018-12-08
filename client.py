import requests
import jsonpickle

from wallet import Wallet
from transaction import Transaction


class Client():
    def send_transaction(self):
        NotImplemented
    
    def send(self):
        url = 'http://localhost:5000/get_blocks'
        t = Transaction("Ali", "Umar", 500)
        headers = {"Content-Type": "application/json"}
        payload = jsonpickle.encode(t)
        res = requests.post(url, data=payload, headers=headers)
        print(res.text)

client = Client()
client.send()