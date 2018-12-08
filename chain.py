import time
import json

from block import Block
from transaction import Transaction

class Blockchain:
    difficulty = 4

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis_block = Block(Transaction(0, 0 ,0))
        genesis_block.index = 0
        genesis_block.timestamp = time.time()
        return genesis_block

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]
    
    def add_block(self, new_block):
        new_block.id = self.get_latest_block().index + 1
        new_block.time = time.time()
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
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
    
    def get_unspent_records(self, user):
        input_records  = []
        output_records = []
        for block in self.chain:
            for record in block.transaction.input:
                if record.address == user:
                    input_records.append()
            for record in block.transaction.output:
                if record.address == user:
                    output_records.append()

        print("Input", input_records)
        print("Output", output_records)
        return [record for record in output_records if record not in input_records]         

    def get_balance(self, user_id):
        unspent_records = self.get_unspent_records(user_id)
        balance = 0
        print(unspent_records)
        for record in unspent_records:
                balance = balance + record.amount
        return balance            


    def to_json(self):
        json_array = []
        for block in self.chain:
            json_array.append(block.to_json())
        return json.dumps(json_array, indent=4)

# chain = Blockchain()

# transaction = Transaction("Ali", "Ayesha", 100)
# chain.add_block(Block(1, time.time(), transaction))
# chain.add_block(Block(2, time.time(), transaction))
# chain.add_block(Block(3, time.time(), transaction))

# print(chain.to_json())

# chain.chain[1].data = {"amount":"2000000"}
# chain.chain[1].hash = chain.chain[1].hash_block()
# print(chain.is_chain_valid())