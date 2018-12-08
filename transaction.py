import hashlib
import json

from record import Record

class Transaction:
    def __init__(self, frm, to, amount):
        self.frm = None
        self.to = None
        self.amount = None
        self.input = []
        self.output = []

    def commit(self, chain):
        self.input = chain.get_unspent_records()
        unspent_amount = 0
        for record in self.input:
            unspent_amount = unspent_amount + record.amount
        if self.amount > unspent_amount:
            return "Insufficient balance for this transaction. Current balance: " + str(unspent_amount)
        remainder_amount = unspent_amount - self.amount
        self.output.append(Record(self.to, self.amount))
        self.output.append(Record(self.frm, remainder_amount))
        return True

        

        