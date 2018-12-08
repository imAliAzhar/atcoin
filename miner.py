import sys
from flask import Flask, request
import requests

node = Flask(__name__)

@node.route('/helo')
def hello():
    return 'Hello World'

@node.route('/get_blocks', methods=["POST"])
def get_blocks():
    if request.method == 'POST':
        block = request.get_json()
        # print("Parameters")
        print(block)
        return "Block received"

def verify_transaction(transaction):
    NotImplemented





node.run()

# class Miner:
    # def __init__(self, ip, port):
        # self.ip = ip
        # self.port = port
# 



# main
# if len(sys.argv) < 3:
#     print('Please enter IP and Port for the miner to run on.')
#     sys.exit()
# else:
#     miner = Miner(sys.argv[1], sys.argv[2])
