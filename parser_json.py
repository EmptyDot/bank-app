from __future__ import annotations

import json
from json import JSONDecodeError
from typing import Union, Optional

from account import Account
from customer import Customer
from customer_parser import CustomerParser
from logger import get_logger, log_message

AccountArgs = dict[str, Union[int, float]]

DEFAULT_FILE_PATH = "data/saved_customers.json"

logger = get_logger()


class CustomerParserJson(CustomerParser):
    """
    Class used for data persistence
    """

    def load_customers(
        self, file_path: Optional[str] = DEFAULT_FILE_PATH
    ) -> list[Customer] | None:
        """
        Load saved customers from the previous instance
        :param file_path: Path to file to load from
        :return: The list of Customers that was loaded
        """

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_str = file.read()
                customers_json = json.loads(json_str)
                customers = []
                for customer_json in customers_json:
                    customers.append(self.create_customer(**customer_json))

                return customers

        except FileNotFoundError:
            logger.error(log_message("FileNotFoundError"))
        except OSError as exc:
            logger.error(log_message(exc.__class__.__name__))
        except JSONDecodeError:
            logger.error(log_message("JSONDecodeError"))

    @staticmethod
    def create_customer(
        name: str, password: str, accounts: list[AccountArgs]
    ) -> Customer:
        """
        Create a customer object
        """
        customer = Customer(name, password)
        if accounts:
            for account_args in accounts:
                customer.add_account(Account(**account_args))
        return customer

    def save_customers(
        self, customers: list[Customer], file_path: Optional[str] = DEFAULT_FILE_PATH
    ) -> bool:
        """
        Save a list of customers
        :param customers: The list of customers to be saved
        :param file_path: Path to save location
        :return: True if successful else False
        """
        if not customers:
            return False

        try:
            with open(file_path, "w", encoding="utf-8") as file:

                json_str = json.dumps(
                    [self.serialize_customer(customer) for customer in customers],
                    indent=2,
                )
                file.write(json_str)
                return True
        except OSError as exc:
            logger.error(log_message(exc.__class__.__name__))

        return False

    @staticmethod
    def serialize_customer(customer: Customer) -> dict:
        """
        Turn a Customer object into a dict to be turned into json
        :param customer: Customer to be serialized
        :return: A dict containing the information about the customer
        """
        return {
            "name": customer.name,
            "password": customer.password,
            "accounts": [
                {"account_number": a.account_number, "balance": a.balance}
                for a in customer.accounts
            ],
        }
