from account import Account


class TestAccount:
    def test_get_balance_int(self):
        acc = Account(123, 1)
        assert acc.get_balance() == 1

    def test_get_balance_float(self):
        acc = Account(123, 0.1)
        assert acc.get_balance() == 0.1

    def test_get_balance_small_amount(self):
        acc = Account(123, 1e-30)
        assert acc.get_balance() == 0

    def test_get_balance_rounded(self):
        acc = Account(123, 0.005)
        assert acc.get_balance() == 0.01

    def test_balance_add(self):
        acc = Account(123, 1)
        acc.balance_add(1)
        assert acc.get_balance() == 2

    def test_balance_add_negative(self):
        amount = 100
        acc = Account(123, amount)
        assert acc.balance_add(-1) is False
        assert acc.get_balance() == amount

    def test_balance_add_wrong_type(self):
        acc = Account(123, 1)
        assert acc.balance_add("one") is False

    def test_balance_sub(self):
        acc = Account(123, 2)
        acc.balance_sub(1)
        assert acc.get_balance() == 1

    def test_balance_sub_negative(self):
        amount = 100
        acc = Account(123, amount)
        assert acc.balance_sub(-1) is False
        assert acc.get_balance() == amount

    def test_balance_sub_wrong_type(self):
        acc = Account(123, 1)
        assert acc.balance_sub("one") is False

    def test_balance_sub_withdraw_more_then_balance(self):
        acc = Account(123, 1)
        assert acc.balance_sub(2) is False
        assert acc.get_balance() > 0

    def test_balance_sub_withdraw_all(self):
        acc = Account(123, 1)
        assert acc.balance_sub(1) is True
        assert acc.get_balance() == 0

    def test___str__(self):
        acc = Account(123, 1)
        assert str(acc) == "Account number: 123, Balance: 1"

    def test___repr__(self):
        acc = Account(123, 1)
        assert repr(acc) == "Account(123, 1)"
