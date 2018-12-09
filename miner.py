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

@node.route('/blocks', methods=["POST"])
def get_blocks():
        block = request.get_json()
        print(block)
        return "Block received"

@node.route('/transactions', methods=["POST"])
def get_transactions():
    tx = request.get_json()
    tx = json.dumps(tx) #convert dict to json
    tx = jsonpickle.decode(tx)
    status = tx.commit(blockchain)
    if status is True:
        block = Block(tx)
        blockchain.add_block(block)
        return "Transaction was successful."
    else:
        return status

@node.route('/balance')
def get_balance():
    user_id = request.args['user_id']
    return str(blockchain.get_balance(user_id))


###############################################################

if len(sys.argv) < 3:
    print("Please pass miner's name and port as parameters")
    exit()

wallet = Wallet(sys.argv[1])
blockchain = Blockchain()

node.run(host="localhost", port=sys.argv[2], debug=True)