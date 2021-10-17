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


class TestCrypto(unittest.TestCase):
    def test_get_historic_crypto_ticks(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_historic_trades('BTC', 'USD', '2021-10-15', limit=5)
            data2 = client.get_historic_trades('BTC', 'USD', datetime.date(2021, 10, 15), limit=5,
                                               raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_historic_trades('BTC', 'USD', '2021-10-15', limit=5)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_last_trade(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_last_trade('BTC', 'USD')
            data2 = client.get_last_trade('BTC', 'USD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_last_trade('BTC', 'USD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_daily_open_close(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_daily_open_close('BTC', 'USD', '2021-10-15')
            data2 = client.get_daily_open_close('BTC', 'USD', date=datetime.date(2021, 10, 15), raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_daily_open_close('BTC', 'USD', '2021-10-15')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_aggregate_bars(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
            data2 = client.get_aggregate_bars('X:BTCUSD', datetime.date(2021, 9, 10), '2021-10-1', limit=30,
                                              raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_grouped_daily_bars(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_grouped_daily_bars('2021-10-15')
            data2 = client.get_grouped_daily_bars(datetime.datetime(2021, 10, 15), raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_grouped_daily_bars('2021-10-15')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_previous_close(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_previous_close('X:BTCUSD')
            data2 = client.get_previous_close('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_previous_close('X:BTCUSD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_snapshot_all(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_snapshot_all(['X:BTCUSD'])
            data2 = client.get_snapshot_all(['X:BTCUSD'], raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_snapshot_all(['X:BTCUSD'])
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_snapshot(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_snapshot('X:BTCUSD')
            data2 = client.get_snapshot('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_snapshot('X:BTCUSD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_gainers_and_losers(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_gainers_and_losers('gainers')
            data2 = client.get_gainers_and_losers('losers', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_gainers_and_losers('gainers')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_level2_book(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_level2_book('X:BTCUSD')
            data2 = client.get_level2_book('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_level2_book('X:BTCUSD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    # ASYNC tests
    async def test_async_get_historic_forex_ticks(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_historic_trades('BTC', 'USD', '2021-10-15', limit=5)
            data2 = await client.async_get_historic_trades('BTC', 'USD', datetime.date(2021, 10, 15), limit=5,
                                                           raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_historic_trades('BTC', 'USD', '2021-10-15', limit=5)
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async_get_last_trade(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_last_trade('BTC', 'USD')
            data2 = await client.async_get_last_trade('BTC', 'USD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_last_trade('BTC', 'USD')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async_get_daily_open_close(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_daily_open_close('BTC', 'USD', '2021-10-15')
            data2 = await client.async_get_daily_open_close('BTC', 'USD', date=datetime.date(2021, 10, 15),
                                                            raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_daily_open_close('BTC', 'USD', '2021-10-15')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async__get_aggregate_bars(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
            data2 = await client.async_get_aggregate_bars('X:BTCUSD', datetime.date(2021, 9, 10), '2021-10-1', limit=30,
                                                          raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async_get_grouped_daily_bars(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_grouped_daily_bars('2021-10-15')
            data2 = await client.async_get_grouped_daily_bars(datetime.datetime(2021, 10, 15), raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_grouped_daily_bars('2021-10-15')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async_get_previous_close(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_previous_close('X:BTCUSD')
            data2 = await client.async_get_previous_close('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_previous_close('X:BTCUSD')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async_get_snapshot_all(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_snapshot_all(['X:BTCUSD'])
            data2 = await client.async_get_snapshot_all(['X:BTCUSD'], raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_snapshot_all(['X:BTCUSD'])
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async_get_snapshot(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_snapshot('X:BTCUSD')
            data2 = await client.async_get_snapshot('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_snapshot('X:BTCUSD')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async__get_gainers_and_losers(self):
        with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_gainers_and_losers('gainers')
            data2 = await client.async_get_gainers_and_losers('losers', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_gainers_and_losers('gainers')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    async def test_async__get_level2_book(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.async_get_level2_book('X:BTCUSD')
            data2 = await client.async_get_level2_book('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.async_get_level2_book('X:BTCUSD')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')


# ========================================================= #


if __name__ == '__main__':
    unittest.main()


# ========================================================= #
