import time
import hashlib

from transaction import Transaction


class Block:
    def __init__(self, index, timestamp, transaction, previous_hash=0):
        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.transaction) 
            + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()
    
    def to_json(self):
        return {
            "index": str(self.index),
            "timestamp": time.ctime(self.timestamp),
            "transaction": self.transaction.to_json(),
            "p_hash": self.previous_hash,
            "hash": self.hash
        }

    def mine_block(self, difficulty):
        while self.hash[0: difficulty] != '0' * difficulty:
          self.nonce = self.nonce + 1
          self.hash = self.compute_hash()

        print("Block mined: " + self.hash)
