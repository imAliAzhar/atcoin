import time
import hashlib
import json

from block import Block

class Chain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), 'Genesis Block', "0")

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]
    
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.hash_block()
        self.chain.append(new_block)
    
    def isChainValid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

chain = Chain()

chain.add_block(Block(1, "01/01/2018", {"amount": 20}, 0))
chain.add_block(Block(2, "01/01/2018", {"amount": 40}, 0))
chain.add_block(Block(3, "01/01/2018", {"amount": 60}, 0))

print(json.dumps(chain, sort_keys=True, indent=4))