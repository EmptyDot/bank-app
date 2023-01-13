import logger
from account import Account


class Customer:
    def __init__(self, name: str, password: str):
        self.name = name.lower()
        self.password = password
        self.accounts: list[Account] = []

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
        return self.password == other_password

    def add_account(self, account: Account) -> bool:
        """
        Add a new account to the customer
        :param account: The account to be added
        :return: True if successful else False
        """
        if isinstance(account, Account):
            self.accounts.append(account)
            return True
        logger.log_exception(
            TypeError(f"Expected type Account, got {type(account)}")
        )
        return False

    def __eq__(self, other):
        return (
            isinstance(other, Customer)
            and self.name == other.name
            and self.password == other.password
            and self.accounts == other.accounts
        )

    def __str__(self):
        return f"Customer({self.name}, {self.password}, accounts={self.accounts})"

    def __repr__(self):
        return f"Customer({self.name}, {self.password})"
