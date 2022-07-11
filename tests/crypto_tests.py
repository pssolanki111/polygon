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


class TestCryptoPrefix(unittest.TestCase):
    def test_crypto_prefix(self):
        func = polygon.crypto.crypto_api.ensure_prefix

        data = func('X:BTCUSD')
        data2 = func('btcUSD')
        data3 = func('X:btcusd')
        data4 = func('bTcUsd')
        data5 = func('X:BtcUSD')

        self.assertEqual(data, 'X:BTCUSD')
        self.assertEqual(data2, 'X:BTCUSD')
        self.assertEqual(data3, 'X:BTCUSD')
        self.assertEqual(data4, 'X:BTCUSD')
        self.assertEqual(data5, 'X:BTCUSD')


# ========================================================= #


class TestCrypto(unittest.TestCase):
    def test_get_historic_crypto_trades(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_historic_trades('BTC', 'USD', '2021-10-15', limit=5)
            data2 = client.get_historic_trades('BTC', 'USD', datetime.date(2021, 10, 15), limit=5,
                                               raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_historic_trades('BTC', 'USD', '2021-10-15', limit=5)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    def test_get_trades(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_trades('X:BTC-USD', limit=5)
            data2 = client.get_trades('X:BTC-USD', datetime.date(2021, 10, 15), limit=5, raw_response=True)
            data3 = client.get_trades('X:BTC-USD', limit=5, all_pages=True, max_pages=2)
            data4 = client.get_trades('X:BTC-USD', limit=5, all_pages=True, max_pages=2, merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_trades('BTC-USD')
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

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_last_trade('BTC', 'USD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    def test_get_daily_open_close(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_daily_open_close('BTC', 'USD', '2021-10-15')
            data2 = client.get_daily_open_close('BTC', 'USD', date=datetime.date(2021, 10, 15), raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)

        # without context manager
        client = polygon.CryptoClient(cred.KEY)
        data = client.get_daily_open_close('BTC', 'USD', '2021-10-15')
        client.close()
        self.assertIsInstance(data, dict)

    def test_get_aggregate_bars(self):
        with polygon.CryptoClient(cred.KEY) as client:
            data = client.get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
            data2 = client.get_aggregate_bars('BTCUSD', datetime.date(2021, 9, 10), '2021-10-01',
                                              limit=30, raw_response=True)
            data4 = client.get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1), full_range=True,
                                              run_parallel=False, high_volatility=True)
            data3 = client.get_aggregate_bars('BTCUSD', '2021-09-10', datetime.date(2021, 10, 1),  full_range=True,
                                              run_parallel=True, high_volatility=True)
            data5 = client.get_aggregate_bars('X:BTCUSD', '2021-06-10', datetime.date(2021, 10, 1),
                                              full_range=True, run_parallel=False, timespan='min',
                                              high_volatility=True)
            data6 = client.get_aggregate_bars('X:BTCUSD', '2021-06-10', datetime.date(2021, 10, 1),
                                              full_range=True, run_parallel=True, timespan='minute',
                                              high_volatility=True)
            data7 = client.get_full_range_aggregate_bars('BTCUSD', '2021-06-10', '2021-10-01')

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data5, list)
            self.assertIsInstance(data6, list)
            self.assertIsInstance(data7, list)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), len(data4))
            self.assertTrue(len(data5) == len(data6) == len(data7) == 164159)

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
    @async_test
    async def test_async_get_historic_crypto_trades(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_historic_trades('BTC', 'USD', '2021-10-15', limit=5)
            data2 = await client.get_historic_trades('BTC', 'USD', datetime.date(2021, 10, 15), limit=5,
                                                     raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_historic_trades('BTC', 'USD', '2021-10-15', limit=5)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    @async_test
    async def test_async_get_trades(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_trades('X:BTC-USD', limit=5)
            data2 = await client.get_trades('X:BTC-USD', datetime.date(2021, 10, 15), limit=5, raw_response=True)
            data3 = await client.get_trades('X:BTC-USD', limit=5, all_pages=True, max_pages=2)
            data4 = await client.get_trades('X:BTC-USD', limit=5, all_pages=True, max_pages=2, merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            # print(data4[0]['count'], data4[1]['count'])
            print(len(data4[0]['results']), '\n', len(data4[1]['results']))
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_trades('BTC-USD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_last_trade(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_last_trade('BTC', 'USD')
            data2 = await client.get_last_trade('BTC', 'USD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data2.json()['status'], 'success')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_last_trade('BTC', 'USD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'success')

    @async_test
    async def test_async_get_daily_open_close(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_daily_open_close('BTC', 'USD', '2021-10-15')
            data2 = await client.get_daily_open_close('BTC', 'USD', date=datetime.date(2021, 10, 15),
                                                            raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_daily_open_close('BTC', 'USD', '2021-10-15')
        await client.close()
        self.assertIsInstance(data, dict)

    @async_test
    async def test_async_get_aggregate_bars(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
            data2 = await client.get_aggregate_bars('X:BTCUSD', datetime.date(2021, 9, 10), '2021-10-01',
                                                          limit=30, raw_response=True)
            data4 = await client.get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1),
                                                    full_range=True, run_parallel=False, high_volatility=True)
            data3 = await client.get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1),
                                                    full_range=True, run_parallel=True, high_volatility=True)
            data5 = await client.get_aggregate_bars('X:BTCUSD', '2021-06-10', datetime.date(2021, 10, 1),
                                                    full_range=True, run_parallel=False, timespan='min',
                                                    high_volatility=True)
            data6 = await client.get_aggregate_bars('X:BTCUSD', '2021-06-10', datetime.date(2021, 10, 1),
                                                    full_range=True, run_parallel=True, timespan='minute',
                                                    high_volatility=True)
            data7 = client.get_full_range_aggregate_bars('BTCUSD', '2021-06-10', '2021-10-01')

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data5, list)
            self.assertIsInstance(data6, list)
            self.assertIsInstance(data7, list)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), len(data4))
            self.assertTrue(len(data5) == len(data6) == len(data7) == 164159)

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_aggregate_bars('X:BTCUSD', '2021-09-10', datetime.date(2021, 10, 1), limit=30)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_grouped_daily_bars(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_grouped_daily_bars('2021-10-15')
            data2 = await client.get_grouped_daily_bars(datetime.datetime(2021, 10, 15), raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_grouped_daily_bars('2021-10-15')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_previous_close(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_previous_close('X:BTCUSD')
            data2 = await client.get_previous_close('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_previous_close('X:BTCUSD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_snapshot_all(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_snapshot_all(['X:BTCUSD'])
            data2 = await client.get_snapshot_all(['X:BTCUSD'], raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_snapshot_all(['X:BTCUSD'])
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_snapshot(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_snapshot('X:BTCUSD')
            data2 = await client.get_snapshot('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_snapshot('X:BTCUSD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async__get_gainers_and_losers(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_gainers_and_losers('gainers')
            data2 = await client.get_gainers_and_losers('losers', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_gainers_and_losers('gainers')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async__get_level2_book(self):
        async with polygon.CryptoClient(cred.KEY, True) as client:
            data = await client.get_level2_book('X:BTCUSD')
            data2 = await client.get_level2_book('X:BTCUSD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # without context manager
        client = polygon.CryptoClient(cred.KEY, True)
        data = await client.get_level2_book('X:BTCUSD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')


# ========================================================= #


if __name__ == '__main__':
    unittest.main()


# ========================================================= #
