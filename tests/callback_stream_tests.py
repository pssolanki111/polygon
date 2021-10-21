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
        streamer.subscribe_stock_trades(['AMD', 'NVDA'])
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
        time.sleep(2)

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

    def test_streaming_options(self):
        cred.KEY = cred.OK
        self._state = None

        streamer = polygon.StreamClient(cred.KEY, 'options', on_message=self.message_handler)
        streamer.start_stream_thread()

        # subbing OPTIONS TRADES
        streamer.subscribe_option_trades()
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


class TestOptionsStream(unittest.TestCase):
    pass


# ========================================================= #


class TestForexStream(unittest.TestCase):
    pass


# ========================================================= #


class TestCryptoStream(unittest.TestCase):
    pass


# ========================================================= #

if __name__ == '__main__':
    unittest.main()

# ========================================================= #
