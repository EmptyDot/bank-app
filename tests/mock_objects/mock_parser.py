from typing import Optional

from account import Account
from customer import Customer
from customer_parser import CustomerParser


class MockParser(CustomerParser):
    def load_customers(self, file_path: Optional[str] = "") -> list[Customer]:
        customers = []
        bob = Customer("bob", "123")
        bob.accounts = [Account(1, 450.1), Account(2, 10.145)]
        customers.append(bob)
        alice = Customer("alice", "456")
        alice.accounts = [Account(3, 252.5), Account(4, 19191.63)]
        customers.append(alice)
        return customers

    def save_customers(self, customers: list[Customer], file_path: Optional[str] = "") -> bool:
        return bool(customers)

