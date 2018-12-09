import sys
import requests
import json
import jsonpickle
import argparse
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
        broadcast(block)
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
    payload = {'port': args.address}
    url = peer_url + "/connect"
    response = requests.get(url, params=payload)
    peers = jsonpickle.decode(response.text)
    peers.append(args.peer)
    url = peer_url + "/chain"
    response = requests.get(url)
    blockchain = jsonpickle.decode(response.text)

display("Running at port " + str(args.address))
node.run(host="localhost", port=args.address)