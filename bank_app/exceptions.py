


class BankError(Exception):
    """Base exception for Bank class"""
    pass

class CustomerError(Exception):
    pass

class BankLookupError(BankError):
    """
    Item was not found
    """
    def __init__(self, name):
        msg = f"Customer of name {name} not found"
        super().__init__(msg)


class