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

    def test_get_quotes(self):
        with polygon.PolygonClient(cred.KEY) as client:
            data = client.get_quotes('AMD', date='2021-06-28', limit=10)
            data1 = client.get_quotes('AMD', date=datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = client.get_quotes('AMD', date=datetime.datetime(2021, 6, 28), limit=10, raw_response=True)
            data3 = client.get_quotes('AMD', date='2021-06-28', limit=10, reverse=False)

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
        data = client.get_quotes('AMD', date='2021-06-28', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    def test_get_last_trade(self):
        with polygon.PolygonClient(cred.KEY) as client:
            data = client.get_last_trade('AMD')
            data1 = client.get_last_trade('AMD', raw_response=True)
            data2 = client.get_last_trade('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY)
        data = client.get_last_trade('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_last_quote(self):
        with polygon.PolygonClient(cred.KEY) as client:
            data = client.get_last_quote('AMD')
            data1 = client.get_last_quote('AMD', raw_response=True)
            data2 = client.get_last_quote('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY)
        data = client.get_last_quote('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_daily_open_close(self):
        with polygon.PolygonClient(cred.KEY) as client:
            data = client.get_daily_open_close('AMD', '2021-06-28')
            data1 = client.get_daily_open_close('AMD', datetime.datetime(2021, 6, 28), raw_response=True)
            data2 = client.get_daily_open_close('AMD', datetime.datetime(2021, 6, 28), raw_response=True, adjusted=
                                                False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

            self.assertTrue(data == data1.json() == data2.json())

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY)
        data = client.get_daily_open_close('AMD', '2021-06-28')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_aggregate_bars(self):
        with polygon.PolygonClient(cred.KEY) as client:
            data = client.get_aggregate_bars('NVDA', '2020-06-28', '2021-06-28', limit=10)
            data1 = client.get_aggregate_bars('NVDA', '2020-06-28', datetime.date(2021, 6, 28), limit=10,
                                              raw_response=True)
            data2 = client.get_aggregate_bars('NVDA', '2020-06-28', datetime.date(2021, 6, 28), limit=10,
                                              raw_response=True, timespan='minute', multiplier=5)
            data3 = client.get_aggregate_bars('NVDA', datetime.date(2020, 6, 28), '2021-06-28', limit=10,
                                              raw_response=False, timespan='minute', multiplier=1)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data3, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertLessEqual(len(data['results']), 10)
            self.assertLessEqual(len(data1.json()['results']), 10)
            self.assertLessEqual(len(data2.json()['results']), 10)
            self.assertLessEqual(len(data3['results']), 10)

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY)
        data = client.get_aggregate_bars('NVDA', '2020-06-28', '2021-06-28', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertLessEqual(len(data['results']), 10)

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

    @async_test
    async def test_async_get_quotes(self):
        async with polygon.PolygonClient(cred.KEY, True) as client:
            data = await client.async_get_quotes('AMD', date='2021-06-28', limit=10)
            data1 = await client.async_get_quotes('AMD', date=datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = await client.async_get_quotes('AMD', date=datetime.datetime(2021, 6, 28), limit=10,
                                                  raw_response=True)
            data3 = await client.async_get_quotes('AMD', date='2021-06-28', limit=10, reverse=False)

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
        data = await client.async_get_quotes('AMD', date='2021-06-28', limit=10)
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    @async_test
    async def test_async_get_last_trade(self):
        async with polygon.PolygonClient(cred.KEY, True) as client:
            data = await client.async_get_last_trade('AMD')
            data1 = await client.async_get_last_trade('AMD', raw_response=True)
            data2 = await client.async_get_last_trade('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY, True)
        data = await client.async_get_last_trade('AMD')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_last_quote(self):
        async with polygon.PolygonClient(cred.KEY, True) as client:
            data = await client.async_get_last_quote('AMD')
            data1 = await client.async_get_last_quote('AMD', raw_response=True)
            data2 = await client.async_get_last_quote('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY, True)
        data = await client.async_get_last_quote('AMD')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_daily_open_close(self):
        async with polygon.PolygonClient(cred.KEY, True) as client:
            data = await client.async_get_daily_open_close('AMD', '2021-06-28')
            data1 = await client.async_get_daily_open_close('AMD', datetime.datetime(2021, 6, 28), raw_response=True)
            data2 = await client.async_get_daily_open_close('AMD', datetime.datetime(2021, 6, 28), raw_response=True,
                                                            adjusted=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

            self.assertTrue(data == data1.json() == data2.json())

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY, True)
        data = await client.async_get_daily_open_close('AMD', '2021-06-28')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_get_aggregate_bars(self):
        async with polygon.PolygonClient(cred.KEY, True) as client:
            data = await client.async_get_aggregate_bars('NVDA', '2020-06-28', '2021-06-28', limit=10)
            data1 = await client.async_get_aggregate_bars('NVDA', '2020-06-28', datetime.date(2021, 6, 28), limit=10,
                                                          raw_response=True)
            data2 = await client.async_get_aggregate_bars('NVDA', '2020-06-28', datetime.date(2021, 6, 28), limit=10,
                                                          raw_response=True, timespan='minute', multiplier=5)
            data3 = await client.async_get_aggregate_bars('NVDA', datetime.date(2020, 6, 28), '2021-06-28', limit=10,
                                                          raw_response=False, timespan='minute', multiplier=1)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data3, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertLessEqual(len(data['results']), 10)
            self.assertLessEqual(len(data1.json()['results']), 10)
            self.assertLessEqual(len(data2.json()['results']), 10)
            self.assertLessEqual(len(data3['results']), 10)

        # Testing without Context Manager
        client = polygon.PolygonClient(cred.KEY, True)
        data = await client.async_get_aggregate_bars('NVDA', '2020-06-28', '2021-06-28', limit=10)
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertLessEqual(len(data['results']), 10)


# ========================================================= #


if __name__ == '__main__':
    unittest.main()


# ========================================================= #
