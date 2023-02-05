import atexit
import logging
from typing import Union, Optional

from bank_app import parser_json
from .account import Account
from .customer import Customer
from .exceptions import CustomerNotFoundError
from .logger import log_exc


class Bank:
    def __init__(
            self,
            customers: Optional[list[Customer]] = None,
            save_on_exit: bool = True,
            save_file_path: Optional[str] = None,
    ):
        self.customers: list[Customer] = customers if customers else []
        self.current_user: Optional[Customer] = None

        if save_on_exit:
            atexit.register(parser_json.save_customers, self.customers, save_file_path)

    @log_exc(exc=OSError, return_value=False)
    def load_customers(self, file_path: Optional[str] = None) -> bool:
        """
        Load the saved customers
        :param file_path: Path to the file to load from
        :return: True if successful else False
        """
        if customers := parser_json.load_customers(file_path):
            self.customers.extend(customers)
            return True

        raise OSError("Failed to load customers")

    def save_customers(self, save_file_path: Optional[str] = None) -> bool:
        return parser_json.save_customers(self.customers, save_file_path)

    def get_customers(self) -> list[Customer]:
        """
        List all customers
        :return: The list of customers
        """
        return self.customers

    @log_exc(exc=(TypeError, ValueError), return_value=False)
    def add_customer(self, name: str, password: str) -> bool:
        """
        Add a new customer
        :param name: Username of the customer. Should be unique.
        :param password: Password of the customer
        :return: True if successful else False
        """

        if any(customer.check_name(name) for customer in self.customers):
            raise ValueError(f"Customer with name {name} already exists.")

        if not isinstance(name, str) or not isinstance(password, str):
            raise TypeError(
                f"Expected type (str, str), got ({type(name)}, {type(password)})"
            )

        customer = Customer(name, password)
        self.customers.append(customer)
        return True

    @log_exc(exc=CustomerNotFoundError, return_value=None)
    def get_customer(self, name: str) -> Optional[Customer]:
        """
        Get a customer by name
        :param name: Username of a customer
        :return: The customer matching the name
        """
        for customer in self.customers:
            if customer.check_name(name):
                return customer

        raise CustomerNotFoundError(f"Customer of name {name} not found")

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

    @log_exc(exc=ValueError, return_value=False)
    def login(self, name: str, password: str) -> bool:
        """
        If the password matches,
        add this customer from the list of customers
        as the new logged in customer.

        :param name: Name of the customer
        :param password: Password of the customer
        :return: True if successful else False
        """
        if customer := self.get_customer(name):
            if customer.check_password(password):
                self.current_user = customer
                return True
            raise ValueError("Incorrect password")
        return False

    @log_exc(exc=CustomerNotFoundError, return_value=False)
    def logout(self) -> bool:
        """
        Log out the currently logged in customer
        :return: True if successful else False
        """
        if not self.current_user:
            raise CustomerNotFoundError("No customer is logged in")

        self.current_user = None
        return True

    @log_exc(exc=CustomerNotFoundError, return_value=None)
    def get_accounts(self) -> Optional[list[Account]]:
        """
        Get all accounts that belong to the currently logged in customer
        :return: The list of accounts
        """
        if not self.current_user:
            raise CustomerNotFoundError("No customer is logged in")

        return self.current_user.accounts

    @log_exc(exc=(CustomerNotFoundError, ValueError, TypeError), return_value=False)
    def add_account(self, account_number: int) -> bool:
        """
        Add an account to the currently logged in customer.
        :param account_number: Account number of the new account.
        :return: True if successful else False
        """
        if not self.current_user:
            raise CustomerNotFoundError("No customer is logged in", logging.WARNING)

        if any(
                user_account.check_account_number(account_number)
                for user_account in self.current_user.accounts
        ):
            raise ValueError(
                f"Customer has no account with account number {account_number}"
            )

        if not isinstance(account_number, int):
            raise TypeError(f"Expected type int, got {type(account_number)}")

        acc = Account(account_number)
        return self.current_user.add_account(acc)

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

    @log_exc(exc=ValueError, return_value=None)
    def get_account(self, account_number: int) -> Optional[Account]:
        """
        Get an account from the currently logged in customer.
        :param account_number: Account number of the account.
        :return: The account matching the account number.
        """
        if accounts := self.get_accounts():
            for account in accounts:
                if account.check_account_number(account_number):
                    return account
            raise ValueError(f"Account with account number {account_number} not found.")
        return None

    @log_exc(exc=TypeError, return_value=False)
    def deposit(self, account_number: int, amount: Union[int, float]) -> bool:
        """
        Deposit money to an account.
        :param account_number: Account number of the account.
        :param amount: The amount to be added.
        :return: True if successful else False
        """
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Expected type (int | float), got {type(amount)}")

        if account := self.get_account(account_number):
            return account.balance_add(amount)

        return False

    @log_exc(exc=TypeError, return_value=False)
    def withdraw(self, account_number: int, amount: Union[int, float]) -> bool:
        """
        Withdraw money from an account.
        :param account_number: Account number of the account.
        :param amount: The amount to be subtracted.
        :return: True if successful else False
        """
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Expected type (int | float), got {type(amount)}")

        if account := self.get_account(account_number):
            return account.balance_sub(amount)

        return False

    def to_json(self) -> dict:
        """
        Convert the object to json format
        :return: dict in json format that represents the object
        """
        return {
            "customers": [customer.to_json() for customer in self.customers],
            "current_user": self.current_user.to_json()
            if isinstance(self.current_user, Customer)
            else "",
        }

    def __str__(self):
        return (
            f"Bank("
            f"{self.get_customers()}, "
            f"current_user={self.current_user}"
            f")"
        )

    def __repr__(self):
        return (
            f"Bank("
            f"{self.get_customers()}, "
            f"current_user={self.current_user}"
            f")"
        )
