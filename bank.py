from __future__ import annotations

from typing import Optional

from account import Account
from customer import Customer


class Bank:
    def __init__(self):
        self.customers: list[Customer] = []
        self.current_user: Optional[Customer] = None

    def get_customers(self) -> list[Customer]:
        pass

    def add_customer(self, name: str, password: str) -> bool:
        pass

    def get_customer(self, name: str) -> Customer | None:
        pass

    def remove_customer(self) -> bool:
        pass

    def change_customer_password(self, name: str, new_password: str) -> bool:
        pass

    def login(self, name: str, password: str) -> bool:
        pass

    def logout(self) -> bool:
        pass

    def get_accounts(self) -> list[Account]:
        pass

    def add_account(self, account_number: int) -> bool:
        pass

    def remove_account(self, account_number: int) -> bool:
        pass

    def get_account(self, account_number: int) -> Account | None:
        pass

    def deposit(self, account_number: int, amount: int | float) -> bool:
        pass

    def withdraw(self, account_number: int, amount: int | float) -> bool:
        pass
