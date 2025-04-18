from .transaction import Transaction

class FinanceTracker:

    def __init__(self):
        self.transactions: list[Transaction] = []
        self.total_incone: float = 0
        self.total_expenses: float = 0

    def add_transaction(self, transaction: Transaction) -> None:

        self.transactions.append(transaction)

    def delete_transaction(self, transaction: Transaction) -> None:

        self.transactions.remove(transaction)

    def calculate_balance(self):
        pass
