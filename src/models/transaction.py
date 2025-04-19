from datetime import date

from .enums import TransactionType

class Transaction:
    def __init__(self, amount: float, category: str, type: TransactionType, date: date, subcat: str):
        self.amount = amount
        self.category = category
        self.type = type
        self.date = date
        self.subcat = subcat
    
    
        