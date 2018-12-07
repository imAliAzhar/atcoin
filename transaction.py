import hashlib


class Transaction:
    def __init__(self, by, to, amount, type="regular"):
        self.type = type
        self.amount = amount
        self.by = by
        self.to = to
        self.hash = self.compute_hash()

    def compute_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.type) + str(self.amount) + str(self.by) 
            + str(self.to)).encode('utf-8'))
        return sha.hexdigest()
        
    def to_json(self):
        return {
            "type": str(self.type),
            "by": str(self.by),
            "to": str(self.to),
            "amount": str(self.amount)
        }