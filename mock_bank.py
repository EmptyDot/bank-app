from bank import Bank
from customer import Customer


class MockBank(Bank):
    """
    Only intended for testing. Allows initialization of bank with customers passed as an argument.
    """
    def __init__(self, customers: list[Customer]):
        super().__init__()
        self.customers = customers



