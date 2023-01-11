from typing import Optional

from bank import Bank
from customer import Customer
from mock_parser import MockParser


class MockBank(Bank):
    def __init__(self, customers: list[Customer]):
        super().__init__(save_on_exit=False, parser=MockParser())
        self.customers = customers
        self.current_user: Optional[Customer] = None


