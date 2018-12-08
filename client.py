import sys
import requests
import jsonpickle

from wallet import Wallet
from transaction import Transaction


URL = 'http://localhost:2999/'

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
        print("\nCurrent Balance:", response.text, "BTC")

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

print("Welcome {0}!".format(sys.argv[1].lower().capitalize()))
client = Client(sys.argv[1])

while True:
    response = 0
    while response not in ["1", "2", "3", "4"]:
        response = input("1. Send coins to another wallet\n2. Check available balance\n3. Buy coins\n4. Exit\n\n")
        if response == "1":
            NotImplemented
        if response == "2":
            client.get_balance()
        if response == "3":
            amount = input("\nEnter number of coins to buy:\n")
            client.buy(str(amount))
        if response == "4":
            exit()
        
        print()