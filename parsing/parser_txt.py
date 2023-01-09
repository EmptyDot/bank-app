from __future__ import annotations

from typing import Optional, Union

from account import Account
from customer import Customer
from parsing.parser import CustomerParser, AccountArgs


class CustomerParserTxt(CustomerParser):
    def load_customers(self) -> list[Customer] | None:
        """
        Load saved customers from the previous instance
        :return: The list of Customers that was loaded
        """
        customers = []
        try:
            with open("saved_customers.txt", "r") as f:
                for line in f.readlines():
                    if customer := self.parse_str(line):
                        customers.append(customer)
            return customers
        except OSError:
            return

    def parse_str(self, customer_str: str) -> Customer | None:
        customer_str = customer_str.rstrip("\n")
        if customer_str.count("#") == 1:
            # At least one account
            customer_info, accounts_str = customer_str.split("#")
            accounts = self.parse_accounts(accounts_str)
            if customer_tuple := self.parse_customer(customer_info):
                name, password = customer_tuple
                return self.create_customer(name, password, accounts)

        elif customer_tuple := self.parse_customer(customer_str):
            # No accounts
            name, password = customer_tuple
            return self.create_customer(name, password)

    @staticmethod
    def parse_customer(customer_info) -> tuple[str, str] | None:
        if customer_info.count("/") == 1:
            name, password = customer_info.split("/")
            return name, password

    def parse_accounts(self, accounts_str: str) -> list[AccountArgs]:
        accounts = []
        if "@" in accounts_str:
            # More than one account
            for account_info in accounts_str.split("@"):
                if account := self.parse_account(account_info):
                    accounts.append(account)
        else:
            # Only one account
            if account := self.parse_account(accounts_str):
                accounts.append(account)

        return accounts

    @staticmethod
    def parse_account(account_info: str) -> AccountArgs | None:
        if account_info.count("/") == 1:
            account_number, balance = account_info.split("/")
            try:
                return {
                    "account_number": int(account_number),
                    "balance": float(balance),
                }
            except ValueError:
                pass

    @staticmethod
    def create_customer(
        name: str, password: str, accounts: Optional[list[AccountArgs]] = None
    ) -> Customer:
        customer = Customer(name, password)
        if accounts:
            for account in accounts:
                customer.add_account(Account(**account))
        return customer

    def save_customers(self, customers: list[Customer]) -> bool:
        """
        Save a list of customers
        :param customers: The list of customers to be saved
        :return: True if successful else False
        """
        try:
            with open("saved_customers.txt", "w") as f:
                for customer in customers:
                    customer_str = self.get_customer_str(customer)
                    f.write(customer_str)
            return True
        except OSError:
            return False

    @staticmethod
    def get_customer_str(customer: Customer):
        """
        Create a formatted string out of a customer object
        :param customer: Customer to be converted
        :return: The formatted string
        """
        if customer.accounts:
            return f"{customer.name}/{customer.password}#{'@'.join([f'{account.account_number}/{account.balance}' for account in customer.accounts])}\n"
        return f"{customer.name}/{customer.password}\n"


if __name__ == "__main__":
    c = CustomerParserTxt().load_customers()
    for i in c:
        print(i)
