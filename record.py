import hashlib
import time


class Record:
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount
        self.id = self.compute_hash()

    def compute_hash(self):
        sha = hashlib.sha256()
        sha.update(self.address + self.amount + time.time())
        return sha.hexdigest()