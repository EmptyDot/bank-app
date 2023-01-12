from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from customer import Customer


class CustomerParser(ABC):
    @abstractmethod
    def load_customers(self, file_path: Optional[str] = "") -> list[Customer] | None:
        """
        Load saved customers from the previous instance
        :param file_path: Path to file to load from
        :return: The list of Customers that was loaded
        """
        pass

    @abstractmethod
    def save_customers(self, customers: list[Customer], file_path: Optional[str] = "") -> bool:
        """
        Save a list of customers
        :param customers: The list of customers to be saved
        :param file_path: Path to save location
        :return: True if successful else False
        """
        pass
