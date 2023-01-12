from __future__ import annotations

from typing import Optional
import atexit

from account import Account
from customer import Customer
from customer_parser import CustomerParser
from parser_json import CustomerParserJson



class Bank:
    def __init__(
        self, save_on_exit: bool = True, parser: CustomerParser = CustomerParserJson()
    ):
        self.customers: list[Customer] = []
        self.current_user: Optional[Customer] = None
        self.__parser = parser

        if save_on_exit:
            atexit.register(self.__parser.save_customers, self.customers)

    def load_customers(self) -> bool:
        """
        Load the saved customers
        :return: True if successful else False
        """
        if customers := self.__parser.load_customers():
            self.customers.extend(customers)
            return True
        return False

    def get_customers(self) -> list[Customer]:
        """
        List all customers
        :return: The list of customers
        """
        return self.customers

    def add_customer(self, name: str, password: str) -> bool:
        """
        Add a new customer
        :param name: Username of the customer. Should be unique.
        :param password: Password of the customer
        :return: True if successful else False
        """

        if all(not customer.check_name(name) for customer in self.customers)\
                and isinstance(name, str) and isinstance(password, str):

            customer = Customer(name, password)
            self.customers.append(customer)
            return True

        return False

    def get_customer(self, name: str) -> Customer | None:
        """
        Get a customer by name
        :param name: Username of a customer
        :return: The customer matching the name
        """
        for customer in self.customers:
            if customer.check_name(name):
                return customer

    def change_customer_password(self, name: str, new_password: str) -> bool:
        """
        Change a customers password
        :param name: Name of the customer
        :param new_password: The new password
        :return: True if successful else False
        """

        if customer := self.get_customer(name):
            customer.password = new_password
            return True
        return False

    def remove_customer(self, name: str) -> bool:
        """
        Remove a customer
        :param name: Name of the customer
        :return: True if successful else False
        """
        if customer := self.get_customer(name):
            self.customers.remove(customer)
            if self.current_user == customer:
                self.logout()
            return True
        return False

    def login(self, name: str, password: str) -> bool:
        """
        If the password matches, add this customer from the list of customers as the new logged in customer.
        :param name: Name of the customer
        :param password: Password of the customer
        :return: True if successful else False
        """
        if customer := self.get_customer(name):
            if customer.check_password(password):
                self.current_user = customer
                return True
        return False

    def logout(self) -> bool:
        """
        Log out the currently logged in customer
        :return: True if successful else False
        """
        if self.current_user:
            self.current_user = None
            return True
        return False

    def get_accounts(self) -> list[Account] | None:
        """
        Get all accounts that belong to the currently logged in customer
        :return: The list of accounts
        """
        if self.current_user:
            return self.current_user.accounts

    def add_account(self, account_number: int) -> bool:
        """
        Add an account to the currently logged in customer.
        :param account_number: Account number of the new account.
        :return: True if successful else False
        """
        if self.current_user:
            if all(
                user_account.account_number != account_number
                for user_account in self.current_user.accounts
            ) and isinstance(account_number, int):
                acc = Account(account_number)
                return self.current_user.add_account(acc)
        return False

    def remove_account(self, account_number: int) -> bool:
        """
        Remove an account from the currently logged in customer.
        :param account_number: Account number of the account.
        :return: True if successful else False
        """
        if account := self.get_account(account_number):
            self.current_user.accounts.remove(account)
            return True
        return False

    def get_account(self, account_number: int) -> Account | None:
        """
        Get an account from the currently logged in customer.
        :param account_number: Account number of the account.
        :return: The account matching the account number.
        """
        if accounts := self.get_accounts():
            for account in accounts:
                if account.account_number == account_number:
                    return account

    def deposit(self, account_number: int, amount: int | float) -> bool:
        """
        Deposit money to an account.
        :param account_number: Account number of the account.
        :param amount: The amount to be added.
        :return: True if successful else False
        """
        if isinstance(amount, (int, float)):
            if account := self.get_account(account_number):
                return account.balance_add(amount)

        return False

    def withdraw(self, account_number: int, amount: int | float) -> bool:
        """
        Withdraw money from an account.
        :param account_number: Account number of the account.
        :param amount: The amount to be subtracted.
        :return: True if successful else False
        """
        if isinstance(amount, (int, float)):
            if account := self.get_account(account_number):
                return account.balance_sub(amount)

        return False

    def __str__(self):
        return f"Bank({self.get_customers()}, current_user={self.current_user})"

    def __repr__(self):
        return f"Bank({self.get_customers()}, current_user={self.current_user})"
