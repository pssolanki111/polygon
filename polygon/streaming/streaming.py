# ========================================================= #
import os
import websocket as ws_client
import threading
import signal
import asyncio
from typing import Union
from enum import Enum
import time
import logging
# ========================================================= # TODO: add auto reconnection


STOCKS = 'stocks'
OPTIONS = 'options'
CRYPTO = 'crypto'
FOREX = 'forex'
HOST = 'socket.polygon.io'
DELAYED_HOST = 'delayed.polygon.io'


# ========================================================= #


def get_logger():
    return logging.getLogger(__name__)


# ========================================================= #


class StreamClient:
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    Note that this is callback based stream client which is suitable for threaded/multi-processed applications. If
    you need to stream using an ``asyncio`` based stream client, see :ref:`async_streamer_client_interface_header`.

    This class implements all the websocket endpoints. Note that you should always import names from top level.
    eg: ``from polygon import StreamClient`` or ``import polygon`` (which allows you to access all names easily)

    Creating the client is as simple as: ``client = StreamClient('MY_API_KEY', 'other_options')``

    Once you have the client, you can call its methods to subscribe/unsubscribe to streams, change handlers and
    process messages. All methods have sane default values and almost everything can be customized.

    Type Hinting tells you what data type a parameter is supposed to be. You should always use ``enums`` for most
    parameters to avoid supplying error prone values.

    Take a look at the `Official documentation <https://polygon.io/docs/websockets/getting-started>`__
    to get an idea of the stream, data formatting for messages and related useful stuff.
    """
    def __init__(self, api_key: str, cluster: str, host: str = HOST, on_message=None, on_close=None,
                 on_error=None, enable_connection_logs: bool = False):
        """
        Initializes the callback function based stream client
        `Official Docs <https://polygon.io/docs/websockets/getting-started>`__

        :param api_key: Your API Key. Visit your dashboard to get yours.
        :param cluster: Which market/cluster to connect to. See :class:`polygon.enums.StreamCluster` for choices.
                        NEVER connect to the same cluster again if there is an existing stream connected to it.
                        The existing connection would be dropped and new one will be established. You can have up to 4
                        concurrent streams connected to 4 different clusters.
        :param host: Host url to connect to. Default is real time. See :class:`polygon.enums.StreamHost` for choices.
        :param on_message: The function to be called when data is received. This is primary function you'll write to
                           process the data from the stream. The function should accept one and only one ``arg``
                           (message). Default handler is :meth:`_default_on_msg`.
        :param on_close: The function to be called when stream is closed. Function should accept two args (
                         close_status_code, close_message). Default handler is :meth:`_default_on_close`
        :param on_error: Function to be called when an error is encountered. Function should accept one arg (
                         exception object). Default handler is :meth:`_default_on_error`
        :param enable_connection_logs: Whether or not to print debug info related to the stream connection.
                                       Helpful for debugging.
        """

        if enable_connection_logs:  # enable connection logs if requested.
            ws_client.enableTrace(True)

        self._host, self._url, self.KEY = host, f'wss://{host}/{cluster}', api_key

        self._ping_interval, self._ping_timeout, self._ping_payload = None, None, None

        self._skip_utf8_validation, self._enable_connection_logs = None, enable_connection_logs

        self.WS = ws_client.WebSocketApp(self._url, on_message=self._default_on_msg, on_close=self._default_on_close,
                                         on_error=self._default_on_error, on_open=self._default_on_open)

        self.WS.on_close = on_close if on_close else self._default_on_close
        self.WS.on_error = on_error if on_error else self._default_on_error
        self.WS.on_message = on_message if on_message else self._default_on_msg

        self._auth = threading.Event()  # to ensure we are logged in before sending any communication.

        self._run_in_thread: Union[threading.Thread, None] = None

    # Context managers
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.WS.close()
        return 

    def _start_stream(self, ping_interval: int = 21, ping_timeout: int = 20, ping_payload: str = '',
                      skip_utf8_validation: bool = True):
        """
        Starts the Stream Event Loop. The loop is infinite and will continue to run until the stream is
        terminated, either manually or due to an exception. This method is for internal use only. you should always
        use :meth:`start_stream_thread` to start the stream.

        :param ping_interval: client would send a ``ping`` every specified number of seconds to server to keep
                              connection alive. Set to 0 to disable pinging. Defaults to 21 seconds
        :param ping_timeout: Timeout in seconds if a ``pong`` (response to ping from server) is not received. The Stream
                             is terminated as it is considered to be dead if no pong is received within the specified
                             timeout. default: 20 seconds
        :param ping_payload: The option message to be sent with the ping. Better to leave it empty string.
        :param skip_utf8_validation: Whether to skip utf validation of messages. Defaults to True. Setting it to
                                     False may result in `performance downgrade
                                     <https://websocket-client.readthedocs.io/en/latest/faq.html#why-is-this-library
                                     -slow>`__
        :return: None
        """

        self._ping_interval, self._ping_timeout, self._ping_payload = ping_interval, ping_timeout, ping_payload

        self._skip_utf8_validation = skip_utf8_validation

        self.WS.run_forever(ping_interval=self._ping_interval, ping_timeout=self._ping_timeout,
                            ping_payload=self._ping_payload, skip_utf8_validation=self._skip_utf8_validation)

    def start_stream_thread(self, ping_interval: int = 21, ping_timeout: int = 20, ping_payload: str = '',
                            skip_utf8_validation: bool = True):
        """
        Starts the Stream. This will not block the main thread and it spawns the streamer in its own thread.

        :param ping_interval: client would send a ``ping`` every specified number of seconds to server to keep
                              connection alive. Set to 0 to disable pinging. Defaults to 21 seconds
        :param ping_timeout: Timeout in seconds if a ``pong`` (response to ping from server) is not received. The Stream
                             is terminated as it is considered to be dead if no pong is received within the specified
                             timeout. default: 20 seconds
        :param ping_payload: The option message to be sent with the ping. Better to leave it empty string.
        :param skip_utf8_validation: Whether to skip utf validation of messages. Defaults to True. Setting it to
                                     False may result in `performance downgrade
                                     <https://websocket-client.readthedocs.io/en/latest/faq.html#why-is-this-library
                                     -slow>`__
        :return: None
        """

        self._run_in_thread = threading.Thread(target=self._start_stream,
                                               args=(ping_interval, ping_timeout, ping_payload, skip_utf8_validation))
        self._run_in_thread.start()

    def close_stream(self, *args, **kwargs):
        """
        Close the websocket connection. Wait for thread to finish if running.
        """

        get_logger().info('Terminating Stream...')

        self.WS.close()

        if self._run_in_thread:
            self._run_in_thread.join()

        get_logger().info('Terminated')

    def _authenticate(self):
        """
        Authenticates the client with the server using API key. Internal function, not meant to be called directly
        by users.

        :return: None
        """

        _payload = '{"action":"auth","params":"%s"}' % self.KEY  # f-strings were trippin' here.

        self.WS.send(_payload)

        time.sleep(1)

        self._auth.set()

    # STOCKS Streams
    def subscribe_stock_trades(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time trades for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is ``*`` which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'T.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_trades(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_stock_trades(symbols, action='unsubscribe')

    def subscribe_stock_quotes(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Quotes for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'Q.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_quotes(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_stock_quotes(symbols, action='unsubscribe')

    def subscribe_stock_minute_aggregates(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time minute aggregates for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'AM.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_minute_aggregates(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_stock_minute_aggregates(symbols, action='unsubscribe')

    def subscribe_stock_seconds_aggregates(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time second aggregates for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'A.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_seconds_aggregates(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_stock_seconds_aggregates(symbols, action='unsubscribe')

    def subscribe_stock_limit_up_limit_down(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time LULD events for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'LULD.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_limit_up_limit_down(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_stock_limit_up_limit_down(symbols, action='unsubscribe')

    def subscribe_stock_imbalances(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Imbalance Events for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'NOI.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_imbalances(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_stock_imbalances(symbols, action='unsubscribe')

    # OPTIONS Streams
    def subscribe_option_trades(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Options Trades for given Options contract.

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'T.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_option_trades(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_option_trades(symbols, action='unsubscribe')

    def subscribe_option_minute_aggregates(self, tickers: list = None, action: str = 'subscribe'):
        """
        Stream real-time Options Minute Aggregates for given Options contract(s).

        :param tickers: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'AM.'

        if tickers is None:
            tickers = _prefix + '*'

        else:
            tickers = ','.join([_prefix + symbol.upper() for symbol in tickers])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), tickers)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_option_minute_aggregates(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_option_minute_aggregates(symbols, action='unsubscribe')

    def subscribe_option_second_aggregates(self, tickers: list = None, action: str = 'subscribe'):
        """
        Stream real-time Options Second Aggregates for given Options contract(s).

        :param tickers: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'A.'

        if tickers is None:
            tickers = _prefix + '*'

        else:
            tickers = ','.join([_prefix + symbol.upper() for symbol in tickers])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), tickers)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise
        
    def unsubscribe_option_second_aggregates(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_option_second_aggregates(symbols, action='unsubscribe')

    # FOREX Streams
    def subscribe_forex_quotes(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time forex quotes for given forex pair(s).

        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'C.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)
        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_forex_quotes(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_forex_quotes(symbols, action='unsubscribe')

    def subscribe_forex_minute_aggregates(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time forex Minute Aggregates for given forex pair(s).

        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'CA.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_forex_minute_aggregates(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_forex_minute_aggregates(symbols, action='unsubscribe')

    # CRYPTO Streams
    def subscribe_crypto_trades(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Trades for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'XT.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_crypto_trades(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_crypto_trades(symbols, action='unsubscribe')

    def subscribe_crypto_quotes(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Quotes for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'XQ.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_crypto_quotes(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_crypto_quotes(symbols, action='unsubscribe')

    def subscribe_crypto_minute_aggregates(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Minute Aggregates for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'XA.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_crypto_minute_aggregates(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_crypto_minute_aggregates(symbols, action='unsubscribe')

    def subscribe_crypto_level2_book(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time level 2 book data for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``
        :param action: Action to be taken. To be used internally. Defaults to subscribe. Options: unsubscribe.
        :return: None
        """

        _prefix = 'XL2.'

        if symbols is None:
            symbols = _prefix + '*'

        else:
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:   
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_crypto_level2_book(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""
        self.subscribe_crypto_level2_book(symbols, action='unsubscribe')

    @staticmethod
    def _default_on_msg(_ws: ws_client.WebSocketApp, msg):
        """
        Default handler for message processing

        :param msg: The message as received from the server
        :return: None
        """

        print('message received:\n', str(msg))

    @staticmethod
    def _default_on_close(_ws: ws_client.WebSocketApp, close_code, msg):
        """
        THe default function to be called when stream is closed.

        :param close_code: The close code as received from server
        :param msg: The close message as received from server
        :return:
        """

        if close_code is None:
            return

        print(f'Closed. Close Code: {close_code} || Args: {None if msg == "" else msg}\nMost common reason for '
              f'stream to be closed is incorrect API key OR internet issues')

    @staticmethod
    def _default_on_error(_ws: ws_client.WebSocketApp, error, *args):
        """
        Default function to be called when an error is encountered.

        :param error: The exception object as supplied by the handler
        :return: None
        """

        print('Error Encountered:\n', str(error))

    def _default_on_open(self, _ws: ws_client.WebSocketApp, *args):
        """
        Default function to be called when stream client is initialized. Takes care of the authentication.

        :param args: Any args supplied by the handler
        :return: None
        """

        self._authenticate()


# ========================================================= #


if __name__ == '__main__':
    print('Don\'t You Dare Running Lib Files Directly')


# ========================================================= #
