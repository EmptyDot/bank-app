from account import Account
from customer import Customer


class TestCustomer:

    def test_check_name_same(self):
        c = Customer("Bob", "123")
        assert c.check_name("Bob")

    def test_check_name_diff_capitalization(self):
        c = Customer("Bob", "123")
        assert c.check_name("BOB")

    def test_check_name_wrong_name(self):
        c = Customer("Bob", "123")
        assert not c.check_name("Alice")

    def test_check_password_correct_password(self):
        password = "123456789"
        c = Customer("Bob", password)
        assert c.check_password(password)

    def test_check_password_wrong_password(self):
        c = Customer("Bob", "password")
        assert c.check_password("bad_password") is False

    def test_add_account(self):
        acc = Account(124641576515, 10000)
        c = Customer("Bob", "123456789")
        len_acc = len(c.accounts)
        c.add_account(acc)

        assert len_acc + 1 == len(c.accounts)
        assert acc == c.accounts[-1]

    def test_add_account_wrong_type(self):
        c = Customer("Bob", "123456789")
        assert c.add_account("Hi") is False

    def test___eq__true(self):
        bob = Customer("Bob", "123")
        bob2 = Customer("Bob", "123")
        assert bob is not bob2 and bob == bob2

    def test___eq__false(self):
        bob = Customer("Bob", "123")
        alice = Customer("Alice", "456")
        assert bob != alice

    def test___eq__wrong_type(self):
        bob = Customer("Bob", "123")
        assert bob != "bob"