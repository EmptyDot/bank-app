import atexit

from bank_app import parser_json
from bank_app.account import Account
from bank_app.bank import Bank
from bank_app.customer import Customer


def get_bank(customers: list[Customer] = None):
    customers = customers if customers else []
    return Bank(customers, save_on_exit=False)


class TestBank:
    def test_save_on_exit(self, tmp_path):
        Bank(save_on_exit=True, save_file_path=tmp_path)
        funcs = []

        class Capture:
            def __eq__(self, other):
                funcs.append(other)
                return False

        c = Capture()
        atexit.unregister(c)
        assert funcs[-1] == parser_json.save_customers

    def test_load_customers(self):
        bank = get_bank()
        assert bank.load_customers("tests/data/test_saved_customers_load.json")
        assert len(bank.customers) > 0

    def test_load_customers_wrong_file(self, tmp_path):
        bank = get_bank()
        assert bank.load_customers(tmp_path / "empty.json") is False

    def test_save_customers(self, tmp_path):
        customers = [Customer("Bob", "123"), Customer("Alice", "456")]
        bank = get_bank(customers)
        file_path = tmp_path / "test_saved_customers.json"
        assert bank.save_customers(file_path)

    def test_save_customers_no_customers(self):
        bank = get_bank()
        assert bank.save_customers() is False

    def test_get_customers(self):
        customers = [Customer("Bob", "123"), Customer("Alice", "456")]
        bank = get_bank(customers)
        assert bank.get_customers() == customers

    def test_add_customer(self):
        bank = get_bank()
        name, password = "Bob", "123"
        assert bank.add_customer(name, password)
        assert len(bank.customers) == 1
        c = bank.customers[0]
        assert c.check_name(name) and c.check_password(password)

    def test_add_customer_non_unique(self):
        bank = get_bank()
        name, password = "Bob", "123"
        assert bank.add_customer(name, password)
        assert bank.add_customer(name, password) is False
        assert len(bank.customers) == 1
        c = bank.customers[0]
        assert c.check_name(name) and c.check_password(password)

    def test_add_customer_wrong_type(self):
        bank = get_bank()
        assert bank.add_customer(["bob"], 123) is False
        assert len(bank.customers) == 0

    def test_get_customer(self):
        name, password = "Bob", "123"
        bank = get_bank([Customer(name, password)])
        c = bank.get_customer("Bob")
        assert c is not None
        assert c.check_name(name) and c.check_password("123")

    def test_get_customer_fail(self):
        bank = get_bank()
        assert bank.get_customer("Bob") is None

    def test_change_customer_password(self):
        bank = get_bank([Customer("Bob", "123"), Customer("Alice", "456")])
        assert bank.change_customer_password("Bob", "789")
        assert bank.customers[0].check_password("789")

    def test_change_customer_password_fail(self):
        bank = get_bank([Customer("Bob", "123")])
        assert bank.change_customer_password("Alice", "789") is False

    def test_remove_customer(self):
        bank = get_bank([Customer("Bob", "123"), Customer("Alice", "456")])
        bob = bank.customers[0]
        assert bob in bank.customers
        assert bank.remove_customer("Bob")
        assert len(bank.customers) == 1
        assert bob not in bank.customers

    def test_remove_customer_fail(self):
        bank = get_bank([Customer("Bob", "123")])
        assert bank.remove_customer("Alice") is False
        assert len(bank.customers) == 1

    def test_remove_customer_logged_in(self):
        bank = get_bank([Customer("Bob", "123"), Customer("Alice", "456")])
        bob = bank.customers[0]
        bank.current_user = bob
        assert bob in bank.customers
        assert bank.remove_customer("Bob")
        assert len(bank.customers) == 1
        assert bob not in bank.customers
        assert bank.current_user is None

    def test_login(self):
        name, password = "Bob", "123"
        bank = get_bank([Customer(name, password)])
        assert bank.login("Bob", "123")
        assert bank.current_user.check_name(
            name.lower()
        ) and bank.current_user.check_password("123")

    def test_login_wrong_password(self):
        bank = get_bank([Customer("Bob", "123")])
        assert bank.login("Bob", "bad_password") is False
        assert bank.current_user is None

    def test_login_wrong_name(self):
        bank = get_bank([Customer("Bob", "123")])
        assert not bank.login("Alice", "123")
        assert bank.current_user is None

    def test_logout(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.logout()
        assert bank.current_user is None

    def test_logout_fail(self):
        bank = get_bank()
        assert bank.logout() is False

    def test_get_accounts(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert type(bank.get_accounts()) == list

    def test_get_accounts_fail(self):
        bank = get_bank()
        assert bank.get_accounts() is None

    def test_add_account(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.add_account(1101000)
        assert bank.add_account(1101001)
        assert len(bank.current_user.accounts) == 2

    def test_add_account_no_user(self):
        bank = get_bank()
        assert bank.add_account(1101000) is False

    def test_add_account_non_unique(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.add_account(1)
        assert bank.add_account(1) is False
        assert len(bank.current_user.accounts) == 1

    def test_add_account_wrong_type(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.add_account("1101000") is False
        assert len(bank.current_user.accounts) == 0

    def test_remove_account(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1), Account(2)]
        assert bank.remove_account(1)
        assert len(bank.current_user.accounts) == 1

    def test_remove_account_no_user(self):
        bank = get_bank()
        assert bank.remove_account(1) is False

    def test_remove_account_no_account(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.remove_account(1) is False
        assert len(bank.current_user.accounts) == 0

    def test_get_account(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1), Account(2)]
        acc = bank.get_account(1)
        assert acc is not None
        assert acc.account_number == 1

    def test_get_account_no_user(self):
        bank = get_bank()
        assert bank.get_account(1) is None

    def test_get_account_no_accounts(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.get_account(1) is None

    def test_get_account_wrong_account_number(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1), Account(2)]
        assert bank.get_account(3) is None

    def test_deposit_int(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1)]
        assert bank.deposit(1, 100)
        assert bank.current_user.accounts[0].balance == 100

    def test_deposit_float(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1)]
        assert bank.deposit(1, 1.23456789)
        assert bank.current_user.accounts[0].balance == 1.23

    def test_deposit_negative(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert bank.deposit(1, -100) is False
        assert bank.current_user.accounts[0].balance == 100

    def test_deposit_no_user(self):
        bank = get_bank()
        assert bank.deposit(1, 100) is False

    def test_deposit_wrong_type(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1)]
        assert bank.deposit(1, "100") is False
        assert bank.current_user.accounts[0].balance == 0

    def test_deposit_no_accounts(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert not bank.deposit(1, 100)

    def test_deposit_wrong_account_number(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1), Account(2)]
        assert bank.deposit(3, 100) is False

    def test_withdraw_int(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert bank.withdraw(1, 1)
        assert bank.current_user.accounts[0].balance == 99

    def test_withdraw_float(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert bank.withdraw(1, 0.1)
        assert bank.current_user.accounts[0].balance == 99.9

    def test_withdraw_negative(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert bank.withdraw(1, -100) is False
        assert bank.current_user.accounts[0].balance == 100

    def test_withdraw_negative_no_user(self):
        bank = get_bank()
        assert bank.withdraw(1, 100) is False

    def test_withdraw_no_accounts(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.withdraw(1, 100) is False

    def test_withdraw_wrong_account_number(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1)]
        assert bank.withdraw(3, 100) is False

    def test_withdraw_wrong_type(self):
        bank = get_bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert bank.withdraw(1, "1") is False
        assert bank.current_user.accounts[0].balance == 100

    def test_to_json(self):
        customers = [Customer("Bob", "123"), Customer("Alice", "456")]
        customers[0].accounts = [Account(1, 123.4), Account(2, 456)]
        bank = get_bank(customers)
        bank.current_user = customers[0]
        assert bank.to_json() == {
            "customers": [customer.to_json() for customer in bank.customers],
            "current_user": customers[0].to_json(),
        }

    def test___str__(self):
        customer = Customer("Bob", "123")
        bank = get_bank([customer])
        assert str(bank) == f"Bank({[customer]}, current_user=None)"

    def test___str__logged_in(self):
        customer = Customer("Bob", "123")
        bank = get_bank([customer])
        bank.current_user = customer
        assert str(bank) == f"Bank({[customer]}, current_user={customer})"

    def test___repr__(self):
        customers = [Customer("Bob", "123"), Customer("Alice", "456")]
        bank = get_bank(customers)
        assert repr(bank) == f"Bank({customers}, current_user=None)"

    def test___repr__logged_in(self):
        customers = [Customer("Bob", "123"), Customer("Alice", "456")]
        bank = get_bank(customers)

        bank.current_user = customers[0]
        assert repr(bank) == f"Bank({customers}, current_user={customers[0]})"
