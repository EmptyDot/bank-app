from __future__ import annotations

from pydantic import BaseModel


class Bank(BaseModel):
    customers: list[Customer] = []
    current_user: Customer | None = None

    def to_json(self):
        return {
            "customers": [customer.to_json() for customer in self.customers],
            "current_user": self.current_user.to_json()
            if type(self.current_user) == Customer
            else "",
        }


class Customer(BaseModel):
    name: str
    password: str
    accounts: list[Account] = []

    def to_json(self):
        return {
            "name": self.name,
            "password": self.password,
            "accounts": [account.to_json() for account in self.accounts],
        }


class Account(BaseModel):
    account_number: int
    balance: int | float

    def to_json(self):
        return {"account_number": self.account_number, "balance": self.balance}
