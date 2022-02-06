# ========================================================= #
import unittest
import polygon
from polygon import cred
import datetime as dt
from requests.models import Response
import asyncio
from httpx import Response as HttpxResponse
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


# ========================================================= #


class TestOptions(unittest.TestCase):
    def test_build_option_symbol(self):
        bos = polygon.build_option_symbol('X', '211205', 'call', 134)
        bos1 = polygon.build_option_symbol('AA', dt.date(2021, 12, 5), 'c', 134.4)
        bos2 = polygon.build_option_symbol('AMD', '211205', 'p', 14.23, prefix_o=True)
        bos3 = polygon.build_option_symbol('MSFT', dt.datetime(2021, 12, 5), 'put', 7.345)
        bos4 = polygon.build_option_symbol('WPGGQ', '211205', 'CALL', 134.0)
        bos5 = polygon.build_option_symbol('PPPPPP', dt.date(2021, 12, 5), 'P', '134.345')

        self.assertEqual(bos, 'X211205C00134000')
        self.assertEqual(bos1, 'AA211205C00134400')
        self.assertEqual(bos2, 'O:AMD211205P00014230')
        self.assertEqual(bos3, 'MSFT211205P00007345')
        self.assertEqual(bos4, 'WPGGQ211205C00134000')
        self.assertEqual(bos5, 'PPPPPP211205P00134345')

    def test_parse_option_symbol(self):
        bos = polygon.parse_option_symbol('O:A211015C00090000')  
        bos2 = polygon.parse_option_symbol('O:AA211015C00013000', expiry_format=str)  
        bos3 = polygon.parse_option_symbol('AA211015P00015000', output_format=list)  
        bos4 = polygon.parse_option_symbol('AMD211015P00037500', output_format=dict, expiry_format=str)
        bos5 = polygon.parse_option_symbol('O:AMD211015P00040000')  
        bos6 = polygon.parse_option_symbol('NVDA211015C00070000', output_format=list)  
        bos7 = polygon.parse_option_symbol('O:NVDA211015C00072500', output_format=dict)
        bos8 = polygon.parse_option_symbol('O:GOOGL211015C00780000', output_format=list)  
        bos9 = polygon.parse_option_symbol('GOOGL2211015P00780000', output_format=list)
        bos10 = polygon.parse_option_symbol('O:AMD1211015C00040000', output_format=list)  

        self.assertIsInstance(bos, polygon.OptionSymbol)
        self.assertIsInstance(bos2, polygon.OptionSymbol)
        self.assertIsInstance(bos3, list)
        self.assertIsInstance(bos4, dict)

        _dt = int(dt.date.today().strftime('%Y')[:2] + '21')

        self.assertTrue(bos.underlying_symbol == 'A' and bos.expiry == dt.date(_dt, 10, 15) and bos.call_or_put == 'C'
                        and bos.strike_price == 90 and bos.option_symbol == 'A211015C00090000')
        self.assertTrue(bos2.underlying_symbol == 'AA' and bos2.expiry == f'{_dt}-10-15' and bos2.call_or_put ==
                        'C' and bos2.strike_price == 13 and bos2.option_symbol == 'AA211015C00013000')
        self.assertTrue(bos5.underlying_symbol == 'AMD' and bos5.expiry == dt.date(_dt, 10, 15) and bos5.call_or_put ==
                        'P' and bos5.strike_price == 40 and bos5.option_symbol == 'AMD211015P00040000')

        self.assertEqual(bos3, ['AA', dt.date(_dt, 10, 15), 'P', 15, 'AA211015P00015000'])
        self.assertEqual(bos6, ['NVDA', dt.date(_dt, 10, 15), 'C', 70, 'NVDA211015C00070000'])
        self.assertEqual(bos8, ['GOOGL', dt.date(_dt, 10, 15), 'C', 780, 'GOOGL211015C00780000'])
        self.assertEqual(bos9, ['GOOGL', dt.date(_dt, 10, 15), 'P', 780, 'GOOGL211015P00780000'])
        self.assertEqual(bos10, ['AMD', dt.date(_dt, 10, 15), 'C', 40, 'AMD211015C00040000'])

        self.assertEqual(bos4, {'underlying_symbol': 'AMD',
                                'strike_price': 37.5,
                                'expiry': f'{_dt}-10-15',
                                'call_or_put': 'P',
                                'option_symbol': 'AMD211015P00037500'})
        self.assertEqual(bos7, {'underlying_symbol': 'NVDA',
                                'strike_price': 72.5,
                                'expiry': dt.date(_dt, 10, 15),
                                'call_or_put': 'C',
                                'option_symbol': 'NVDA211015C00072500'})

    def test_build_option_symbol_for_tda(self):
        bos = polygon.build_option_symbol_for_tda('X', '120521', 'call', 134)
        bos1 = polygon.build_option_symbol_for_tda('AA', dt.date(2021, 12, 5), 'c', 134.4)
        bos2 = polygon.build_option_symbol_for_tda('AMD', '120521', 'p', 14.23)
        bos3 = polygon.build_option_symbol_for_tda('MSFT', dt.datetime(2021, 12, 5), 'put', 7.345)
        bos4 = polygon.build_option_symbol_for_tda('WPGGQ', '120521', 'CALL', 134.0)
        bos5 = polygon.build_option_symbol_for_tda('PPPPPP', dt.date(2021, 12, 5), 'P', '134.345')
        bos6 = polygon.build_option_symbol_for_tda('PPPPPP', dt.date(2021, 12, 5), 'P', '134.345', format_='dot')

        self.assertEqual(bos, 'X_120521C134')
        self.assertEqual(bos1, 'AA_120521C134.4')
        self.assertEqual(bos2, 'AMD_120521P14.23')
        self.assertEqual(bos3, 'MSFT_120521P7.345')
        self.assertEqual(bos4, 'WPGGQ_120521C134')
        self.assertEqual(bos5, 'PPPPPP_120521P134.345')
        self.assertEqual(bos6, '.PPPPPP120521P134.345')

    def test_parse_option_symbol_from_tda(self):
        bos = polygon.parse_option_symbol_from_tda('X_101521C134')
        bos3 = polygon.parse_option_symbol_from_tda('AA_101521C134.4', output_format=list)
        bos4 = polygon.parse_option_symbol_from_tda('AMD_101521P14.23', output_format=dict, expiry_format=str)
        bos6 = polygon.parse_option_symbol_from_tda('MSFT_101521P7.345', output_format=list)
        bos8 = polygon.parse_option_symbol_from_tda('WPGGQ_101521C134.0', output_format=list)
        bos9 = polygon.parse_option_symbol_from_tda('PPPPPP_101521P134.345', output_format=list)
        bos10 = polygon.parse_option_symbol_from_tda('.PPPPPP211015P134.345', output_format=list)
        bos11 = polygon.parse_option_symbol_from_tda('.X211015P134', output_format=list)

        self.assertIsInstance(bos, polygon.OptionSymbol)
        self.assertIsInstance(bos3, list)
        self.assertIsInstance(bos4, dict)

        _dt = int(dt.date.today().strftime('%Y')[:2] + '21')

        self.assertTrue(bos.underlying_symbol == 'X' and bos.expiry == dt.date(_dt, 10, 15) and bos.call_or_put == 'C'
                        and bos.strike_price == 134 and bos.option_symbol == 'X_101521C134')

        self.assertEqual(bos3, ['AA', dt.date(_dt, 10, 15), 'C', 134.4, 'AA_101521C134.4'])
        self.assertEqual(bos6, ['MSFT', dt.date(_dt, 10, 15), 'P', 7.345, 'MSFT_101521P7.345'])
        self.assertEqual(bos8, ['WPGGQ', dt.date(_dt, 10, 15), 'C', 134, 'WPGGQ_101521C134.0'])
        self.assertEqual(bos9, ['PPPPPP', dt.date(_dt, 10, 15), 'P', 134.345, 'PPPPPP_101521P134.345'])
        self.assertEqual(bos10, ['PPPPPP', dt.date(_dt, 10, 15), 'P', 134.345, 'PPPPPP_101521P134.345'])
        self.assertEqual(bos11, ['X', dt.date(_dt, 10, 15), 'P', 134, 'X_101521P134'])

        self.assertEqual(bos4, {'underlying_symbol': 'AMD',
                                'strike_price': 14.23,
                                'expiry': f'{_dt}-10-15',
                                'call_or_put': 'P',
                                'option_symbol': 'AMD_101521P14.23'})

    def test_convert_from_tda_to_polygon_format(self):
        bos1 = polygon.convert_from_tda_to_polygon_format('X_101521C134')
        bos2 = polygon.convert_from_tda_to_polygon_format('AA_101521C134.4', True)
        bos3 = polygon.convert_from_tda_to_polygon_format('AMD_101521P14.23')
        bos4 = polygon.convert_from_tda_to_polygon_format('MSFT_101521P7.345')
        bos5 = polygon.convert_from_tda_to_polygon_format('WPGGQ_101521C134.0')
        bos6 = polygon.convert_from_tda_to_polygon_format('PPPPPP_101521P134.345')
        bos7 = polygon.convert_from_tda_to_polygon_format('.PPPPPP211015P134.345')
        bos8 = polygon.convert_from_tda_to_polygon_format('.X211015P134.02')

        self.assertEqual(bos1, 'X211015C00134000')
        self.assertEqual(bos2, 'O:AA211015C00134400')
        self.assertEqual(bos3, 'AMD211015P00014230')
        self.assertEqual(bos4, 'MSFT211015P00007345')
        self.assertEqual(bos5, 'WPGGQ211015C00134000')
        self.assertEqual(bos6, 'PPPPPP211015P00134345')
        self.assertEqual(bos7, 'PPPPPP211015P00134345')
        self.assertEqual(bos8, 'X211015P00134020')

    def test_convert_from_polygon_to_tda_format(self):
        bos1 = polygon.convert_from_polygon_to_tda_format('X211015C00134000')
        bos2 = polygon.convert_from_polygon_to_tda_format('O:AA211015C00134400')
        bos3 = polygon.convert_from_polygon_to_tda_format('AMD211015P00014230')
        bos4 = polygon.convert_from_polygon_to_tda_format('MSFT211015P00007345')
        bos5 = polygon.convert_from_polygon_to_tda_format('WPGGQ211015C00134000')
        bos6 = polygon.convert_from_polygon_to_tda_format('PPPPPP211015P00134345')
        bos7 = polygon.convert_from_polygon_to_tda_format('PPPPPP211015P00134345', format_='dot')
        bos8 = polygon.convert_from_polygon_to_tda_format('X211015P00134000', format_='dot')

        self.assertEqual(bos1, 'X_101521C134')
        self.assertEqual(bos2, 'AA_101521C134.4')
        self.assertEqual(bos3, 'AMD_101521P14.23')
        self.assertEqual(bos4, 'MSFT_101521P7.345')
        self.assertEqual(bos5, 'WPGGQ_101521C134')
        self.assertEqual(bos6, 'PPPPPP_101521P134.345')
        self.assertEqual(bos7, '.PPPPPP101521P134.345')
        self.assertEqual(bos8, '.X101521P134')

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

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)
            self.assertIsInstance(data2.json(), dict)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data5, list)
            self.assertIsInstance(data6, list)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), len(data4))
            self.assertEqual(len(data5), 4355)
            self.assertEqual(len(data6), 4355)

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

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)
            self.assertIsInstance(data2.json(), dict)
            self.assertIsInstance(data3, list)
            self.assertIsInstance(data4, list)
            self.assertIsInstance(data5, list)
            self.assertIsInstance(data6, list)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')
            self.assertEqual(len(data3), len(data4))
            self.assertEqual(len(data5), 4355)
            self.assertEqual(len(data6), 4355)

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
