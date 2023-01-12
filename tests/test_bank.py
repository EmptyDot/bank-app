from bank import Bank

from customer import Customer
from account import Account
from mock_bank import MockBank


class TestBank:
    def test_get_customers(self):
        customers = [Customer("Bob", "123"), Customer("Alice", "456")]
        bank = MockBank(customers)
        assert bank.get_customers() == customers

    def test_add_customer(self):
        bank = Bank()
        name, password = "Bob", "123"
        assert bank.add_customer(name, password)
        assert len(bank.customers) == 1
        assert bank.customers[-1] == Customer(name, password)

    def test_add_customer_non_unique(self):
        bank = Bank()
        name, password = "Bob", "123"
        c = Customer(name, password)
        assert bank.add_customer(name, password)
        assert not bank.add_customer(name, password)
        assert len(bank.customers) == 1
        assert bank.customers[-1] == c

    def test_add_customer_wrong_type(self):
        bank = Bank()
        name, password = ["bob"], 123
        assert bank.add_customer(name, password) is False
        assert len(bank.customers) == 0

    def test_get_customer(self):
        bank = MockBank([Customer("Bob", "123"), Customer("Alice", "456")])
        c = bank.get_customer("Bob")
        bob = Customer("Bob", "123")
        assert c is not None
        assert bob == c

    def test_get_customer_fail(self):
        bank = Bank()
        assert bank.get_customer("Bob") is None

    def test_change_customer_password(self):
        bank = MockBank([Customer("Bob", "123"), Customer("Alice", "456")])
        assert bank.change_customer_password("Bob", "789")
        assert bank.customers[0].password == "789"

    def test_change_customer_password_fail(self):
        bank = MockBank([Customer("Bob", "123")])
        assert not bank.change_customer_password("Alice", "789")

    def test_remove_customer(self):
        bank = MockBank([Customer("Bob", "123"), Customer("Alice", "456")])
        bob = bank.customers[0]
        assert bob in bank.customers
        assert bank.remove_customer("Bob")
        assert len(bank.customers) == 1
        assert bob not in bank.customers

    def test_remove_customer_fail(self):
        bank = MockBank([Customer("Bob", "123")])
        assert not bank.remove_customer("Alice")
        assert len(bank.customers) == 1

    def test_remove_customer_logged_in(self):
        bank = MockBank([Customer("Bob", "123"), Customer("Alice", "456")])
        bob = bank.customers[0]
        bank.current_user = bob
        assert bob in bank.customers
        assert bank.remove_customer("Bob")
        assert len(bank.customers) == 1
        assert bob not in bank.customers
        assert bank.current_user is None


    def test_login(self):
        bank = MockBank([Customer("Bob", "123")])
        assert bank.login("Bob", "123")
        assert bank.current_user == Customer("Bob", "123")

    def test_login_wrong_password(self):
        bank = MockBank([Customer("Bob", "123")])
        assert not bank.login("Bob", "bad_password")
        assert bank.current_user is None

    def test_login_wrong_name(self):
        bank = MockBank([Customer("Bob", "123")])
        assert not bank.login("Alice", "123")
        assert bank.current_user is None

    def test_logout(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.logout()
        assert bank.current_user is None

    def test_logout_fail(self):
        bank = Bank()
        assert not bank.logout()

    def test_get_accounts(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert type(bank.get_accounts()) == list

    def test_get_accounts_fail(self):
        bank = Bank()
        assert bank.get_accounts() is None

    def test_add_account(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.add_account(1101000)
        assert bank.add_account(1101001)
        assert len(bank.current_user.accounts) == 2

    def test_add_account_no_user(self):
        bank = Bank()
        assert not bank.add_account(1101000)

    def test_add_account_non_unique(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.add_account(1)
        assert not bank.add_account(1)
        assert len(bank.current_user.accounts) == 1

    def test_add_account_wrong_type(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.add_account("1101000") is False
        assert len(bank.current_user.accounts) == 0

    def test_remove_account(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1), Account(2)]
        assert bank.remove_account(1)
        assert len(bank.current_user.accounts) == 1

    def test_remove_account_no_user(self):
        bank = Bank()
        assert not bank.remove_account(1)

    def test_remove_account_no_account(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert not bank.remove_account(1)
        assert len(bank.current_user.accounts) == 0

    def test_get_account(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1), Account(2)]
        acc = bank.get_account(1)
        assert acc is not None
        assert acc.account_number == 1

    def test_get_account_no_user(self):
        bank = Bank()
        assert bank.get_account(1) is None

    def test_get_account_no_accounts(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert bank.get_account(1) is None

    def test_get_account_wrong_account_number(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1), Account(2)]
        assert bank.get_account(3) is None

    def test_deposit_int(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1)]
        assert bank.deposit(1, 100)
        assert bank.current_user.accounts[0].balance == 100

    def test_deposit_float(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1)]
        assert bank.deposit(1, 1.23456789)
        assert bank.current_user.accounts[0].balance == 1.23

    def test_deposit_negative(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert not bank.deposit(1, -100)
        assert bank.current_user.accounts[0].balance == 100

    def test_deposit_no_user(self):
        bank = Bank()
        assert not bank.deposit(1, 100)

    def test_deposit_wrong_type(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1)]
        assert bank.deposit(1, "100") is False
        assert bank.current_user.accounts[0].balance == 0

    def test_deposit_no_accounts(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert not bank.deposit(1, 100)

    def test_deposit_wrong_account_number(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1), Account(2)]
        assert not bank.deposit(3, 100)

    def test_withdraw_int(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert bank.withdraw(1, 1)
        assert bank.current_user.accounts[0].balance == 99

    def test_withdraw_float(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert bank.withdraw(1, 0.1)
        assert bank.current_user.accounts[0].balance == 99.9

    def test_withdraw_negative(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert not bank.withdraw(1, -100)
        assert bank.current_user.accounts[0].balance == 100

    def test_withdraw_negative_no_user(self):
        bank = Bank()
        assert not bank.withdraw(1, 100)

    def test_withdraw_no_accounts(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        assert not bank.withdraw(1, 100)

    def test_withdraw_wrong_account_number(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1)]
        assert not bank.withdraw(3, 100)

    def test_withdraw_wrong_type(self):
        bank = Bank()
        bank.current_user = Customer("Bob", "123")
        bank.current_user.accounts = [Account(1, 100)]
        assert bank.withdraw(1, "1") is False
        assert bank.current_user.accounts[0].balance == 100

    def test___str__(self):
        bank = MockBank([Customer("Bob", "123"), Customer("Alice", "456")])
        assert str(bank) == f'Bank({[Customer("Bob", "123"), Customer("Alice", "456")]}, current_user=None)'

    def test___str__logged_in(self):
        bank = MockBank([Customer("Bob", "123")])
        bank.current_user = Customer("Bob", "123")
        assert str(bank) == f'Bank({[Customer("Bob", "123")]}, current_user={Customer("Bob", "123")})'

    def test___repr__(self):
        bank = MockBank([Customer("Bob", "123"), Customer("Alice", "456")])
        assert repr(bank) == f'Bank({[Customer("Bob", "123"), Customer("Alice", "456")]}, current_user=None)'

    def test___repr__logged_in(self):
        bank = MockBank([Customer("Bob", "123")])
        bank.current_user = Customer("Bob", "123")
        assert repr(bank) == f'Bank({[Customer("Bob", "123")]}, current_user={Customer("Bob", "123")})'
