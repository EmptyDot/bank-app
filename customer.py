from account import Account


class Customer:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.accounts: list[Account] = []

    def check_password(self, other) -> bool:
        pass

    def add_account(self, account: Account):
        pass
