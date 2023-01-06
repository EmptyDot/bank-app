from customer import Customer
from account import Account

FILE_PATH = "saved_customers.txt"


def parse_customers_txt() -> list[Customer]:
    """
    Read from a txt file and create customers
    :return: A list of Customers
    """
    with open(FILE_PATH, "r") as f:
        customers = []
        for line in f.readlines():
            line = line.rstrip("\n")
            customer_info, accounts = line.split("#")
            name, password = customer_info.split("/")
            this_customer = Customer(name, password)
            for account_info in accounts.split("@"):
                account_number, balance = account_info.split("/")
                this_customer.add_account(Account(account_number, balance))
            customers.append(this_customer)
        return customers


def save_customers(customers: list[Customer]):
    """
    Save a list of customers to a txt file
    :param customers: The list of customers to saved
    """
    with open(FILE_PATH, "w") as f:
        for customer in customers:
            accounts_str = "@".join(
                [
                    f"{account.account_number}/{account.balance}"
                    for account in customer.accounts
                ]
            )
            customer_str = f"{customer.name}/{customer.password}"
            f.write(f"{customer_str}#{accounts_str}\n")



