import time
import hashlib
import json
import jsonpickle

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
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.hash_block():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False

        return True
    
    def to_json(self):
        json_array = []
        for block in self.chain:
            block = {
                "index": str(block.index),
                "timestamp": time.ctime(block.timestamp),
                "data": str(block.data),
                "p_hash": block.previous_hash,
                "hash": block.hash
            }
            json_array.append(block)
        return json.dumps(json_array, indent=4)

chain = Chain()

chain.add_block(Block(1, time.time(), {"amount": 20}, 0))
chain.add_block(Block(2, time.time(), {"amount": 40}, 0))
chain.add_block(Block(3, time.time(), {"amount": 60}, 0))

print(chain.to_json())

# chain.chain[1].data = {"amount":"2000000"}
# chain.chain[1].hash = chain.chain[1].hash_block()
# print(chain.is_chain_valid())