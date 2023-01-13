from typing import Optional

from bank import Bank
from customer import Customer
from tests.mock_objects.mock_parser import MockParser


class MockBank(Bank):
    def __init__(self, customers: list[Customer], save_on_exit: bool):
        super().__init__(save_on_exit=save_on_exit, parser=MockParser())
        self.customers = customers
