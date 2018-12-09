import sys
import requests
import json
import jsonpickle
import argparse
from flask import Flask, request
from threading import Thread

from wallet import Wallet
from transaction import Transaction
from chain import Blockchain
from block import Block


node = Flask(__name__)

@node.route('/add_peer', methods=["POST"])
def add_peer():
    port = request.get_json()
    print(port)
    port = port["port"]
    print(port)
    if port not in peers:
        display("New peer added: " + str(port))
        peers.append(port)
        broadcast_peer(port)
        display("It's okay dont panic now")
    else:
        display("Peer " + port + " already exists.")
    return "Added"

@node.route('/transactions', methods=["POST"])
def get_transactions():
    tx = request.get_json()
    tx = json.dumps(tx) # convert dict to json
    tx = jsonpickle.decode(tx)
    status = tx.commit(blockchain)
    if status is True:
        block = Block(tx)
        blockchain.add_block(block)
        broadcast_block(block)
        return "Transaction was successful."
    else:
        return status

def broadcast_peer(new_peer):
    base_url = "http://localhost:" 
    headers = {"Content-Type": "application/json"}
    payload = {'port': new_peer}
    payload = json.dumps(payload)
    for peer in peers:
        if peer != args.address and peer != new_peer:
            url = base_url + str(peer) + "/add_peer"
            requests.post(url, data=payload, headers=headers)


@node.route('/get_peers')
def get_peers():
    return jsonpickle.encode(peers)

@node.route('/chain')
def send_chain():
    return jsonpickle.encode(blockchain)

@node.route('/block', methods=["POST"])
def get_blocks():
        block = request.get_json()
        block = json.dumps(block) # convert dict to json
        block = jsonpickle.decode(block)
        status = blockchain.is_block_valid(block)
        if status is True:
            broadcast_block(block)
        return "Block received"



@node.route('/balance')
def get_balance():
    display("<peers>")
    print(peers)
    display("</peers>")
    user_id = request.args['user_id']
    return str(blockchain.get_balance(user_id))

def broadcast_block(block):
    base_url = "http://localhost:" 
    headers = {"Content-Type": "application/json"}
    payload = jsonpickle.encode(block)
    for peer in peers:
        if peer != args.address:
            url = base_url + str(peer) + "/block"
            requests.post(url, data=payload, headers=headers)



def display(message):
    print("\033[0;33m" + str(message) + "\033[0;00m") 




###############################################################



parser = argparse.ArgumentParser(description='miner for atcoin')
parser.add_argument("-n", "--name", required=True, help="name of the wallet holder")
parser.add_argument("-a", "--address", required=True, help="port on which the node will listen")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-p", "--peer", help="any node in the network")
group.add_argument("-b", "--bootstrap", action='store_true', help="use if this node is a bootstrap node")

args = parser.parse_args()

wallet = Wallet(args.name)
peers = []

if args.bootstrap is True:
    display("Setting up bootstrap node...")
    blockchain = Blockchain()
else:
    display("Connecting to peer...")
    peer_url = "http://localhost:{0}".format(args.peer)

    url = peer_url + "/get_peers"
    response = requests.get(url)
    peers = jsonpickle.decode(response.text)
    peers.append(args.peer)

    url = peer_url + "/chain"
    response = requests.get(url)
    blockchain = jsonpickle.decode(response.text)

    url = peer_url + "/add_peer"
    headers = {"Content-Type": "application/json"}
    payload = {'port': args.address}
    payload = json.dumps(payload)
    response = requests.post(url, data=payload, headers=headers)

display("Running at port " + str(args.address))
node.run(host="localhost", port=args.address)