import sys
import requests
import json
import jsonpickle
from flask import Flask, request

from wallet import Wallet
from transaction import Transaction
from chain import Blockchain
from block import Block


node = Flask(__name__)

@node.route('/connect')
def add_peer():
    port = request.args['port']
    if port not in peers:
        display("Adding new peer: " + port)
        peers.append(port)
    else:
        display("Peer " + port + " already exists.")
    return jsonpickle.encode(peers)

@node.route('/chain')
def send_chain():
    return jsonpickle.encode(blockchain)

@node.route('/block', methods=["POST"])
def get_blocks():
        block = request.get_json()
        block = json.dumps(block) # convert dict to json
        block = jsonpickle.decode(block)
        blockchain.is_block_valid(block)
        return "Block received"

@node.route('/transactions', methods=["POST"])
def get_transactions():
    tx = request.get_json()
    tx = json.dumps(tx) # convert dict to json
    tx = jsonpickle.decode(tx)
    status = tx.commit(blockchain)
    if status is True:
        block = Block(tx)
        blockchain.add_block(block)
        broadcast(block)
        return "Transaction was successful."
    else:
        return status

@node.route('/balance')
def get_balance():
    user_id = request.args['user_id']
    return str(blockchain.get_balance(user_id))

def broadcast(block):
    base_url = "http://localhost:" 
    headers = {"Content-Type": "application/json"}
    payload = jsonpickle.encode(block)
    for peer in peers:
        url = base_url + str(peer) + "/block"
        requests.post(url, data=payload, headers=headers)


def display(message):
   print("\033[0;33m" + str(message) + "\033[0;00m") 

# def interactive_menu():
#     while True:
#         response = 0
#         while response not in ["1", "2", "3", "4"]:
#             response = input("1. Connect to the network\n2. Check available balance\n3. Buy coins\n4. Exit\n\n")
            
#             if response == "1":
    


###############################################################

if len(sys.argv) < 3:
    display("Please pass miner's name and port as parameters")
    exit()

wallet = Wallet(sys.argv[1])
peers = []

if sys.argv[2] == "-bs": # bootstrap node differentiates itself, does not pass port
    blockchain = Blockchain()
    port = 5000 # default port for bootstrap node
else:
    display("Connecting to bootstrap node...")
    base_url = "http://localhost:5000/"
    port = sys.argv[2]
    payload = {'port': port}
    url = base_url + "connect"
    response = requests.get(url, params=payload)
    peers = jsonpickle.decode(response.text)
    peers.append(5000) # add bootstrap node to peers
    url = base_url + "chain"
    response = requests.get(url)
    blockchain = jsonpickle.decode(response.text)

display("Running at port " + str(port))
node.run(host="localhost", port=port)