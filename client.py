import sys
import requests
import jsonpickle

from wallet import Wallet
from transaction import Transaction


URL = 'http://localhost:3000/'

class Client():
    def __init__(self, name):
        self.wallet = Wallet(name)

    def send_transaction(self):
        NotImplemented
    
    def buy(self, amount):
        tx = Transaction(self.wallet.public_key, self.wallet.public_key, amount, "buy")
        self.send(tx)

    def get_balance(self):
        url = URL + 'balance'
        payload = {'user_id': self.wallet.public_key}
        response = requests.get(url, params=payload)
        print("Current Balance:", response.text)

    def send(self, data):
        url = URL + 'transactions'
        headers = {"Content-Type": "application/json"}
        payload = jsonpickle.encode(data)
        response = requests.post(url, data=payload, headers=headers)
        print(response.text)

###############################################################

if len(sys.argv) < 2:
    print("Please pass client's name as parameter")
    exit()

client = Client(sys.argv[1])
client.buy(50)
client.get_balance()