from __future__ import annotations

import json

from account import Account
from customer import Customer
from parsing.parser import CustomerParser, AccountArgs


class CustomerParserJson(CustomerParser):
    def load_customers(self) -> list[Customer] | None:
        """
        Load saved customers from the previous instance
        :return: The list of Customers that was loaded
        """
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
    def create_customer(
        name: str, password: str, accounts: list[AccountArgs]
    ) -> Customer:
        customer = Customer(name, password)
        if accounts:
            for account_args in accounts:
                customer.add_account(Account(**account_args))
        return customer

    def save_customers(self, customers: list[Customer]) -> bool:
        """
        Save a list of customers
        :param customers: The list of customers to be saved
        :return: True if successful else False
        """
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
    def serialize_customer(customer: Customer) -> dict:
        """
        Turn a Customer object into a dict to be turned into json
        :param customer: Customer to be serialized
        :return: A dict containing the information about the cutomer
        """
        return {
            "name": customer.name,
            "password": customer.password,
            "accounts": [
                {"account_number": a.account_number, "balance": a.balance}
                for a in customer.accounts
            ],
        }
