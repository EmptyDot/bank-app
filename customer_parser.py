from __future__ import annotations

from abc import ABC, abstractmethod


from customer import Customer




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
