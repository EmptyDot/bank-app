from __future__ import annotations

import json

from account import Account
from customer import Customer
from parsing.parser import CustomerParser


class CustomerParserJson(CustomerParser):
    def load_customers(self) -> list[Customer] | None:
        customers = []
        try:
            with open("saved_customers.json", "r") as f:
                json_str = f.read()
                customers_json = json.loads(json_str)

                for customer_json in customers_json:
                    customers.append(self.create_customer(**customer_json))
                return customers
        except OSError:
            return

    @staticmethod
    def create_customer(name, password, accounts) -> Customer:
        customer = Customer(name, password)
        for account in accounts:
            customer.add_account(Account(**account))
        return customer

    def save_customers(self, customers: list[Customer]) -> bool:
        try:
            with open("saved_customers.json", "w") as f:

                json_str = json.dumps(
                    [self.serialize_customer(customer) for customer in customers],
                )
                f.write(json_str)
                return True
        except OSError:
            return False

    @staticmethod
    def serialize_customer(customer: Customer):
        return {
            "name": customer.name,
            "password": customer.password,
            "accounts": [
                {"account_number": a.account_number, "balance": a.balance}
                for a in customer.accounts
            ],
        }

