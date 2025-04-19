import os
import json

from models import Transaction, TransactionType

DATA_FILE = "data/transactions.json"

class Data:
    
    def __init__(self):
        pass

    def save_transactions(self, transactions):
        with open(DATA_FILE, "w") as f:
            data = [t.transaction_to_dict() for t in transactions]
            json.dump(data, f, indent=4)

    def load_transactions(self):
        self.transactions = []
        if not os.path.exists(DATA_FILE):
            return self.transactions

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for d in data:
                t = Transaction(
                    amount=d["amount"],
                    category=d["category"],
                    subcat=d["subcat"],
                    type=TransactionType(d["type"]),
                    date=d["date"]
                )
                self.transactions.append(t)
            
        return self.transactions


    