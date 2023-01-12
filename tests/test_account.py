from account import Account


class TestAccount:
    def test_get_balance_int(self):
        acc = Account(123, 1)
        assert acc.balance == 1

    def test_get_balance_float(self):
        acc = Account(123, 0.1)
        assert acc.balance == 0.1

    def test_get_balance_small_amount(self):
        acc = Account(123, 1e-30)
        assert acc.balance == 0

    def test_get_balance_rounded(self):
        acc = Account(123, 0.005)
        assert acc.balance == 0.01

    def test_balance_add_int(self):
        acc = Account(123, 1)
        acc.balance_add(1)
        assert acc.balance == 2

    def test_balance_add_float(self):
        acc = Account(123, 1)
        acc.balance_add(1.6)
        assert acc.balance == 2.6

    def test_balance_add_negative(self):
        amount = 100
        acc = Account(123, amount)
        assert acc.balance_add(-1) is False
        assert acc.balance == amount

    def test_balance_sub_int(self):
        acc = Account(123, 2)
        acc.balance_sub(1)
        assert acc.balance == 1

    def test_balance_sub_float(self):
        acc = Account(123, 1)
        acc.balance_sub(0.4)
        assert acc.balance == 0.6

    def test_balance_sub_negative(self):
        amount = 100
        acc = Account(123, amount)
        assert acc.balance_sub(-1) is False
        assert acc.balance == amount

    def test_balance_sub_withdraw_more_then_balance(self):
        acc = Account(123, 1)
        assert acc.balance_sub(2) is False
        assert acc.balance == 1

    def test_balance_sub_withdraw_all(self):
        acc = Account(123, 1)
        assert acc.balance_sub(1) is True
        assert acc.balance == 0

    def test___str__(self):
        acc = Account(123, 1)
        assert str(acc) == "Account(123, balance=1.0)"

    def test___repr__(self):
        acc = Account(123, 1)
        assert repr(acc) == "Account(123, balance=1.0)"
