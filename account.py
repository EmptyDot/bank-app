from __future__ import annotations

import logging
from decimal import Decimal, getcontext

import logger

getcontext()


class Account:
    def __init__(self, account_number: int, balance: int | float = 0):
        self.account_number = account_number
        self.__balance = Decimal(balance)

    @property
    def balance(self) -> float:
        """
        Get the balance to be presented to the user, not to be used for arithmetic operations.
        :return: Balance represented as a float with 2 decimals of precision
        """
        return float(round(self.__balance, 2))

    def balance_add(self, amount: int | float) -> bool:
        """
        Add an amount to the current account balance
        :param amount: Amount to be added
        :return: True if successful else False
        """
        if amount <= 0:
            logger.log_message(f"Amount: {amount} <= 0", logging.WARNING)
            return False

        self.__balance = self.__balance + Decimal(amount)
        return True

    def balance_sub(self, amount: int | float) -> bool:
        """
        Subtract an amount from the current account balance
        :param amount: Amount to be subtracted
        :return: True if successful else False
        """
        if amount <= 0:
            logger.log_message(f"Amount: {amount} <= 0", logging.WARNING)
            return False
        if amount > self.__balance:
            logger.log_message(f"Amount: {amount} > {self.balance}", logging.WARNING)
            return False

        self.__balance = self.__balance - Decimal(amount)
        return True

    def __eq__(self, other_account: Account):
        return (
            self.account_number == other_account.account_number
            and self.balance == other_account.balance
        )

    def __str__(self):
        return f"Account({self.account_number}, balance={self.balance})"

    def __repr__(self):
        return f"Account({self.account_number}, balance={self.balance})"
