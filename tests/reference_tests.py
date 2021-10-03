# ========================================================= #
import unittest
import polygon
from polygon import cred
import datetime
from requests.models import Response
import asyncio
from httpx import Response as HttpxResponse
import polygon.enums as enums
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

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, dict)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['count'], 1)
            self.assertEqual(data1['count'], 20)
            self.assertEqual(data2.json()['count'], 120)

        # Testing without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_tickers(search='GO', limit=30, market='stocks')
        data1 = client.get_next_page_tickers(data)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data1, dict)
        self.assertEqual(data['count'], 30)
        self.assertEqual(data1['count'], 30)

    def test_get_ticker_types(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_ticker_types_v3()
            data1 = client.get_ticker_types_v3(asset_class='stocks', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)

            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_ticker_types_v3()
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_ticker_details(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_ticker_details('AMD')
            data1 = client.get_ticker_details('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['type'], 'CS')
            self.assertEqual(data1.json()['type'], 'CS')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_ticker_details('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['type'], 'CS')

    def test_get_ticker_details_vx(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_ticker_details_vx('AMD')
            data1 = client.get_ticker_details_vx('AMD', date='2021-06-28', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_ticker_details_vx('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_option_contracts(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_option_contracts('AMD', limit=10)
            data1 = client.get_option_contracts('AMD', limit=10, contract_type='call', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
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

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_ticker_news('AMD', limit=10)
        data1 = client.get_next_page_news(data)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data1, dict)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data1['status'], 'OK')

    def test_get_stock_dividends(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_stock_dividends('AMD')
            data1 = client.get_stock_dividends('AMD', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_stock_dividends('AMD')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_stock_financials(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_stock_financials('AMD', limit=10)
            data1 = client.get_stock_financials('AMD', report_type='YA', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_stock_financials('AMD', limit=10)
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

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
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

    def test_get_condition_mappings(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_condition_mappings()
            data1 = client.get_condition_mappings('quotes', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_condition_mappings('trades')
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

    def test_get_locales(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_locales()
            data1 = client.get_locales(raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_locales()
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_markets(self):
        with polygon.ReferenceClient(cred.KEY) as client:
            data = client.get_markets()
            data1 = client.get_markets(raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data1, Response)
            self.assertIsInstance(data1.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data1.json()['status'], 'OK')

        # without context manager
        client = polygon.ReferenceClient(cred.KEY)
        data = client.get_markets()
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')


# ========================================================= #


if __name__ == '__main__':
    unittest.main()


# ========================================================= #
