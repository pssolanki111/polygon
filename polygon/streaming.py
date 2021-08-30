# ========================================================= #
import websockets as wss
import websocket as ws_client
import threading
import signal
import asyncio
import inspect
import json
from typing import Union
from enum import Enum
import time
import logging
# ========================================================= # TODO: Write Enums for all endpoints


STOCKS = 'stocks'
CRYPTO = 'crypto'
FOREX = 'forex'
HOST = 'socket.polygon.io'
DELAYED_HOST = 'delayed.polygon.io'


# ========================================================= #


def get_logger():
    return logging.getLogger(__name__)


# ========================================================= #


class StreamClient:
    def __init__(self, api_key: str, market: str = STOCKS, host: str = HOST, on_message=None, on_close=None,
                 on_error=None, enable_connection_logs: bool = False):
        """
        Initializes the stream connection.
        Official Docs: https://polygon.io/docs/websockets/getting-started
        :param api_key: Your API Key. Visit your dashboard to get the API key.
        :param market: Which market/cluster to connect to. Default 'stocks'. Options: 'crypto', 'forex'
        :param host: Host url to connect to. Default is real time. Change to polygon.DELAYED_HOST for delayed stream
        on stocks websockets stream only.
        :param on_message: The function to be called when data is received. This is primary function you'll write to
        process the data from the stream. The function should accept one and only one arg (message).
        :param on_close: The function to be called when stream is closed. Function should accept two args (
          close_status_code, close_message)
        :param on_error: Function to be called when an error is encountered. Function should accept one arg (
         exception object)
        :param enable_connection_logs: Whether or not to print useful debug info related to the stream connection.
        Helpful for trying to debug something. Defaults to False.
        """

        if enable_connection_logs:  # enable connection logs if requested.
            ws_client.enableTrace(True)

        self._host, self._url, self.KEY = host, f'wss://{host}/{market}', api_key

        self._ping_interval, self._ping_timeout, self._ping_payload = None, None, None

        self._skip_utf8_validation, self._enable_connection_logs = None, enable_connection_logs

        self.WS = ws_client.WebSocketApp(self._url, on_message=self._default_on_msg, on_close=self._default_on_close,
                                         on_error=self._default_on_error, on_open=self._default_on_open)

        self.WS.on_close = on_close if on_close else self._default_on_close
        self.WS.on_error = on_error if on_error else self._default_on_error
        self.WS.on_message = on_message if on_message else self._default_on_msg

        self._auth = threading.Event()  # to ensure we are logged in before sending any communication.

        self._run_in_thread: Union[threading.Thread, None] = None

        # signal Handlers. Can be overridden by user.
        signal.signal(signal.SIGINT, self.close_stream)
        signal.signal(signal.SIGTERM, self.close_stream)

    def _start_stream(self, ping_interval: int = 21, ping_timeout: int = 20, ping_payload: str = '',
                      skip_utf8_validation: bool = True):
        """
        Starts the Stream Event Loop. The loop is infinite and will continue to run until the stream is
        terminated, either manually or due to an exception.This method is for internal use only.
        ALWAYS start your streams using client.start_stream_thread.
        :param ping_interval: client would send a ping every specified number of seconds to server to keep connection
        alive. Set to 0 to disable pinging. Defaults to 21 seconds
        :param ping_timeout: Timeout in seconds if a pong (response to ping from server) is not received. The Stream
        is terminated as it is considered to be dead if no pong is received within the specified timeout. default: 20
        :param ping_payload: The option message to be sent with the ping. Better to leave it empty string.
        :param skip_utf8_validation: Whether to skip utf validation of messages. Defaults to True. Setting it to
        False may result in performance downgrade.
        :return: None
        """

        self._ping_interval, self._ping_timeout, self._ping_payload = ping_interval, ping_timeout, ping_payload

        self._skip_utf8_validation = skip_utf8_validation

        self.WS.run_forever(ping_interval=self._ping_interval, ping_timeout=self._ping_timeout,
                            ping_payload=self._ping_payload, skip_utf8_validation=self._skip_utf8_validation)

    def start_stream_thread(self, ping_interval: int = 21, ping_timeout: int = 20, ping_payload: str = '',
                            skip_utf8_validation: bool = True):
        """
        Starts the Stream event loop in a thread. This will not block the main thread. Useful for GUI applications
        and use cases where you have more than one event loop in general
        :param ping_interval: client would send a ping every specified number of seconds to server to keep connection
        alive. Set to 0 to disable pinging. Defaults to 21 seconds
        :param ping_timeout: Timeout in seconds if a pong (response to ping from server) is not received. The Stream
        is terminated as it is considered to be dead if no pong is received within the specified timeout. default: 20
        :param ping_payload: The option message to be sent with the ping. Better to leave it empty string.
        :param skip_utf8_validation: Whether to skip utf validation of messages. Defaults to True. Setting it to
        False may result in performance downgrade.
        :return: None
        """

        self._run_in_thread = threading.Thread(target=self._start_stream,
                                               args=(ping_interval, ping_timeout, ping_payload, skip_utf8_validation))
        self._run_in_thread.start()

    def close_stream(self, *args, **kwargs):
        """
        Close the websocket connection. Wait for thread to finish if running.
        :param args: Arguments supplied by signal handlers
        :param kwargs: KWArguments supplied by signal handlers
        :return: None
        """

        get_logger().info('Terminating Stream...')

        self.WS.close()

        if self._run_in_thread:
            self._run_in_thread.join()

        get_logger().info('Terminated')

    def _authenticate(self):
        """
        Authenticates the client with the server using API key.
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

    def unsubscribe_stock_trades(self, symbols: list = None):
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_quotes(self, symbols: list = None):
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_minute_aggregates(self, symbols: list = None):
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_seconds_aggregates(self, symbols: list = None):
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_limit_up_limit_down(self, symbols: list = None):
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

        _payload = '{"action":"subscribe", "params":"%s"}' % symbols

        try:
            # Ensuring we are logged in and the socket is open to receive subscription messages
            self._auth.wait()

            self.WS.send(_payload)

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_stock_imbalances(self, symbols: list = None):
        self.subscribe_stock_imbalances(symbols, action='unsubscribe')

    # FOREX Streams
    def subscribe_forex_quotes(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time forex quotes for given forex pair(s).
        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
        each Ticker must be in format: from/to. For example: USD/CNH
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
        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_forex_quotes(self, symbols: list = None):
        self.subscribe_forex_quotes(symbols, action='unsubscribe')

    def subscribe_forex_minute_aggregates(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time forex Minute Aggregates for given forex pair(s).
        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
        each Ticker must be in format: from/to. For example: USD/CNH
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_forex_minute_aggregates(self, symbols: list = None):
        self.subscribe_forex_minute_aggregates(symbols, action='unsubscribe')

    # CRYPTO Streams
    def subscribe_crypto_trades(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Trades for given cryptocurrency pair(s).
        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
        each Ticker must be in format: from-to. For example: BTC-USD
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_crypto_trades(self, symbols: list = None):
        self.subscribe_crypto_trades(symbols, action='unsubscribe')

    def subscribe_crypto_quotes(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Quotes for given cryptocurrency pair(s).
        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
        each Ticker must be in format: from-to. For example: BTC-USD
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_crypto_quotes(self, symbols: list = None):
        self.subscribe_crypto_quotes(symbols, action='unsubscribe')

    def subscribe_crypto_minute_aggregates(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time Minute Aggregates for given cryptocurrency pair(s).
        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
        each Ticker must be in format: from-to. For example: BTC-USD
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_crypto_minute_aggregates(self, symbols: list = None):
        self.subscribe_crypto_minute_aggregates(symbols, action='unsubscribe')

    def subscribe_crypto_level2_book(self, symbols: list = None, action: str = 'subscribe'):
        """
        Stream real-time level 2 book data for given cryptocurrency pair(s).
        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
        each Ticker must be in format: from-to. For example: BTC-USD
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

        except ws_client._exceptions.WebSocketConnectionClosedException:  # TODO: inspect the behavior when market opens
            get_logger().error('Login Failed. Please recheck your API key and try again.')
            return

        except Exception:
            raise

    def unsubscribe_crypto_level2_book(self, symbols: list = None):
        self.subscribe_crypto_level2_book(symbols, action='unsubscribe')

    @staticmethod
    def _default_on_msg(_ws: ws_client.WebSocketApp, msg):
        """
        Default handler for message processing
        :param msg: The message as received from the server
        :param args: Other args supplied by the handler
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


class AsyncStreamClient:
    def __init__(self, api_key: str, host: str = HOST, market: str = STOCKS, ping_interval: int = 20,
                 ping_timeout: bool = 19, max_message_size: int = 1048576, max_memory_queue: int = 32,
                 read_limit: int = 65536, write_limit: int = 65536):
        """
        Initializes the stream client for async streaming.
        Official Docs: https://polygon.io/docs/websockets/getting-started
        :param api_key: Your API Key. Visit your dashboard to get the API key.
        :param market: Which market/cluster to connect to. Default 'stocks'. Options: 'crypto', 'forex'
        :param host: Host url to connect to. Default is real time. Change to polygon.DELAYED_HOST for delayed stream
        on stocks websockets stream only.
        :param ping_interval: Send a ping to server every specified number of seconds to keep the connection alive.
        Defaults to 20 seconds. Setting to 0 disables pinging.
        :param ping_timeout: The number of seconds to wait after sending a ping for the response (pong). If no
        response is received from the server in those many seconds, stream is considered dead and exits with code
        1011. Defaults to 19 seconds.
        :param max_message_size: The max_size parameter enforces the maximum size for incoming messages in bytes. The
        default value is 1 MiB. None disables the limit. If a message larger than the maximum size is received,
         recv() will raise ConnectionClosedError and the connection will be closed with code 1009
        :param max_memory_queue: sets the maximum length of the queue that holds incoming messages. The default value
        is 32. None disables the limit. Messages are added to an in-memory queue when they’re received; then recv()
        pops from that queue
        :param read_limit: sets the high-water limit of the buffer for incoming bytes. The low-water limit is half the
        high-water limit. The default value is 64 KiB, half of asyncio’s default
        :param write_limit: The write_limit argument sets the high-water limit of the buffer for outgoing bytes. The
         low-water limit is a quarter of the high-water limit. The default value is 64 KiB, equal to asyncio’s default
        """
        self.KEY, self._market, self.WS = api_key, market, None

        self._apis, self._handlers = self._default_handlers_and_apis()

        self._url = f'wss://{host}/{self._market}'

        self._ping_interval, self._ping_timeout = ping_interval, ping_timeout

        self._max_message_size, self._max_memory_queue = max_message_size, max_memory_queue

        self._read_limit, self._write_limit, self._auth = read_limit, write_limit, False

    async def login(self) -> wss.WebSocketClientProtocol:
        """
        Creates Websocket Socket client using the configuration and Logs to the stream with credentials.
        :return: None
        """

        self.WS = await wss.connect(self._url, ping_interval=self._ping_interval, ping_timeout=self._ping_timeout,
                                    max_size=self._max_message_size, max_queue=self._max_memory_queue,
                                    read_limit=self._read_limit, write_limit=self._write_limit)

        _payload = '{"action":"auth","params":"%s"}' % self.KEY  # f-strings were trippin' here.

        await self.WS.send(_payload)

        self._auth = True

    async def _send(self, data: str):
        """
        Internal function to send data to websocket endpoints
        :param data: The formatted string to be sent.
        :return: None
        """

        if self.WS is None:
            raise ValueError('Looks like the socket is not open. Login Failed')

        get_logger().debug(f'Sending Data: {str(data)}')

        await self.WS.send(str(data))

    async def _recv(self):
        """
        Internal function to receive messages from websocket endpoints.
        :return: The JSON decoded message data.
        """

        if self.WS is None:
            raise ValueError('Looks like the socket is not open. Login Failed')

        _raw = await self.WS.recv()

        try:
            _data = json.loads(_raw)

        except json.decoder.JSONDecodeError as exc:
            msg = f'Unable to decode message string: {_raw}.\nUsually happens with invalid symbols.\nException ' \
                  f'Message: {str(exc)}'
            raise ValueError(msg)

        return _data

    async def start_stream(self, reconnect: bool = False, max_reconnection_attempts: Union[int, bool] = 5):
        """
        The Main method to start the stream. Allows Reconnecting by simply specifying a parameter.
        :param reconnect: Defaults to False. Setting True creates an inner loop which traps disconnection errors
        except Login failed and other unknown errors, and reconnects to the stream with the same subscription it had
        earlier before getting disconnected.
        :param max_reconnection_attempts: Determines max how many times should the program attempt to reconnect in
        case of failed attempts. The Counter is reset as soon as a successful connection is re-established. Setting
        to False disables the limit which is NOT recommended unless you know you got a situation.
        :return: None
        """
        if not self._auth:
            await self.login()

        if not reconnect:
            _msg = await self._recv()

            for msg in _msg:
                asyncio.create_task(self._handlers[self._apis[msg['ev']]](msg))

            return

        if not (isinstance(max_reconnection_attempts, int) or max_reconnection_attempts is False):
            raise ValueError('max_reconnection_attempts must be a positive whole number or False (False NOT '
                             'recommended as it disables the limit)')

        if not max_reconnection_attempts:
            print('It is never recommended to allow Infinite reconnection attempts as this does not account for when '
                  'Server has an outage or client does not have access to internet. It is suggested to Re-start stream '
                  'with a finite limit for attempts')

        elif max_reconnection_attempts < 1:
            raise ValueError('max_reconnection_attempts must be a positive whole number')

        #

    @staticmethod
    async def _default_process_message(update):
        """
        The default Handler for Message Streams which were NOT initialized with a handler function
        :param update: The update message as received after decoding the message.
        :return: None
        """

        if update['ev'] == 'status':
            if update['status'] in ['auth_success', 'connected']:
                get_logger().info(update['message'])

            else:
                get_logger().error(update['message'])
                exit(21)

        print(update)

    def _default_handlers_and_apis(self):
        """Assign default handler value to all stream setups"""
        _handlers = {}

        _apis = {'T': 'stock_trades', 'Q': 'stock_quotes', 'AM': 'stock_agg_min', 'A': 'stock_agg_sec',
                 'LULD': 'stock_luld', 'NOI': 'stock_imbalances', 'C': 'forex_quotes', 'CA': 'forex_agg_min',
                 'XT': 'crypto_trades', 'XQ': 'crypto_quotes', 'XL2': 'crypto_l2', 'XA': 'crypto_agg_min',
                 'status': 'status'}

        for name in _apis.values():
            _handlers[name] = self._default_process_message

        return _apis, _handlers


# ========================================================= #


class SerialKiller:
    def __init__(self):
        self.kill_me = False
        signal.signal(signal.SIGINT, self.kill_me_slowly)
        signal.signal(signal.SIGTERM, self.kill_me_slowly)
        signal.signal(signal.SIGHUP, self.kill_me_slowly)

    def kill_me_slowly(self, signum, frame) -> None:
        self.kill_me = True
        get_logger().warning('Signal Received: ' + str(signum) + ' at frame: ' + str(frame))


# ========================================================= #


if __name__ == '__main__':
    print('Don\'t You Dare Running Lib Files Directly')
    # import antigravity  # Fly Me to The Moon
    from polygon import cred
    from pprint import pprint

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: (%(asctime)s) : %(message)s')

    async def test():
        client = AsyncStreamClient(cred.KEY)

        while 1:
            await client.start_stream()

    asyncio.run(test())

    # client = StreamClient(cred.KEY)
    # client.start_stream_thread()
    # # client.unsubscribe_stock_limit_up_limit_down(['AMD', 'PYPL'])
    # client.subscribe_stock_trades(['AMD', 'NVDA'])


# ========================================================= #
