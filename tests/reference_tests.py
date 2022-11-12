# ========================================================= #
import unittest
import polygon
from polygon import cred
import datetime
from requests.models import Response
import asyncio
from httpx import Response as HttpxResponse
from collections import OrderedDict

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


class TestReferences(unittest.TestCase):
    def test_get_tickers(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_tickers('AMD')
            data1 = client.get_tickers(search='GO', limit=20, market='stocks')
            data2 = client.get_tickers(symbol_type='CS', market='stocks', raw_response=True, limit=120)
            data3 = client.get_tickers(limit=5, market='stocks', all_pages=True, max_pages=2)
            data4 = client.get_tickers(limit=5, market='stocks', all_pages=True, max_pages=2,
                                       merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['count'], 1)
            self.assertEqual(data1['count'], 20)
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)
            self.assertEqual(data2.json()['count'], 120)

        # Testing without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_tickers(search='GO', limit=30, market='stocks')
        data1 = client.get_next_page(data)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data1, dict)
        self.assertEqual(data['count'], 30)
        self.assertEqual(data1['count'], 30)

    def test_get_ticker_types(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_ticker_types()
            data1 = client.get_ticker_types(asset_class='stocks', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)

            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_ticker_types()
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_ticker_details(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_ticker_details('AMD')
            data1 = client.get_ticker_details('AMD', date='2021-06-28', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_ticker_details('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')
        
    def test_get_bulk_ticker_details(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11')
            data1 = client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11', sort='desc')
            data2 = client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11', 
                                                   custom_dates=['2022-06-28', '2022-06-27'])
            data3 = client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11', run_parallel=False)

            self.assertIsInstance(data, OrderedDict)
            self.assertIsInstance(data1, OrderedDict)
            self.assertIsInstance(data2, OrderedDict)
            self.assertIsInstance(data3, OrderedDict)
            
            self.assertTrue(len(data) == len(data3) == len(data1) == 4)
            self.assertTrue(list(data1.keys())[-1] < list(data1.keys())[0])
            self.assertTrue(len(data2), 6)

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11')
        client.close()
        self.assertIsInstance(data, OrderedDict)
        self.assertTrue(len(data) == 4)

    def test_get_option_contract(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_option_contract('AMD1220520C00090000', as_of_date=datetime.date(2022, 4, 20))
            data1 = client.get_option_contract('O:AMD1220520C00090000',
                                               as_of_date=datetime.date(2022, 4, 20), raw_response=True)
            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_option_contract('AMD1220520C00090000', as_of_date=datetime.date(2022, 4, 20))
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_option_contracts(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_option_contracts('AMD', limit=10)
            data1 = client.get_option_contracts('AMD', limit=10, contract_type='call', raw_response=True)
            data3 = client.get_option_contracts('AMD', limit=5, all_pages=True, max_pages=2)
            data4 = client.get_option_contracts('AMD', limit=5, all_pages=True, max_pages=2, merge_all_pages=False)
            
            # as_of_date test to get historical contracts
            one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
            data_one_year_ago = client.get_option_contracts('AMD', all_pages=True, as_of_date=one_year_ago)
            self.assertIsInstance(data_one_year_ago, list)
            self.assertTrue(len(data_one_year_ago) > 0)
            # as of one year ago, we must have at least one expiration date in the year and month of one_year_ago
            # list of expiration dates with the day stripped
            exp_year_and_month = [c['expiration_date'][:7] for c in data_one_year_ago]
            self.assertIn(one_year_ago.strftime('%Y-%m'), exp_year_and_month)
            
        
            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_option_contracts('AMD', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_ticker_news(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_ticker_news(limit=10)
            data1 = client.get_ticker_news('AMD', limit=10, raw_response=True)
            data3 = client.get_ticker_news(limit=5, all_pages=True, max_pages=2)
            data4 = client.get_ticker_news(limit=5, all_pages=True, max_pages=2, merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_ticker_news('AMD', limit=10)
        data1 = client.get_next_page(data)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data1, dict)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data1['status'], 'OK')

    def test_get_stock_dividends(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_stock_dividends('AMD')
            data1 = client.get_stock_dividends('AMD', raw_response=True)
            data3 = client.get_stock_dividends('AMD', limit=5, all_pages=True, max_pages=2)
            data4 = client.get_stock_dividends('AMD', limit=5, all_pages=True, max_pages=2, merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3) <= 10, True)
            self.assertEqual(len(data4) <= 2, True)
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_stock_dividends('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_stock_financials_vx(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_stock_financials_vx('AMD', limit=10)
            data1 = client.get_stock_financials_vx('AMD', include_sources=True, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_stock_financials_vx('AMD', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_stock_splits(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_stock_splits('AMD')
            data1 = client.get_stock_splits('AMD', raw_response=True)
            data3 = client.get_stock_splits('AMD', limit=5, all_pages=True, max_pages=2)
            data4 = client.get_stock_splits('AMD', limit=5, all_pages=True, max_pages=2, merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3) <= 10, True)
            self.assertEqual(len(data4) <= 2, True)
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_stock_splits('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_market_holidays(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_market_holidays()
            data1 = client.get_market_holidays(raw_response=True)

            self.assertIsInstance(data, list)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), list)

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_market_holidays()
        client.close()
        self.assertIsInstance(data, list)

    def test_get_market_status(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_market_status()
            data1 = client.get_market_status(raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_market_status()
        client.close()
        self.assertIsInstance(data, dict)

    def test_get_conditions(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_conditions()
            data1 = client.get_conditions('options', data_type='nbbo', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_conditions()
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_exchanges(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_exchanges()
            data1 = client.get_exchanges('stocks', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_exchanges(locale='us')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_tickers(self):
        async with polygon.ReferenceClient(cred.KEY, use_async=True) as client:
            data = await client.get_tickers('AMD')
            data1 = await client.get_tickers(search='GO', limit=20, market='stocks')
            data2 = await client.get_tickers(symbol_type='CS', market='stocks', raw_response=True, limit=120)
            data3 = await client.get_tickers(limit=5, market='stocks', all_pages=True, max_pages=2)
            data4 = await client.get_tickers(limit=5, market='stocks', all_pages=True, max_pages=2,
                                             merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['count'], 1)
            self.assertEqual(data1['count'], 20)
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)
            self.assertEqual(data2.json()['count'], 120)

        # Testing without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_tickers(search='GO', limit=30, market='stocks')
        data1 = await client.get_next_page(data)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data1, dict)
        self.assertEqual(data['count'], 30)
        self.assertEqual(data1['count'], 30)

    @async_test
    async def test_async_get_ticker_types(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_ticker_types()
            data1 = await client.get_ticker_types(asset_class='stocks', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)

            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_ticker_types()
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_ticker_details(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_ticker_details('AMD')
            data1 = await client.get_ticker_details('AMD', date='2021-06-28', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_ticker_details('AMD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')
        
    @async_test
    async def test_get_bulk_ticker_details(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11')
            data1 = await client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11', sort='desc')
            data2 = await client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11', 
                                                         custom_dates=['2022-06-28', '2022-06-27'])
            data3 = await client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11', run_parallel=False)

            self.assertIsInstance(data, OrderedDict)
            self.assertIsInstance(data1, OrderedDict)
            self.assertIsInstance(data2, OrderedDict)
            self.assertIsInstance(data3, OrderedDict)
            
            self.assertTrue(len(data) == len(data3) == len(data1) == 4)
            self.assertTrue(list(data1.keys())[-1] < list(data1.keys())[0])
            self.assertTrue(len(data2), 6)

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_bulk_ticker_details('AMD', '2022-07-08', '2022-07-11')
        await client.close()
        self.assertIsInstance(data, OrderedDict)
        self.assertTrue(len(data) == 4)

    @async_test
    async def test_async_get_option_contract(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_option_contract('AMD1220520C00090000', as_of_date=datetime.date(2022, 4, 20))
            data1 = await client.get_option_contract('O:AMD1220520C00090000',
                                                     as_of_date=datetime.date(2022, 4, 20), raw_response=True)
            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_option_contract('AMD1220520C00090000', as_of_date=datetime.date(2022, 4, 20))
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_option_contracts(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_option_contracts('AMD', limit=10)
            data1 = await client.get_option_contracts('AMD', limit=10, contract_type='call', raw_response=True)
            data3 = await client.get_option_contracts('AMD', limit=5, all_pages=True, max_pages=2)
            data4 = await client.get_option_contracts('AMD', limit=5, all_pages=True, max_pages=2,
                                                      merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)
            self.assertEqual(data1.json()['status'], 'OK')


            # as_of_date test to get historical contracts
            one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
            data_one_year_ago = await client.get_option_contracts('AMD', all_pages=True, as_of_date=one_year_ago)
            self.assertIsInstance(data_one_year_ago, list)
            self.assertTrue(len(data_one_year_ago) > 0)
            # as of one year ago, we must have at least one expiration date in the year and month of one_year_ago
            # list of expiration dates with the day stripped
            exp_year_and_month = [c['expiration_date'][:7] for c in data_one_year_ago]
            self.assertIn(one_year_ago.strftime('%Y-%m'), exp_year_and_month)

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_option_contracts('AMD', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_ticker_news(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_ticker_news(limit=10)
            data1 = await client.get_ticker_news('AMD', limit=10, raw_response=True)
            data3 = await client.get_ticker_news(limit=5, all_pages=True, max_pages=2)
            data4 = await client.get_ticker_news(limit=5, all_pages=True, max_pages=2, merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_ticker_news('AMD', limit=10)
        data1 = await client.get_next_page(data)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data1, dict)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data1['status'], 'OK')

    @async_test
    async def test_async_get_stock_dividends(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_stock_dividends('AMD')
            data1 = await client.get_stock_dividends('AMD', raw_response=True)
            data3 = await client.get_stock_dividends('AMD', limit=5, all_pages=True, max_pages=2)
            data4 = await client.get_stock_dividends('AMD', limit=5, all_pages=True, max_pages=2, merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3) <= 10, True)
            self.assertEqual(len(data4) <= 2, True)
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_stock_dividends('AMD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_stock_financials_vx(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_stock_financials_vx('AMD', limit=10)
            data1 = await client.get_stock_financials_vx('AMD', include_sources=True, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_stock_financials_vx('AMD', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_stock_splits(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_stock_splits('AMD')
            data1 = await client.get_stock_splits('AMD', raw_response=True)
            data3 = await client.get_stock_splits('AMD', limit=5, all_pages=True, max_pages=2)
            data4 = await client.get_stock_splits('AMD', limit=5, all_pages=True, max_pages=2, merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3) <= 10, True)
            self.assertEqual(len(data4) <= 2, True)
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_stock_splits('AMD')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_market_holidays(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_market_holidays()
            data1 = await client.get_market_holidays(raw_response=True)

            self.assertIsInstance(data, list)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data1.json(), list)

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_market_holidays()
        await client.close()
        self.assertIsInstance(data, list)

    @async_test
    async def test_async_get_market_status(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_market_status()
            data1 = await client.get_market_status(raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data1.json(), dict)

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_market_status()
        await client.close()
        self.assertIsInstance(data, dict)

    @async_test
    async def test_async_get_conditions(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_conditions()
            data1 = await client.get_conditions('options', data_type='nbbo', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_conditions()
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_exchanges(self):
        async with polygon.ReferenceClient(cred.KEY, True) as client:
            data = await client.get_exchanges()
            data1 = await client.get_exchanges('stocks', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, HttpxResponse)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY, True)
        data = await client.get_exchanges(locale='us')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')


# ========================================================= #


if __name__ == '__main__':
    unittest.main()

# ========================================================= #
