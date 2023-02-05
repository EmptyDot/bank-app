class CustomerError(Exception):
    """Base class for customer exceptions"""

    pass


class CustomerNotFoundError(CustomerError):
    """Failure to access a customer"""
    pass
