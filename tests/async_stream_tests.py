# ========================================================= #
import unittest
import json
import polygon
from polygon import cred
import datetime as dt
import asyncio
# ========================================================= #

# Test Runners
func = polygon.streaming.async_streaming.ensure_prefix

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


class TestAsyncStreamPrefix(unittest.TestCase):
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
    async def message_handler(self, msg):
        print(f'msg: {msg} || type: {type(msg)}')
        self._state = msg['ev']

    @staticmethod
    async def handle_messages(streamer, recon: bool = False):
        if recon:
            await streamer.handle_messages(recon)
            return

        while 1:
            await streamer.handle_messages()

    @async_test
    async def test_streaming_stocks(self):
        self._state = None
        cred.KEY = cred.KEY

        streamer = polygon.AsyncStreamClient(cred.KEY, 'stocks')
        await streamer.change_handler('status', self.message_handler)

        # subbing STOCK TRADES
        await streamer.subscribe_stock_trades(['AMD', 'NVDA', 'TSLA', 'MSFT', 'GOOG'], self.message_handler)
        asyncio.ensure_future(self.handle_messages(streamer))

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'T')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing STOCK TRADES
        await streamer.unsubscribe_stock_trades(['AMD', 'NVDA', 'TSLA', 'MSFT', 'GOOG'])

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'status')

        except AssertionError:
            await streamer.close_stream()
            raise

        # subbing STOCK QUOTES
        await streamer.subscribe_stock_quotes(['AMD', 'NVDA', 'TSLA', 'MSFT', 'GOOG'],
                                              handler_function=self.message_handler,
                                              force_uppercase_symbols=False)

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'Q')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing STOCK QUOTES
        await streamer.unsubscribe_stock_quotes(['AMD', 'NVDA', 'TSLA', 'MSFT', 'GOOG'])

        try:
            await asyncio.sleep(5)
            self.assertEqual(self._state, 'status')

        except AssertionError:
            await streamer.close_stream()
            raise

        # subbing STOCK SECOND AGGS
        await streamer.subscribe_stock_second_aggregates(['AMD', 'NVDA', 'TSLA', 'MSFT', 'GOOG'],
                                                         handler_function=self.message_handler)

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'A')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing STOCK SECOND AGGS
        await streamer.unsubscribe_stock_second_aggregates(['AMD', 'NVDA', 'TSLA', 'MSFT', 'GOOG'])

        try:
            await asyncio.sleep(10)
            self.assertEqual(self._state, 'status')

        except AssertionError:
            await streamer.close_stream()
            raise

        finally:
            await streamer.close_stream()


# ========================================================= #


class TestOptionsStream(unittest.TestCase):
    cred.KEY = cred.OK

    async def message_handler(self, msg):
        print(f'msg: {msg} || type: {type(msg)}')
        self._state = msg['ev']

    @staticmethod
    async def handle_messages(streamer, recon: bool = False):
        if recon:
            await streamer.handle_messages(recon)
            return

        while 1:
            await streamer.handle_messages()

    @async_test
    async def test_streaming_options(self):
        self._state = None

        streamer = polygon.AsyncStreamClient(cred.KEY, 'options')
        await streamer.change_handler('status', self.message_handler)

        # subbing OPTIONS TRADES
        await streamer.subscribe_option_trades(handler_function=self.message_handler,
                                               force_uppercase_symbols=False)
        asyncio.ensure_future(self.handle_messages(streamer))

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'T')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing OPTIONS TRADES
        await streamer.unsubscribe_option_trades()

        try:
            await asyncio.sleep(5)
            self.assertEqual(self._state, 'status')

        except AssertionError:
            await streamer.close_stream()
            raise

        # subbing OPTIONS QUOTES
        await streamer.subscribe_option_quotes(handler_function=self.message_handler)

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'Q')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing OPTIONS QUOTES
        await streamer.unsubscribe_option_quotes()

        try:
            await asyncio.sleep(5)
            self.assertEqual(self._state, 'status')

        except AssertionError:
            await streamer.close_stream()
            raise

        # subbing OPTIONS SECOND AGGREGATES
        await streamer.subscribe_option_second_aggregates(handler_function=self.message_handler)

        try:
            await asyncio.sleep(4)
            self.assertEqual(self._state, 'A')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing OPTIONS SECOND AGGREGATES
        await streamer.unsubscribe_option_second_aggregates()

        try:
            await asyncio.sleep(7)
            self.assertEqual(self._state, 'status')
        except AssertionError:
            await streamer.close_stream()
            raise

        finally:
            await streamer.close_stream()


# ========================================================= #


class TestForexStream(unittest.TestCase):
    cred.KEY = cred.CK

    async def message_handler(self, msg):
        print(f'msg: {msg} || type: {type(msg)}')
        self._state = msg['ev']

    @staticmethod
    async def handle_messages(streamer, recon: bool = False):
        if recon:
            await streamer.handle_messages(recon)
            return

        while 1:
            await streamer.handle_messages()

    @async_test
    async def test_streaming_forex(self):
        self._state = None

        streamer = polygon.AsyncStreamClient(cred.KEY, 'forex')
        await streamer.change_handler('status', self.message_handler)

        # subbing FOREX QUOTES
        await streamer.subscribe_forex_quotes(['EUR/USD', 'C:USD/EUR', 'AUD/USD'],
                                              handler_function=self.message_handler,
                                              force_uppercase_symbols=False)
        asyncio.ensure_future(self.handle_messages(streamer))

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'C')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing FOREX QUOTES
        await streamer.unsubscribe_forex_quotes(['EUR/USD', 'C:USD/EUR', 'AUD/USD'])

        try:
            await asyncio.sleep(4)
            self.assertTrue(self._state in ['C', 'status'])

        except AssertionError:
            await streamer.close_stream()
            raise

        finally:
            await streamer.close_stream()


# ========================================================= #


class TestCryptoStream(unittest.TestCase):
    cred.KEY = cred.CK

    async def message_handler(self, msg):
        print(f'msg: {msg} || type: {type(msg)}')
        self._state = msg['ev']

    @staticmethod
    async def handle_messages(streamer, recon: bool = False):
        if recon:
            await streamer.handle_messages(recon)
            return

        while 1:
            await streamer.handle_messages()

    @async_test
    async def test_streaming_crypto(self):
        self._state = None

        streamer = polygon.AsyncStreamClient(cred.KEY, 'crypto')
        await streamer.change_handler('status', self.message_handler)

        # subbing CRYPTO TRADES
        await streamer.subscribe_crypto_trades(['BTC-USD', 'X:LTC-USD'], handler_function=self.message_handler,
                                               force_uppercase_symbols=False)
        asyncio.ensure_future(self.handle_messages(streamer))

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'XT')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing CRYPTO TRADES
        await streamer.unsubscribe_crypto_trades(['BTC-USD', 'X:LTC-USD'])

        try:
            await asyncio.sleep(6)
            self.assertTrue(self._state in ['XT', 'status'])

        except AssertionError:
            await streamer.close_stream()
            raise

        # subbing CRYPTO QUOTES
        await streamer.subscribe_crypto_quotes(['BTC-USD', 'X:LTC-USD'], handler_function=self.message_handler)
        asyncio.ensure_future(self.handle_messages(streamer))

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'XQ')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing CRYPTO QUOTES
        await streamer.unsubscribe_crypto_quotes(['BTC-USD', 'X:LTC-USD'])

        try:
            await asyncio.sleep(6)
            self.assertTrue(self._state in ['XQ', 'status'])

        except AssertionError:
            await streamer.close_stream()
            raise

        # subbing CRYPTO LEVEL2 BOOK
        await streamer.subscribe_crypto_level2_book(['BTC-USD', 'X:LTC-USD'], handler_function=self.message_handler)
        asyncio.ensure_future(self.handle_messages(streamer))

        try:
            await asyncio.sleep(3)
            self.assertEqual(self._state, 'XL2')
        except AssertionError:
            await streamer.close_stream()
            raise

        # unsubbing CRYPTO LEVEL2 BOOK
        await streamer.unsubscribe_crypto_level2_book(['BTC-USD', 'X:LTC-USD'])

        try:
            await asyncio.sleep(6)
            self.assertTrue(self._state in ['XL2', 'status'])

        except AssertionError:
            await streamer.close_stream()
            raise

        finally:
            await streamer.close_stream()


# ========================================================= #

if __name__ == '__main__':
    unittest.main()

# ========================================================= #
