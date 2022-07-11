# ========================================================= #
import unittest
import polygon
from polygon import cred
import datetime as dt
from requests.models import Response
import asyncio
from httpx import Response as HttpxResponse
from polygon.enums import OptionSymbolFormat

# ========================================================= #

# Test Runners
cred.KEY = cred.OK

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


class TestOptionsPrefix(unittest.TestCase):
    def test_option_prefix(self):
        func = polygon.options.options.ensure_prefix

        data = func('O:TSLA120110C00123000')
        data2 = func('TSLA120110c00123000')
        data3 = func('O:tsla120110C00123000')
        data4 = func('O:tSLa120110P00123000')
        data5 = func('TsLa120110p00123000')

        self.assertEqual(data, 'O:TSLA120110C00123000')
        self.assertEqual(data2, 'O:TSLA120110C00123000')
        self.assertEqual(data3, 'O:TSLA120110C00123000')
        self.assertEqual(data4, 'O:TSLA120110P00123000')
        self.assertEqual(data5, 'O:TSLA120110P00123000')


class TestOptionSymbology(unittest.TestCase):
    def test_build_option_symbol(self):
        symbol1 = polygon.build_option_symbol('AMD', dt.date(2022, 6, 28), 'call', 546.56)
        symbol2 = polygon.build_option_symbol('TSLA', '220628', 'c', 546, _format='polygon')
        symbol3 = polygon.build_option_symbol('A', '220628', 'put', 66.01, prefix_o=True)

        self.assertEqual(symbol1, 'AMD220628C00546560')
        self.assertEqual(symbol2, 'TSLA220628C00546000')
        self.assertEqual(symbol3, 'O:A220628P00066010')
        
        symbol1 = polygon.build_option_symbol('AMD', dt.date(2022, 6, 28), 'call', 546.56, _format='tda')
        symbol2 = polygon.build_option_symbol('NVDA', '220628', 'c', 546, _format='tos')
        symbol3 = polygon.build_option_symbol('TSLA', dt.date(2022, 6, 28), 'put', 46.01, _format='tradier')
        symbol4 = polygon.build_option_symbol('A', dt.date(2022, 6, 28), 'p', 46.1, _format='ibkr')
        symbol5 = polygon.build_option_symbol('AB', dt.date(2022, 6, 28), 'p', 46.01, _format='trade_station')
        symbol6 = polygon.build_option_symbol('PTON', '220628', 'p', 46, _format=OptionSymbolFormat.POLYGON)

        self.assertEqual(symbol1, 'AMD_062822C546.56')
        self.assertEqual(symbol2, '.NVDA062822C546')
        self.assertEqual(symbol3, 'TSLA220628P00046010')
        self.assertEqual(symbol4, 'A 220628P00046100')
        self.assertEqual(symbol5, 'AB 220628P46.01')
        self.assertEqual(symbol6, 'PTON220628P00046000')
        
    def test_parse_option_symbol(self):
        parsed_details1 = polygon.parse_option_symbol('AMD211205C00156000')
        parsed_details2 = polygon.parse_option_symbol('AMD211205C00156000', output_format=list)
        parsed_details3 = polygon.parse_option_symbol('AMD211205C00156000', output_format=dict)
        
        self.assertIsInstance(parsed_details1, polygon.OptionSymbol)
        self.assertIsInstance(parsed_details2, list)
        self.assertIsInstance(parsed_details3, dict)

        self.assertTrue(parsed_details1.underlying_symbol == 'AMD' 
                        and parsed_details1.expiry == dt.date(2021, 12, 5) 
                        and parsed_details1.call_or_put == 'C' and parsed_details1.strike_price == 156 
                        and parsed_details1.option_symbol == 'AMD211205C00156000')
        
        self.assertTrue(parsed_details2, ['AMD', dt.date(2021, 12, 5), 'C', 156, 'AMD211205C00156000'])
        self.assertEqual(parsed_details3, {'underlying_symbol': 'AMD', 'expiry': dt.date(2021, 12, 5), 
                                           'call_or_put': 'C', 'strike_price': 156,
                                           'option_symbol': 'AMD211205C00156000'})

        parsed_details1 = polygon.parse_option_symbol('AMD211205C00156000', _format=OptionSymbolFormat.TRADIER)
        parsed_details2 = polygon.parse_option_symbol('AMD_062822P587.56', _format='tda', output_format=list)
        parsed_details3 = polygon.parse_option_symbol('AB 220628P46.01', _format='trade_station', output_format=dict)

        self.assertIsInstance(parsed_details1, polygon.OptionSymbol)
        self.assertIsInstance(parsed_details2, list)
        self.assertIsInstance(parsed_details3, dict)

        self.assertTrue(parsed_details1.underlying_symbol == 'AMD'
                        and parsed_details1.expiry == dt.date(2021, 12, 5)
                        and parsed_details1.call_or_put == 'C' and parsed_details1.strike_price == 156
                        and parsed_details1.option_symbol == 'AMD211205C00156000')

        self.assertTrue(parsed_details2, ['AMD', dt.date(2022, 6, 28), 'P', 587.56, 'AMD_062822P587.56'])
        self.assertEqual(parsed_details3, {'underlying_symbol': 'AB', 'expiry': dt.date(2022, 6, 28), 
                                           'call_or_put': 'P', 'strike_price': 46.01,
                                           'option_symbol': 'AB 220628P46.01'})
        
    def test_convert_option_symbol_formats(self):
        symbol1 = polygon.convert_option_symbol_formats('AMD220628P00096050', from_format='polygon', to_format='tda')
        symbol2 = polygon.convert_option_symbol_formats('AB 220628P46.01', from_format='trade_station',
                                                        to_format='polygon')
        symbol3 = polygon.convert_option_symbol_formats('NVDA220628C00546000', 'tradier', 'tos')
        
        self.assertEqual(symbol1, 'AMD_062822P96.05')
        self.assertEqual(symbol2, 'AB220628P00046010')
        self.assertEqual(symbol3, '.NVDA062822C546')
        
    def test_detect_option_symbol_format(self):
        format1 = polygon.detect_option_symbol_format('AMD_062822P96.05')
        format2 = polygon.detect_option_symbol_format('AB220628P00046010')
        format3 = polygon.detect_option_symbol_format('.NVDA062822C546')
        format4 = polygon.detect_option_symbol_format('AB 220628P46.01')
        format5 = polygon.detect_option_symbol_format('AB 220628P00046045')
        
        self.assertEqual(format1, 'tda')
        self.assertEqual(format2, 'polygon')
        self.assertEqual(format3, 'tos')
        self.assertEqual(format4, 'trade_station')
        self.assertEqual(format5, ['ibkr', 'trade_station'])
        
        
# ========================================================= #


class TestOptions(unittest.TestCase):
    def test_get_trades(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_trades('O:TSLA210903C00700000', limit=10)
            data2 = client.get_trades('O:TSLA210903C00700000', limit=10, raw_response=True)
            data3 = client.get_trades('O:TSLA210903C00700000', limit=5, all_pages=True, max_pages=2)
            data4 = client.get_trades('O:TSLA210903C00700000', limit=5, all_pages=True, max_pages=2,
                                      merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_trades('O:TSLA210903C00700000', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_quotes(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_quotes('O:TSLA210903C00700000', limit=10)
            data2 = client.get_quotes('O:TSLA210903C00700000', limit=10, raw_response=True)
            data3 = client.get_quotes('O:TSLA210903C00700000', limit=5, all_pages=True, max_pages=2)
            data4 = client.get_quotes('O:TSLA210903C00700000', limit=5, all_pages=True, max_pages=2,
                                      merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_quotes('O:TSLA210903C00700000', limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_last_trade(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_last_trade('O:TSLA210903C00700000')
            data2 = client.get_last_trade('O:TSLA210903C00700000', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_last_trade('O:TSLA210903C00700000')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_daily_open_close(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_daily_open_close('O:TSLA210903C00700000', date='2021-07-22')
            data2 = client.get_daily_open_close('TSLA210903C00700000', date=dt.date(2021, 7, 22), raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_daily_open_close('O:TSLA210903C00700000', date='2021-07-22')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_aggregate_bars(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_aggregate_bars('O:TSLA210903C00700000', '2021-09-10', dt.date(2021, 10, 1), limit=30)
            data2 = client.get_aggregate_bars('O:TSLA210903C00700000', dt.date(2021, 9, 10), '2021-10-01',
                                              limit=30, raw_response=True)
            data4 = client.get_aggregate_bars('TSLA210903C00700000', '2021-09-10', dt.date(2021, 10, 1),
                                              full_range=True, run_parallel=False, high_volatility=True)
            data3 = client.get_aggregate_bars('O:TSLA210903C00700000', '2021-09-10', dt.date(2021, 10, 1),
                                              full_range=True, run_parallel=True, high_volatility=True)
            data5 = client.get_aggregate_bars('TSLA210903C00700000', '2021-06-10', dt.date(2021, 10, 1),
                                              full_range=True, run_parallel=False, timespan='min',
                                              high_volatility=True)
            data6 = client.get_aggregate_bars('O:TSLA210903C00700000', '2021-06-10', dt.date(2021, 10, 1),
                                              full_range=True, run_parallel=True, timespan='minute',
                                              high_volatility=True)
            data7 = client.get_full_range_aggregate_bars('O:TSLA210903C00700000', '2021-06-10', '2021-10-01')

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
            self.assertTrue(len(data5) == len(data6) == len(data7) == 4355)

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_aggregate_bars('O:TSLA210903C00700000', from_date='2021-07-22', to_date='2021-10-22',
                                         limit=10)
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_snapshot(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_snapshot('AAPL', 'O:AAPL230616C00150000')
            data2 = client.get_snapshot('AAPL', 'O:AAPL230616C00150000', raw_response=True)
            data3 = client.get_snapshot('AAPL', 'O:AAPL230616C00150000', all_pages=True, max_pages=2)
            data4 = client.get_snapshot('AAPL', 'O:AAPL230616C00150000', all_pages=True, max_pages=2,
                                        merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3) <= 10, True)
            self.assertEqual(len(data4) <= 2, True)
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_snapshot('AAPL', 'O:AAPL230616C00150000')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_previous_close(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_previous_close('O:TSLA210903C00700000')
            data2 = client.get_previous_close('O:TSLA210903C00700000', adjusted=True, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_previous_close('O:TSLA210903C00700000')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_trades(self):
        async with polygon.OptionsClient(cred.KEY, True) as client:
            data = await client.get_trades('O:TSLA210903C00700000', limit=10)
            data2 = await client.get_trades('O:TSLA210903C00700000', limit=10, raw_response=True)
            data3 = await client.get_trades('O:TSLA210903C00700000', limit=5, all_pages=True, max_pages=2)
            data4 = await client.get_trades('O:TSLA210903C00700000', limit=5, all_pages=True, max_pages=2,
                                            merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, True)
        data = await client.get_trades('O:TSLA210903C00700000', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_quotes(self):
        async with polygon.OptionsClient(cred.KEY, True) as client:
            data = await client.get_quotes('O:TSLA210903C00700000', limit=10)
            data2 = await client.get_quotes('O:TSLA210903C00700000', limit=10, raw_response=True)
            data3 = await client.get_quotes('O:TSLA210903C00700000', limit=5, all_pages=True, max_pages=2)
            data4 = await client.get_quotes('O:TSLA210903C00700000', limit=5, all_pages=True, max_pages=2,
                                            merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), 10)
            self.assertEqual(len(data4), 2)

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, True)
        data = await client.get_quotes('O:TSLA210903C00700000', limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_last_trade(self):
        async with polygon.OptionsClient(cred.KEY, use_async=True) as client:
            data = await client.get_last_trade('O:TSLA210903C00700000')
            data2 = await client.get_last_trade('O:TSLA210903C00700000', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, use_async=True)
        data = await client.get_last_trade('O:TSLA210903C00700000')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_daily_open_close(self):
        async with polygon.OptionsClient(cred.KEY, True) as client:
            data = await client.get_daily_open_close('O:TSLA210903C00700000', date='2021-07-22')
            data2 = await client.get_daily_open_close('TSLA210903C00700000', date=dt.date(2021, 7, 22),
                                                      raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, True)
        data = await client.get_daily_open_close('O:TSLA210903C00700000', date='2021-07-22')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_aggregate_bars(self):
        async with polygon.OptionsClient(cred.KEY, True) as client:
            data = await client.get_aggregate_bars('O:TSLA210903C00700000', '2021-09-10', dt.date(2021, 10, 1),
                                                   limit=30)
            data2 = await client.get_aggregate_bars('O:TSLA210903C00700000', dt.date(2021, 9, 10), '2021-10-01',
                                                    limit=30, raw_response=True)
            data4 = await client.get_aggregate_bars('TSLA210903C00700000', '2021-09-10', dt.date(2021, 10, 1),
                                                    full_range=True, run_parallel=False, high_volatility=True)
            data3 = await client.get_aggregate_bars('O:TSLA210903C00700000', '2021-09-10', dt.date(2021, 10, 1),
                                                    full_range=True, run_parallel=True, high_volatility=True)
            data5 = await client.get_aggregate_bars('TSLA210903C00700000', '2021-06-10', dt.date(2021, 10, 1),
                                                    full_range=True, run_parallel=False, timespan='min',
                                                    high_volatility=True)
            data6 = await client.get_aggregate_bars('O:TSLA210903C00700000', '2021-06-10', dt.date(2021, 10, 1),
                                                    full_range=True, run_parallel=True, timespan='minute',
                                                    high_volatility=True)
            data7 = await client.get_full_range_aggregate_bars('O:TSLA210903C00700000', '2021-06-10', '2021-10-01')

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
            self.assertTrue(len(data5) == len(data6) == len(data7) == 4355)

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, True)
        data = await client.get_aggregate_bars('TSLA210903C00700000', from_date='2021-07-22', to_date='2021-10-22',
                                               limit=10)
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_snapshot(self):
        async with polygon.OptionsClient(cred.KEY, True) as client:
            data = await client.get_snapshot('AAPL', 'O:AAPL230616C00150000')
            data2 = await client.get_snapshot('AAPL', 'O:AAPL230616C00150000', raw_response=True)
            data3 = await client.get_snapshot('AAPL', 'O:AAPL230616C00150000', all_pages=True, max_pages=2)
            data4 = await client.get_snapshot('AAPL', 'O:AAPL230616C00150000', all_pages=True, max_pages=2,
                                              merge_all_pages=False)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(len(data3) <= 10, True)
            self.assertEqual(len(data4) <= 2, True)
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, True)
        data = await client.get_snapshot('AAPL', 'O:AAPL230616C00150000')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_previous_close(self):
        async with polygon.OptionsClient(cred.KEY, use_async=True) as client:
            data = await client.get_previous_close('O:TSLA210903C00700000')
            data2 = await client.get_previous_close('O:TSLA210903C00700000', adjusted=True, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, use_async=True)
        data = await client.get_previous_close('O:TSLA210903C00700000')
        await client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')


# ========================================================= #

if __name__ == '__main__':
    unittest.main()

# ========================================================= #
