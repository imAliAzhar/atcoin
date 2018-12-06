import hashlib

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) 
            + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()
    
    def mine_block(self, difficulty):
        while self.hash[0, difficulty] != '0' * difficulty:
          self.nonce = self.nonce + 1
          self.hash = self.hash_block()
      
        print("Block mined: " + self.hash)