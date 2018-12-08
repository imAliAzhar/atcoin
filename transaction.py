import hashlib
import json

from record import Record

class Transaction:
    def __init__(self, frm, to, amount, kind="regular"):
        self.frm = frm
        self.to = to
        self.amount = amount
        self.kind = kind
        self.input = []
        self.output = []

    def commit(self, chain):
        if self.kind == "regular":
            self.input = chain.get_unspent_records(self.frm)
            unspent_amount = chain.get_balance(self.frm)
            if self.amount > unspent_amount:
                return "Insufficient balance for this transaction. Current balance: " + str(unspent_amount)
            remainder_amount = unspent_amount - self.amount
            self.output.append(Record(self.to, self.amount))
            self.output.append(Record(self.frm, remainder_amount))
            return True
        elif self.kind == "buy":
            self.output.append(Record(self.to, self.amount))
            return True


        

        