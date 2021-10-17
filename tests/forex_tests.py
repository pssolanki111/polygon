# ========================================================= #
import unittest
import polygon
from polygon import cred
import datetime
from requests.models import Response
import asyncio
from httpx import Response as HttpxResponse
# ========================================================= #

# Test Runners

# ========================================================= #


# Helper Function for testing asyncio components
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


# ========================================================= #


class ForexStocks(unittest.TestCase):
    def test_get_historic_forex_ticks(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_historic_forex_ticks('AUD', 'USD', '2021-10-15', limit=5)
            data2 = client.get_historic_forex_ticks('AUD', 'USD', datetime.date(2021, 10, 15), limit=5,
                                                    raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_historic_forex_ticks('AUD', 'USD', '2021-10-15', limit=5)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_last_quote(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_last_quote('AUD', 'USD')
            data2 = client.get_last_quote('AUD', 'USD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_last_quote('AUD', 'USD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_aggregate_bars(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_aggregate_bars('C:EURUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
            data2 = client.get_aggregate_bars('C:EURUSD', datetime.date(2021, 9, 10), '2021-10-1', limit=30,
                                              raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_aggregate_bars('C:EURUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

# ========================================================= #


if __name__ == '__main__':
    unittest.main()


# ========================================================= #
