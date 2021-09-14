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


class TestStocks(unittest.TestCase):
    def test_get_trades(self):
        with polygon.PolygonClient(cred.KEY) as client:
            data = client.get_trades('AMD', date='2021-06-28', limit=10)
            data1 = client.get_trades('AMD', date=datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = client.get_trades('AMD', date=datetime.datetime(2021, 6, 28), limit=10, raw_response=True)
            data3 = client.get_trades('AMD', date='2021-06-28', limit=10, reverse=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data3, dict)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)
            self.assertIsInstance(data3, dict)

            self.assertEqual(len(data['results']), 10)
            self.assertEqual(len(data1.json()['results']), 10)
            self.assertEqual(len(data2.json()['results']), 10)
            self.assertEqual(len(data3['results']), 10)

            self.assertTrue(data['results'] == data1.json()['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY)
        data = client.get_trades('AMD', date='2021-06-28', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    @async_test
    async def test_async_get_trades(self):
        async with polygon.PolygonClient(cred.KEY, True) as client:
            data = await client.async_get_trades('AMD', date='2021-06-28', limit=10)
            data1 = await client.async_get_trades('AMD', date=datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = await client.async_get_trades('AMD', date=datetime.datetime(2021, 6, 28), limit=10,
                                                  raw_response=True)
            data3 = await client.async_get_trades('AMD', date='2021-06-28', limit=10, reverse=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data3, dict)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)
            self.assertIsInstance(data3, dict)

            self.assertEqual(len(data['results']), 10)
            self.assertEqual(len(data1.json()['results']), 10)
            self.assertEqual(len(data2.json()['results']), 10)
            self.assertEqual(len(data3['results']), 10)

            self.assertTrue(data['results'] == data1.json()['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY, True)
        data = await client.async_get_trades('AMD', date='2021-06-28', limit=10)
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)


# ========================================================= #


if __name__ == '__main__':
    unittest.main()


# ========================================================= #
