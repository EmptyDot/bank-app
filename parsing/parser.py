from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from customer import Customer

AccountArgs = dict[str, Union[int, float]]


class CustomerParser(ABC):
    @abstractmethod
    def load_customers(self) -> list[Customer] | None:
        """
        Load saved customers from the previous instance
        :return: The list of Customers that was loaded
        """
        pass

    @abstractmethod
    def save_customers(self, customers: list[Customer]) -> bool:
        """
        Save a list of customers
        :param customers: The list of customers to be saved
        :return: True if successful else False
        """
        pass
