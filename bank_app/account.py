from __future__ import annotations

from decimal import Decimal, getcontext
from typing import Union

from bank_app.logger import log_exc

getcontext()


class Account:
    def __init__(self, account_number: int, balance: Union[int, float] = 0):
        self.account_number = account_number
        self.__balance = Decimal(balance)

    @property
    def balance(self) -> float:
        """
        Get the balance to be presented to the user, not to be used for arithmetic operations.
        :return: Balance represented as a float with 2 decimals of precision
        """
        return float(round(self.__balance, 2))

    @log_exc(exc=ValueError, return_value=False)
    def balance_add(self, amount: Union[int, float]) -> bool:
        """
        Add an amount to the current account balance
        :param amount: Amount to be added
        :return: True if successful else False
        """
        if amount <= 0:
            raise ValueError(f"Amount: {amount} <= 0")

        self.__balance = self.__balance + Decimal(amount)
        return True

    @log_exc(exc=ValueError, return_value=False)
    def balance_sub(self, amount: Union[int, float]) -> bool:
        """
        Subtract an amount from the current account balance
        :param amount: Amount to be subtracted
        :return: True if successful else False
        """
        if amount <= 0:
            raise ValueError(f"Amount: {amount} <= 0")

        if amount > self.__balance:
            raise ValueError(f"Amount: {amount} > {self.balance}")

        self.__balance = self.__balance - Decimal(amount)
        return True

    def check_account_number(self, other_account_number: int):
        """
        Check if account number matches another account number
        :param other_account_number: The account number to be checked
        :return: True if equal else False
        """

        return self.account_number == other_account_number

    def to_json(self):
        return {"account_number": self.account_number, "balance": self.balance}

    def __eq__(self, other_account: Account):
        return (
            self.account_number == other_account.account_number
            and self.balance == other_account.balance
        )

    def __str__(self):
        return f"Account({self.account_number}, balance={self.balance})"

    def __repr__(self):
        return f"Account({self.account_number}, balance={self.balance})"
