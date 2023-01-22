from passlib.hash import bcrypt

from bank_app import logger
from .account import Account


class Customer:
    def __init__(self, name: str, password: str, hash_password: bool = True):
        self.name = name.lower()
        if hash_password:
            self.password = password
        else:
            self.__password = password

        self.accounts: list[Account] = []

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password: str):
        self.__password = bcrypt.using(rounds=13).hash(password)

    def check_name(self, other_name: str) -> bool:
        """
        Check if customer password matches another name (case-insensitive)
        :param other_name: The name to be checked
        :return: True if equal else False
        """
        return self.name == other_name.lower()

    def check_password(self, other_password: str) -> bool:
        """
        Check if customer password matches another password
        :param other_password: The password to be checked
        :return: True if equal else False
        """
        return bcrypt.verify(other_password, self.password)

    def add_account(self, account: Account) -> bool:
        """
        Add a new account to the customer
        :param account: The account to be added
        :return: True if successful else False
        """
        if isinstance(account, Account):
            self.accounts.append(account)
            return True
        logger.log_message(TypeError(f"Expected type Account, got {type(account)}"))
        return False

    def to_json(self):
        return {
            "name": self.name,
            "password": self.password,
            "accounts": [account.to_json() for account in self.accounts],
        }

    def __str__(self):
        return f"Customer({self.name}, {self.password}, accounts={self.accounts})"

    def __repr__(self):
        return f"Customer({self.name}, {self.password})"
