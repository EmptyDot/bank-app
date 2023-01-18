from __future__ import annotations

import json
import logging
from json import JSONDecodeError
from os import PathLike
from typing import Union, Optional

from bank_app import logger
from .account import Account
from .customer import Customer
from .customer_parser import CustomerParser

AccountArgs = dict[str, Union[int, float]]

DEFAULT_FILE_PATH = "data/saved_customers.json"


class CustomerParserJson(CustomerParser):
    """
    Class used for data persistence
    """

    def load_customers(
        self, file_path: PathLike[str] = DEFAULT_FILE_PATH
    ) -> list[Customer] | None:
        """
        Load saved customers from the previous instance
        :param file_path: Path to file to load from
        :return: The list of Customers that was loaded
        """
        logger.log_message(f"Loading files from {file_path}", logging.INFO)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_str = file.read()
                customers_json = json.loads(json_str)
                customers = []
                for customer_json in customers_json:
                    customers.append(self.create_customer(**customer_json))

                return customers

        except FileNotFoundError as e:
            logger.log_exception(e)
        except OSError as e:
            logger.log_exception(e)
        except JSONDecodeError as e:
            logger.log_exception(e)

    @staticmethod
    def create_customer(
        name: str, password: str, accounts: list[AccountArgs]
    ) -> Customer:
        """
        Create a customer object
        """
        customer = Customer(name, password, hash_password=False)
        if accounts:
            for account_args in accounts:
                customer.add_account(Account(**account_args))
        return customer

    def save_customers(
        self, customers: list[Customer], file_path: PathLike[str] = DEFAULT_FILE_PATH
    ) -> bool:
        """
        Save a list of customers
        :param customers: The list of customers to be saved
        :param file_path: Path to save location
        :return: True if successful else False
        """
        if not customers:
            return False
        logger.log_message(f"Saving customers to {file_path}", logging.INFO)
        try:
            with open(file_path, "w", encoding="utf-8") as file:

                json_str = json.dumps(
                    [customer.to_json() for customer in customers],
                    indent=2,
                )
                file.write(json_str)
                return True
        except OSError as e:
            logger.log_message(f"{type(e).__name__}: {e}", logging.ERROR)

        return False
