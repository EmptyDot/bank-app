import json
import logging
from json import JSONDecodeError
from typing import Optional, Union

from bank_app import logger
from .account import Account
from .customer import Customer
from .logger import log_exc

DEFAULT_FILE_PATH = "bank_app/data/saved_customers.json"


@log_exc(exc=(FileNotFoundError, OSError, JSONDecodeError), return_value=None)
def load_customers(
    file_path: Optional[str] = None,
) -> Optional[list[Customer]]:
    """
    Load saved customers from the previous instance
    :param file_path: Path to file to load from
    :return: The list of Customers that was loaded
    """
    file_path = file_path if file_path else DEFAULT_FILE_PATH

    with open(file_path, "r", encoding="utf-8") as file:
        json_str = file.read()
        customers_json = json.loads(json_str)
        customers = []
        for customer_json in customers_json:
            customers.append(create_customer(**customer_json))

        return customers


def create_customer(
    name: str, password: str, accounts: list[dict[str, Union[int, float]]]
) -> Customer:
    """
    Create a customer object
    """
    customer = Customer(name, password, hash_password=False)
    if accounts:
        for account_args in accounts:
            customer.add_account(Account(**account_args))

    return customer


@log_exc(exc=OSError, return_value=False)
def save_customers(customers: list[Customer], file_path: Optional[str] = None) -> bool:
    """
    Save a list of customers
    :param customers: The list of customers to be saved
    :param file_path: Path to save location
    :return: True if successful else False
    """
    if not customers:
        return False
    file_path = file_path if file_path else DEFAULT_FILE_PATH

    with open(file_path, "w", encoding="utf-8") as file:
        json_str = json.dumps(
            [customer.to_json() for customer in customers],
            indent=2,
        )
        file.write(json_str)
        return True


