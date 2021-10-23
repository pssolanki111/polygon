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
cred.KEY = cred.CK

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


class TestForexPrefix(unittest.TestCase):
    def test_forex_prefix(self):
        func = polygon.forex.forex_api.ensure_prefix

        data = func('C:EURUSD')
        data2 = func('EURUSD')
        data3 = func('C:eurusd')
        data4 = func('eurusd')
        data5 = func('EuRuSD')

        self.assertEqual(data, 'C:EURUSD')
        self.assertEqual(data2, 'C:EURUSD')
        self.assertEqual(data3, 'C:EURUSD')
        self.assertEqual(data4, 'C:EURUSD')
        self.assertEqual(data5, 'C:EURUSD')


# ========================================================= #


class TestForex(unittest.TestCase):
    def test_get_historic_forex_ticks(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_historic_forex_ticks('AUD', 'USD', '2021-10-15', limit=5)
            data2 = client.get_historic_forex_ticks('AUD', 'USD', datetime.date(2021, 10, 15), limit=5,
                                                    raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_historic_forex_ticks('AUD', 'USD', '2021-10-15', limit=5)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    def test_get_last_quote(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_last_quote('AUD', 'USD')
            data2 = client.get_last_quote('AUD', 'USD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_last_quote('AUD', 'USD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    def test_get_aggregate_bars(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_aggregate_bars('C:EURUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
            data2 = client.get_aggregate_bars('C:EURUSD', datetime.date(2021, 9, 10), '2021-10-01', limit=30,
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

    def test_get_grouped_daily_bars(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_grouped_daily_bars('2021-10-15')
            data2 = client.get_grouped_daily_bars(datetime.datetime(2021, 10, 15), raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_grouped_daily_bars('2021-10-15')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_previous_close(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_previous_close('C:EURUSD')
            data2 = client.get_previous_close('C:EURUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_previous_close('C:EURUSD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_snapshot_all(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_snapshot_all(['C:EURUSD'])
            data2 = client.get_snapshot_all(['C:EURUSD'], raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_snapshot_all(['C:EURUSD'])
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_snapshot(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_snapshot('C:EURUSD')
            data2 = client.get_snapshot('C:EURUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_snapshot('C:EURUSD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_gainers_and_losers(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.get_gainers_and_losers('gainers')
            data2 = client.get_gainers_and_losers('losers', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.get_gainers_and_losers('gainers')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_real_time_currency_conversion(self):
        with polygon.ForexClient(cred.KEY) as client:
            data = client.real_time_currency_conversion('AUD', 'USD', amount=10)
            data2 = client.real_time_currency_conversion('USD', 'AUD',  amount=10, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.ForexClient(cred.KEY)
        data = client.real_time_currency_conversion('AUD', 'USD', amount=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    # ASYNC tests
    @async_test
    async def test_async_get_historic_forex_ticks(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.get_historic_forex_ticks('AUD', 'USD', '2021-10-15', limit=5)
            data2 = await client.get_historic_forex_ticks('AUD', 'USD', datetime.date(2021, 10, 15), limit=5,
                                                                raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.get_historic_forex_ticks('AUD', 'USD', '2021-10-15', limit=5)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    @async_test
    async def test_async_get_last_quote(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.get_last_quote('AUD', 'USD')
            data2 = await client.get_last_quote('AUD', 'USD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.get_last_quote('AUD', 'USD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    @async_test
    async def test_async__get_aggregate_bars(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.get_aggregate_bars('C:EURUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
            data2 = await client.get_aggregate_bars('C:EURUSD', datetime.date(2021, 9, 10), '2021-10-01',
                                                          limit=30, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.get_aggregate_bars('C:EURUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_grouped_daily_bars(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.get_grouped_daily_bars('2021-10-15')
            data2 = await client.get_grouped_daily_bars(datetime.datetime(2021, 10, 15), raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.get_grouped_daily_bars('2021-10-15')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_previous_close(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.get_previous_close('C:EURUSD')
            data2 = await client.get_previous_close('C:EURUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.get_previous_close('C:EURUSD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async__get_snapshot_all(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.get_snapshot_all(['C:EURUSD'])
            data2 = await client.get_snapshot_all(['C:EURUSD'], raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.get_snapshot_all(['C:EURUSD'])
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_snapshot(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.get_snapshot('C:EURUSD')
            data2 = await client.get_snapshot('C:EURUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.get_snapshot('C:EURUSD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async__get_gainers_and_losers(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.get_gainers_and_losers('gainers')
            data2 = await client.get_gainers_and_losers('losers', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.get_gainers_and_losers('gainers')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_real_time_currency_conversion(self):
        async with polygon.ForexClient(cred.KEY, True) as client:
            data = await client.real_time_currency_conversion('AUD', 'USD', amount=10)
            data2 = await client.real_time_currency_conversion('USD', 'AUD',  amount=10, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.ForexClient(cred.KEY, True)
        data = await client.real_time_currency_conversion('AUD', 'USD', amount=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

# ========================================================= #


if __name__ == '__main__':
    unittest.main()


# ========================================================= #
