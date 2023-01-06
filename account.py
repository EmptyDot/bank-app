from __future__ import annotations
from decimal import Decimal, getcontext

getcontext()


class Account:
    def __init__(self, account_number: int, balance: int | float = 0):
        self.account_number = account_number
        self._balance = Decimal(balance)

    @property
    def balance(self) -> float:
        """
        Get the balance to be presented to the user, not to be used for arithmetic operations.
        :return: Balance represented as a float with 2 decimals of precision
        """
        return float(round(self._balance, 2))

    def balance_add(self, amount: int | float) -> bool:
        """
        Add an amount to the current account balance
        :param amount: Amount to be added
        :return: True if successful else False
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False

        self._balance = self._balance + Decimal(amount)
        return True

    def balance_sub(self, amount: int | float) -> bool:
        """
        Subtract an amount from the current account balance
        :param amount: Amount to be subtracted
        :return: True if successful else False
        """
        if not isinstance(amount, (int, float)) or amount <= 0 or amount > self._balance:
            return False

        self._balance = self._balance - Decimal(amount)
        return True

    def __str__(self):
        return f"Account({self.account_number}, balance={self._balance})"

    def __repr__(self):
        return f"Account({self.account_number}, balance={self._balance})"

