from account import Account


class Customer:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.accounts: list[Account] = []

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
        return False
