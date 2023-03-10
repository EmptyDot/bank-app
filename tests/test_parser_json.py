from passlib.hash import bcrypt

from bank_app import parser_json
from bank_app.account import Account
from bank_app.customer import Customer


def get_customer_list():
    customers = []
    bob = Customer("Bob", "123")
    bob.accounts = [Account(1, 200), Account(2, 41515.24)]
    customers.append(bob)
    alice = Customer("Alice", "123")
    alice.accounts = [Account(3, 300), Account(4, 1.224)]
    customers.append(alice)
    return customers


def test_load_customers():
    customers = parser_json.load_customers("tests/data/test_saved_customers_load.json")
    assert isinstance(customers, list)
    assert all(isinstance(customer, Customer) for customer in customers)


def test_load_customers_wrong_file(tmp_path):
    assert parser_json.load_customers(tmp_path / "wrong_file.json") is None


def test_load_customers_empty_file(tmp_path):
    open(tmp_path / "empty.json", "a").close()
    assert parser_json.load_customers(tmp_path / "empty.json") is None


def test_load_customers_os_error(tmp_path):
    isdir = tmp_path / "isdir"
    isdir.mkdir()
    assert parser_json.load_customers(isdir) is None


def test_create_customer():
    name, password = "Bob", "123"
    acc1_num, acc1_balance = 1, 200
    acc2_num, acc2_balance = 2, 41515.24
    accounts = [
        {"account_number": acc1_num, "balance": acc1_balance},
        {"account_number": acc2_num, "balance": acc2_balance},
    ]
    hashed_password = bcrypt.using(rounds=13).hash(password)
    customer = parser_json.create_customer(name, hashed_password, accounts)
    assert customer.check_name(name)
    assert customer.check_password(password)
    assert all(
        customer.accounts[idx].account_number == account["account_number"]
        and customer.accounts[idx].balance == account["balance"]
        for idx, account in enumerate(accounts)
    )


def test_save_customers(tmp_path):
    customers = get_customer_list()
    assert parser_json.save_customers(customers, tmp_path / "test_saved_customers.json")


def test_save_customers_no_customers(tmp_path):
    assert (
        parser_json.save_customers([], tmp_path / "test_saved_customers.json") is False
    )


def test_save_customers_no_accounts(tmp_path):
    assert parser_json.save_customers(
        [Customer("Bob", "123")], tmp_path / "test_saved_customers.json"
    )


def test_save_customers_os_error(tmp_path):
    isdir = tmp_path / "isdir"
    isdir.mkdir()
    customers = get_customer_list()
    assert parser_json.save_customers(customers, isdir) is False
