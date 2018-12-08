import hashlib
import time


class Record:
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount
        self.id = self.compute_hash()

    def compute_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.address) + str(self.amount) + str(time.time())).encode('utf-8'))
        return sha.hexdigest()