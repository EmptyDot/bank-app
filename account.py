from __future__ import annotations


class Account:
    def __init__(self, account_number: int, balance: int | float):
        self.account_number = account_number
        self.balance = balance

    def get_balance(self):
        pass

    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass
