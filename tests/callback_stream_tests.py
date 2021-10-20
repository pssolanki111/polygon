# ========================================================= #
import unittest
import polygon
from polygon import cred
import datetime as dt
# ========================================================= #

# Test Runners
cred.KEY = cred.OK

# ========================================================= #


class TestStocksStream(unittest.TestCase):
    def __init__(self):
        super().__init__()
        self._state = None

    def message_handler(self, ws, msg):
        print(f'msg: {msg} || type: {type(msg)}')


# ========================================================= #


class TestOptionsStream(unittest.TestCase):
    pass


# ========================================================= #


class TestForexStream(unittest.TestCase):
    pass


# ========================================================= #


class TestCryptoStream(unittest.TestCase):
    pass


# ========================================================= #

if __name__ == '__main__':
    unittest.main()

# ========================================================= #
