
from account import Account
from customer import Customer
from parsing.parser import CustomerParser


class MockParser(CustomerParser):
    def load_customers(self) -> list[Customer]:
        customers = []
        bob = Customer("bob", "123")
        bob.accounts = [Account(1, 450.1), Account(2, 10.145)]
        customers.append(bob)
        alice = Customer("alice", "456")
        alice.accounts = [Account(3, 252.5), Account(4, 19191.63)]
        customers.append(alice)
        return customers

    def save_customers(self, customers: list[Customer]) -> bool:
        return True

