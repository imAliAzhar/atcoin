import os
import sys
import requests
import argparse
import jsonpickle

from wallet import Wallet
from transaction import Transaction


URL = 'http://localhost:'

class Client():
    def __init__(self, name):
        self.wallet = Wallet(name)

    def send_transaction(self, to, amount):
        tx = Transaction(self.wallet.public_key, to, amount)
        self.send(tx) 
    
    def buy(self, amount):
        tx = Transaction(self.wallet.public_key, self.wallet.public_key, amount, "buy")
        self.send(tx)

    def get_balance(self):
        url = URL + 'balance'
        payload = {'user_id': self.wallet.public_key}
        try:
            response = requests.get(url, params=payload)
            print("\nCurrent Balance:", response.text, "BTC")
        except:
            print("\nHost is offline..")

    def send(self, data):
        url = URL + 'transactions'
        headers = {"Content-Type": "application/json"}
        payload = jsonpickle.encode(data)
        try:
            response = requests.post(url, data=payload, headers=headers)
            print(response.text)
        except:
            print("\nHost is offline..")

###############################################################


parser = argparse.ArgumentParser(description='miner for atcoin')
parser.add_argument("-n", "--name", required=True, help="name of the wallet holder")
parser.add_argument("-p", "--peer", help="any node in the network")
args = parser.parse_args()

print("Welcome {0}!".format(args.name.lower().title()))
URL = URL + args.peer + "/" 

client = Client(args.name)

while True:
    response = 0
    while response not in ["1", "2", "3", "4"]:
        response = input("1. Send coins to another wallet\n2. Check available balance\n3. Buy coins\n4. Exit\n\n")
        
        if response == "1":
            to = input("\nEnter receiver's name:\n").title()
            amount = input("\nEnter amount to send:\n")

            pu_file = "keys/public/" + to.lower() + ".key"
            
            if os.path.isfile(pu_file):
                with open(pu_file, 'r') as f:
                    recv_key = f.readline()
                    client.send_transaction(recv_key, str(amount))
            else:
                print("\nWallet for {0} does not exist.".format(to))

        if response == "2":
            client.get_balance()

        if response == "3":
            amount = input("\nEnter number of coins to buy:\n")
            client.buy(str(amount))

        if response == "4":
            exit()
        
        print()