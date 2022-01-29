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


class TestChangeEnums(unittest.TestCase):
    def test_change_enum_sync_base(self):
        from polygon import enums
        base_client = polygon.BaseClient('LoL')

        test1 = base_client._change_enum(enums.StreamCluster.STOCKS, str)
        test2 = base_client._change_enum('stocks', str)
        test3 = base_client._change_enum(enums.StreamCluster.OPTIONS, [str, int])
        test4 = base_client._change_enum('options', [str, int])
        test5 = base_client._change_enum(enums.TickerType.CS)
        test6 = base_client._change_enum('CS')
        test7 = base_client._change_enum(enums.StockReportType.TRAILING_TWELVE_MONTHS_ANNUALIZED, [str, int])
        test8 = base_client._change_enum(5, int)
        test9 = base_client._change_enum(68.6, [int, str, float])

        self.assertEqual(test1, 'stocks')
        self.assertEqual(test2, 'stocks')
        self.assertEqual(test3, 'options')
        self.assertEqual(test4, 'options')
        self.assertEqual(test5, 'CS')
        self.assertEqual(test6, 'CS')
        self.assertEqual(test7, 'TA')
        self.assertEqual(test8, 5)
        self.assertEqual(test9, 68.6)


# ========================================================= #


class TestStocks(unittest.TestCase):
    def test_get_trades(self):
        with polygon.StocksClient(cred.KEY) as client:
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

            self.assertEqual(len(data['results']), 10)
            self.assertEqual(len(data1.json()['results']), 10)
            self.assertEqual(len(data2.json()['results']), 10)
            self.assertEqual(len(data3['results']), 10)

            self.assertTrue(data['results'] == data1.json()['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_trades('AMD', date='2021-06-28', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    def test_get_trades_vx(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_trades_vx('AMD', '2021-06-28', limit=10)
            data1 = client.get_trades_vx('AMD', datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = client.get_trades_vx('AMD', datetime.datetime(2021, 6, 28), limit=10, raw_response=True)
            data3 = client.get_trades_vx('AMD', '2021-06-28', limit=10)
            data4 = client.get_trades_vx('AMD', '2021-06-28', limit=5, all_pages=True, max_pages=2)
            data5 = client.get_trades_vx('AMD', '2021-06-28', limit=5, all_pages=True, max_pages=2,
                                         merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data3, dict)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data5, list)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(len(data['results']), 10)
            self.assertEqual(len(data1.json()['results']), 10)
            self.assertEqual(len(data2.json()['results']), 10)
            self.assertEqual(len(data3['results']), 10)
            self.assertEqual(len(data4), 10)
            self.assertEqual(len(data5), 2)

            self.assertTrue(data['results'] == data1.json()['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_trades_vx('AMD', '2021-06-28', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    def test_get_quotes(self):
        with polygon.StocksClient(cred.KEY) as client:
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
        client = polygon.StocksClient(cred.KEY)
        data = client.get_quotes('AMD', date='2021-06-28', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    def test_get_quotes_vx(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_quotes_vx('AMD', '2021-06-28', limit=10)
            data1 = client.get_quotes_vx('AMD', datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = client.get_quotes_vx('AMD', datetime.datetime(2021, 6, 28), limit=10, raw_response=True)
            data3 = client.get_quotes_vx('AMD', '2021-06-28', limit=10)
            data4 = client.get_quotes_vx('AMD', '2021-06-28', limit=5, all_pages=True, max_pages=2)
            data5 = client.get_quotes_vx('AMD', '2021-06-28', limit=5, all_pages=True, max_pages=2,
                                         merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data3, dict)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data5, list)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(len(data['results']), 10)
            self.assertEqual(len(data1.json()['results']), 10)
            self.assertEqual(len(data2.json()['results']), 10)
            self.assertEqual(len(data3['results']), 10)
            self.assertEqual(len(data4), 10)
            self.assertEqual(len(data5), 2)

            self.assertTrue(data['results'] == data1.json()['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_quotes_vx('AMD', '2021-06-28', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    def test_get_last_trade(self):
        with polygon.StocksClient(cred.KEY) as client:
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
        client = polygon.StocksClient(cred.KEY)
        data = client.get_last_trade('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_last_quote(self):
        with polygon.StocksClient(cred.KEY) as client:
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
        client = polygon.StocksClient(cred.KEY)
        data = client.get_last_quote('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_daily_open_close(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_daily_open_close('AMD', '2021-06-28')
            data1 = client.get_daily_open_close('AMD', datetime.datetime(2021, 6, 28), raw_response=True)
            data2 = client.get_daily_open_close('AMD', datetime.datetime(2021, 6, 28), raw_response=True,
                                                adjusted=False)

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
        client = polygon.StocksClient(cred.KEY)
        data = client.get_daily_open_close('AMD', '2021-06-28')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_aggregate_bars(self):
        with polygon.StocksClient(cred.KEY) as client:
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
        client = polygon.StocksClient(cred.KEY)
        data = client.get_aggregate_bars('NVDA', '2020-06-28', '2021-06-28', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertLessEqual(len(data['results']), 10)

    def test_get_grouped_daily_bars(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_grouped_daily_bars('2020-06-28')
            data1 = client.get_grouped_daily_bars('2020-06-28', adjusted=False)
            data2 = client.get_grouped_daily_bars('2020-06-28', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, dict)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

            self.assertIn(data['adjusted'], ['true', True])
            self.assertIn(data1['adjusted'], ['false', False])
            self.assertIn(data2.json()['adjusted'], ['true', True])

            self.assertEqual(data['resultsCount'], 0)
            self.assertEqual(data1['resultsCount'], 0)
            self.assertEqual(data2.json()['resultsCount'], 0)

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_grouped_daily_bars('2020-06-28')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['resultsCount'], 0)

    def test_get_previous_close(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_previous_close('AMD')
            data1 = client.get_previous_close('AMD', adjusted=False)
            data2 = client.get_previous_close('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, dict)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

            self.assertIn(data['adjusted'], ['true', True])
            self.assertIn(data1['adjusted'], ['false', False])
            self.assertIn(data2.json()['adjusted'], ['true', True])

            self.assertTrue(data['results'] == data1['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_previous_close('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_snapshot(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_snapshot('AMD')
            data1 = client.get_snapshot('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)

            self.assertIsInstance(data1.json(), dict)

            self.assertTrue(data['status'] in ['OK', 'NotFound'])
            self.assertTrue(data1.json()['status'] in ['OK', 'NotFound'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_snapshot('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertTrue(data['status'] in ['OK', 'NotFound'])

    def test_get_current_price(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_current_price('AMD')

            self.assertTrue(isinstance(data, (int, float)))
            self.assertGreater(data, 0)

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_current_price('AMD')
        client.close()
        self.assertTrue(isinstance(data, (int, float)))
        self.assertGreater(data, 0)

    def test_get_snapshot_all(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_snapshot_all(['AMD', 'NVDA'])
            data1 = client.get_snapshot_all(['AMD', 'NVDA'], raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)

            self.assertIsInstance(data1.json(), dict)

            self.assertTrue(data['status'] in ['OK', 'NotFound'])
            self.assertTrue(data1.json()['status'] in ['OK', 'NotFound'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_snapshot_all(['AMD', 'NVDA'])
        client.close()
        self.assertIsInstance(data, dict)
        self.assertTrue(data['status'] in ['OK', 'NotFound'])

    def test_get_gainers_and_losers(self):
        with polygon.StocksClient(cred.KEY) as client:
            data = client.get_gainers_and_losers()
            data1 = client.get_gainers_and_losers('losers', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)

            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY)
        data = client.get_gainers_and_losers()
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_trades(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_trades('AMD', date='2021-06-28', limit=10)
            data1 = await client.get_trades('AMD', date=datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = await client.get_trades('AMD', date=datetime.datetime(2021, 6, 28), limit=10,
                                            raw_response=True)
            data3 = await client.get_trades('AMD', date='2021-06-28', limit=10, reverse=False)

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
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_trades('AMD', date='2021-06-28', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    @async_test
    async def test_async_get_trades_vx(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_trades_vx('AMD', '2021-06-28', limit=10)
            data1 = await client.get_trades_vx('AMD', datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = await client.get_trades_vx('AMD', datetime.datetime(2021, 6, 28), limit=10, raw_response=True)
            data3 = await client.get_trades_vx('AMD', '2021-06-28', limit=10)
            data4 = await client.get_trades_vx('AMD', '2021-06-28', limit=5, all_pages=True, max_pages=2)
            data5 = await client.get_trades_vx('AMD', '2021-06-28', limit=5, all_pages=True, max_pages=2,
                                               merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data3, dict)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data5, list)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(len(data['results']), 10)
            self.assertEqual(len(data1.json()['results']), 10)
            self.assertEqual(len(data2.json()['results']), 10)
            self.assertEqual(len(data3['results']), 10)
            self.assertEqual(len(data4), 10)
            self.assertEqual(len(data5), 2)

            self.assertTrue(data['results'] == data1.json()['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_trades_vx('AMD', '2021-06-28', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    @async_test
    async def test_async_get_quotes(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_quotes('AMD', date='2021-06-28', limit=10)
            data1 = await client.get_quotes('AMD', date=datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = await client.get_quotes('AMD', date=datetime.datetime(2021, 6, 28), limit=10,
                                            raw_response=True)
            data3 = await client.get_quotes('AMD', date='2021-06-28', limit=10, reverse=False)

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
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_quotes('AMD', date='2021-06-28', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    @async_test
    async def test_async_get_quotes_vx(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_quotes_vx('AMD', '2021-06-28', limit=10)
            data1 = await client.get_quotes_vx('AMD', datetime.date(2021, 6, 28), limit=10, raw_response=True)
            data2 = await client.get_quotes_vx('AMD', datetime.datetime(2021, 6, 28), limit=10, raw_response=True)
            data3 = await client.get_quotes_vx('AMD', '2021-06-28', limit=10)
            data4 = await client.get_quotes_vx('AMD', '2021-06-28', limit=5, all_pages=True, max_pages=2)
            data5 = await client.get_quotes_vx('AMD', '2021-06-28', limit=5, all_pages=True, max_pages=2,
                                               merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data3, dict)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data5, list)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(len(data['results']), 10)
            self.assertEqual(len(data1.json()['results']), 10)
            self.assertEqual(len(data2.json()['results']), 10)
            self.assertEqual(len(data3['results']), 10)
            self.assertEqual(len(data4), 10)
            self.assertEqual(len(data5), 2)

            self.assertTrue(data['results'] == data1.json()['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_quotes_vx('AMD', '2021-06-28', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data['results']), 10)

    @async_test
    async def test_async_get_last_trade(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_last_trade('AMD')
            data1 = await client.get_last_trade('AMD', raw_response=True)
            data2 = await client.get_last_trade('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_last_trade('AMD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_last_quote(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_last_quote('AMD')
            data1 = await client.get_last_quote('AMD', raw_response=True)
            data2 = await client.get_last_quote('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)
            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_last_quote('AMD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_daily_open_close(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_daily_open_close('AMD', '2021-06-28')
            data1 = await client.get_daily_open_close('AMD', datetime.datetime(2021, 6, 28), raw_response=True)
            data2 = await client.get_daily_open_close('AMD', datetime.datetime(2021, 6, 28), raw_response=True,
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
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_daily_open_close('AMD', '2021-06-28')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_aggregate_bars(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_aggregate_bars('NVDA', '2020-06-28', '2021-06-28', limit=10)
            data1 = await client.get_aggregate_bars('NVDA', '2020-06-28', datetime.date(2021, 6, 28), limit=10,
                                                    raw_response=True)
            data2 = await client.get_aggregate_bars('NVDA', '2020-06-28', datetime.date(2021, 6, 28), limit=10,
                                                    raw_response=True, timespan='minute', multiplier=5)
            data3 = await client.get_aggregate_bars('NVDA', datetime.date(2020, 6, 28), '2021-06-28', limit=10,
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
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_aggregate_bars('NVDA', '2020-06-28', '2021-06-28', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertLessEqual(len(data['results']), 10)

    @async_test
    async def test_async_get_grouped_daily_bars(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_grouped_daily_bars('2020-06-28')
            data1 = await client.get_grouped_daily_bars('2020-06-28', adjusted=False)
            data2 = await client.get_grouped_daily_bars('2020-06-28', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, dict)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

            self.assertIn(data['adjusted'], ['true', True])
            self.assertIn(data1['adjusted'], ['false', False])
            self.assertIn(data2.json()['adjusted'], ['true', True])

            self.assertEqual(data['resultsCount'], 0)
            self.assertEqual(data1['resultsCount'], 0)
            self.assertEqual(data2.json()['resultsCount'], 0)

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, use_async=True)
        data = await client.get_grouped_daily_bars('2020-06-28')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['resultsCount'], 0)

    @async_test
    async def test_async_get_previous_close(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_previous_close('AMD')
            data1 = await client.get_previous_close('AMD', adjusted=False)
            data2 = await client.get_previous_close('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, dict)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

            self.assertIn(data['adjusted'], ['true', True])
            self.assertIn(data1['adjusted'], ['false', False])
            self.assertIn(data2.json()['adjusted'], ['true', True])

            self.assertTrue(data['results'] == data1['results'] == data2.json()['results'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_previous_close('AMD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_snapshot(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_snapshot('AMD')
            data1 = await client.get_snapshot('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)

            self.assertTrue(data['status'] in ['OK', 'NotFound'])
            self.assertTrue(data1.json()['status'] in ['OK', 'NotFound'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_snapshot('AMD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertTrue(data['status'] in ['OK', 'NotFound'])

    @async_test
    async def test_async_get_current_price(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_current_price('AMD')

            self.assertTrue(isinstance(data, (int, float)))
            self.assertGreater(data, 0)

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_current_price('AMD')
        await client.close()
        self.assertTrue(isinstance(data, (int, float)))
        self.assertGreater(data, 0)

    @async_test
    async def test_async_get_snapshot_all(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_snapshot_all(['AMD', 'NVDA'])
            data1 = await client.get_snapshot_all(['AMD', 'NVDA'], raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)

            self.assertTrue(data['status'] in ['OK', 'NotFound'])
            self.assertTrue(data1.json()['status'] in ['OK', 'NotFound'])

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_snapshot_all(['AMD', 'NVDA'])
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertTrue(data['status'] in ['OK', 'NotFound'])

    @async_test
    async def test_async_get_gainers_and_losers(self):
        async with polygon.StocksClient(cred.KEY, True) as client:
            data = await client.get_gainers_and_losers()
            data1 = await client.get_gainers_and_losers('losers', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # Testing without Context Manager
        client = polygon.StocksClient(cred.KEY, True)
        data = await client.get_gainers_and_losers()
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')


# ========================================================= #


if __name__ == '__main__':
    unittest.main()

# ========================================================= #
