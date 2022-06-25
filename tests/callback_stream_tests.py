# ========================================================= #
import unittest
import polygon
from polygon import cred
import datetime as dt
import time
import json
# ========================================================= #

# Test Runners
cred.KEY = cred.KEY
func = polygon.streaming.streaming.ensure_prefix

# ========================================================= #


class TestCallbackStreamPrefix(unittest.TestCase):
    def test_forex_stream_prefix(self):
        data = func('C:EUR/USD', _prefix='C:')
        data2 = func('EUR/USD', _prefix='C:')
        data3 = func('C:eur/usd', _prefix='C:')
        data4 = func('eur/usd', _prefix='C:')
        data5 = func('EuR/uSD', _prefix='C:')

        self.assertEqual(data, 'C:EUR/USD')
        self.assertEqual(data2, 'C:EUR/USD')
        self.assertEqual(data3, 'C:EUR/USD')
        self.assertEqual(data4, 'C:EUR/USD')
        self.assertEqual(data5, 'C:EUR/USD')

    def test_option_stream_prefix(self):
        data = func('O:TSLA120110c00123000')
        data2 = func('TSLA120110c00123000')
        data3 = func('O:tsla120110C00123000')
        data4 = func('O:tSLa120110P00123000')
        data5 = func('TsLa120110p00123000')

        self.assertEqual(data, 'O:TSLA120110C00123000')
        self.assertEqual(data2, 'O:TSLA120110C00123000')
        self.assertEqual(data3, 'O:TSLA120110C00123000')
        self.assertEqual(data4, 'O:TSLA120110P00123000')
        self.assertEqual(data5, 'O:TSLA120110P00123000')

    def test_crypto_stream_prefix(self):
        data = func('X:BTC-USD', _prefix='X:')
        data2 = func('btc-USD', _prefix='X:')
        data3 = func('X:btc-usd', _prefix='X:')
        data4 = func('bTc-Usd', _prefix='X:')
        data5 = func('X:Btc-USD', _prefix='X:')

        self.assertEqual(data, 'X:BTC-USD')
        self.assertEqual(data2, 'X:BTC-USD')
        self.assertEqual(data3, 'X:BTC-USD')
        self.assertEqual(data4, 'X:BTC-USD')
        self.assertEqual(data5, 'X:BTC-USD')


# ========================================================= #


class TestStocksStream(unittest.TestCase):
    def message_handler(self, ws, msg):
        msg = json.loads(msg)
        print(f'msg: {msg} || type: {type(msg)}')
        self._state = msg[-1]['ev']

    def test_streaming_stocks(self):
        self._state = None

        streamer = polygon.StreamClient(cred.KEY, 'stocks', on_message=self.message_handler)
        streamer.start_stream_thread()

        # subbing STOCK TRADES
        streamer.subscribe_stock_trades(['AMD', 'NVDA'], force_uppercase_symbols=False)
        time.sleep(3)

        try:
            self.assertEqual(self._state, 'T')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing STOCK TRADES
        streamer.unsubscribe_stock_trades(['AMD', 'NVDA'])
        time.sleep(2)

        try:
            self.assertEqual(self._state, 'status')

        except AssertionError:
            streamer.close_stream()
            raise

        # subbing STOCK QUOTES
        streamer.subscribe_stock_quotes(['AMD', 'NVDA'])
        time.sleep(3)

        try:
            self.assertEqual(self._state, 'Q')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing STOCK QUOTES
        streamer.unsubscribe_stock_quotes(['AMD', 'NVDA'])
        time.sleep(3)

        try:
            self.assertEqual(self._state, 'status')

        except AssertionError:
            streamer.close_stream()
            raise

        # subbing STOCK Minute Aggregates
        streamer.subscribe_stock_minute_aggregates(['AMD', 'NVDA'])
        time.sleep(1.5)

        try:
            self.assertEqual(self._state, 'status')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing STOCK Minute Aggregates
        streamer.unsubscribe_stock_minute_aggregates(['AMD', 'NVDA'])
        time.sleep(2)

        try:
            self.assertEqual(self._state, 'status')

        except AssertionError:
            streamer.close_stream()
            raise

        # subbing STOCK Second Aggregates
        streamer.subscribe_stock_second_aggregates(['AMD', 'NVDA'])
        time.sleep(4)

        try:
            self.assertEqual(self._state, 'A')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing STOCK Second Aggregates
        streamer.unsubscribe_stock_second_aggregates(['AMD', 'NVDA'])
        time.sleep(2)

        try:
            self.assertEqual(self._state, 'status')

        except AssertionError:
            streamer.close_stream()
            raise

        finally:
            streamer.close_stream()


# ========================================================= #


class TestOptionsStream(unittest.TestCase):
    def message_handler(self, ws, msg):
        msg = json.loads(msg)
        print(f'msg: {msg} || type: {type(msg)}')
        self._state = msg[-1]['ev']

    def test_streaming_options(self):
        cred.KEY = cred.OK
        self._state = None

        streamer = polygon.StreamClient(cred.KEY, 'options', on_message=self.message_handler)
        streamer.start_stream_thread()

        # subbing OPTIONS TRADES
        streamer.subscribe_option_trades(force_uppercase_symbols=False)
        time.sleep(2)

        try:
            self.assertEqual(self._state, 'T')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing OPTIONS TRADES
        streamer.unsubscribe_option_trades()
        time.sleep(3)

        try:
            self.assertTrue(self._state in ['status', 'T'])

        except AssertionError:
            streamer.close_stream()
            raise

        # subbing OPTIONS QUOTES
        streamer.subscribe_option_quotes()
        time.sleep(2)

        try:
            self.assertEqual(self._state, 'Q')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing OPTIONS QUOTES
        streamer.unsubscribe_option_quotes()
        time.sleep(3)

        try:
            self.assertTrue(self._state in ['status', 'Q'])

        except AssertionError:
            streamer.close_stream()
            raise

        # subbing OPTIONS Second aggregates
        streamer.subscribe_option_second_aggregates()
        time.sleep(2)

        try:
            self.assertEqual(self._state, 'A')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing OPTIONS Second aggregates
        streamer.unsubscribe_option_second_aggregates()
        time.sleep(3)

        try:
            self.assertTrue(self._state in ['status', 'A'])

        except AssertionError:
            streamer.close_stream()
            raise

        finally:
            streamer.close_stream()


# ========================================================= #


class TestForexStream(unittest.TestCase):
    def message_handler(self, ws, msg):
        msg = json.loads(msg)
        print(f'msg: {msg} || type: {type(msg)}')
        self._state = msg[-1]['ev']

    def test_streaming_forex(self):
        cred.KEY = cred.CK
        self._state = None

        streamer = polygon.StreamClient(cred.KEY, 'forex', on_message=self.message_handler)
        streamer.start_stream_thread()

        # subbing FOREX QUOTES
        streamer.subscribe_forex_quotes(force_uppercase_symbols=False)
        time.sleep(2)

        try:
            self.assertEqual(self._state, 'C')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing FOREX QUOTES
        streamer.unsubscribe_forex_quotes()
        time.sleep(3)

        try:
            self.assertTrue(self._state in ['status', 'C'])

        except AssertionError:
            streamer.close_stream()
            raise

        finally:
            streamer.close_stream()


# ========================================================= #


class TestCryptoStream(unittest.TestCase):
    def message_handler(self, ws, msg):
        msg = json.loads(msg)
        print(f'msg: {msg} || type: {type(msg)}')
        self._state = msg[-1]['ev']

    def test_streaming_crypto(self):
        cred.KEY = cred.CK
        self._state = None

        streamer = polygon.StreamClient(cred.KEY, 'crypto', on_message=self.message_handler)
        streamer.start_stream_thread()

        # subbing CRYPTO TRADES
        streamer.subscribe_crypto_trades()
        time.sleep(2)

        try:
            self.assertEqual(self._state, 'XT')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing CRYPTO TRADES
        streamer.unsubscribe_crypto_trades()
        time.sleep(3)

        try:
            self.assertTrue(self._state in ['status', 'XT'])

        except AssertionError:
            streamer.close_stream()
            raise

        # subbing CRYPTO QUOTES
        streamer.subscribe_crypto_quotes(force_uppercase_symbols=False)
        time.sleep(4)

        try:
            self.assertEqual(self._state, 'XQ')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing CRYPTO QUOTES
        streamer.unsubscribe_crypto_quotes()
        time.sleep(3)

        try:
            self.assertTrue(self._state in ['status', 'XQ'])

        except AssertionError:
            streamer.close_stream()
            raise

        # subbing CRYPTO LEVEL2
        streamer.subscribe_crypto_level2_book()
        time.sleep(5)

        try:
            self.assertEqual(self._state, 'XL2')

        except AssertionError:
            streamer.close_stream()
            raise

        # unsubbing CRYPTO LEVEL2
        streamer.unsubscribe_crypto_level2_book()
        time.sleep(3)

        try:
            self.assertTrue(self._state in ['status', 'XL2'])

        except AssertionError:
            streamer.close_stream()
            raise

        finally:
            streamer.close_stream()


# ========================================================= #

if __name__ == '__main__':
    unittest.main()

# ========================================================= #
