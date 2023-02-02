from bank_app import logger


class C:
    def __init__(self):
        pass

    @logger.log_exception((TypeError, ValueError))
    def f(self):
        raise ValueError("TypeError in f")

f = C().f()
