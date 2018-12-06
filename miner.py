import sys
import time
import hashlib

from block import Block

class Miner:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {
            "proof-of-work": 9,
            "transactions": None},
            "0")





# main
if len(sys.argv) < 3:
    print('Please enter IP and Port for the miner to run on.')
    sys.exit()
else:
    miner = Miner(sys.argv[1], sys.argv[2])
