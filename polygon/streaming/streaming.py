# ========================================================= #
import logging
import threading
import time
from typing import Union
import websocket as ws_client
from enum import Enum

# ========================================================= #


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

    def __init__(self, api_key: str, cluster, host=HOST, on_message=None, on_close=None,
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

        self._host, self.KEY, self._cluster = self._change_enum(host, str), api_key, self._change_enum(cluster, str)

        self._url, self._re, self._attempts = f'wss://{self._host}/{self._cluster}', None, 0

        self._subs = []

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

    def start_stream_thread(self, reconnect: bool = False, max_reconnection_attempts=5, reconnection_delay=5,
                            ping_interval: int = 21, ping_timeout: int = 20,  ping_payload: str = '',
                            skip_utf8_validation: bool = True):
        """
        Starts the Stream. This will not block the main thread and it spawns the streamer in its own thread.

        :param reconnect: If this is ``False`` (default), it starts the usual connection thread and calls your
                          callbacks when a msg is received. Uses the :meth:`_default_on_msg` if no callback was
                          specified. Setting it to True traps disconnection errors reconnects to the stream with the
                          same subscriptions it had earlier before getting disconnected. Note that if you define a
                          custom function for ``on_error`` callback, the reconnection would not work.
        :param max_reconnection_attempts: Determines how many times should the program attempt to reconnect in
                                          case of failed attempts. The Counter is reset as soon as a successful
                                          connection is re-established. Setting it to False disables the limit which is
                                          NOT recommended unless you know you got a situation. This value is ignored
                                          if ``reconnect`` is False (The default). Defaults to 5.
        :param reconnection_delay: Number of seconds to wait before attempting to reconnect after a failed
                                   reconnection attempt or a disconnection. This value is ignored if ``reconnect``
                                   is False (the default). Defaults to 5.
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

        try:
            self._run_in_thread = threading.Thread(target=self._start_stream, args=(
                                                   ping_interval, ping_timeout, ping_payload, skip_utf8_validation))
            self._run_in_thread.start()

        except Exception as exc:
            print(f'error encountered: {str(exc)}')

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

    def _modify_sub(self, symbols=None, action='subscribe', _prefix='T.'):
        """
        Internal Function to send subscribe or unsubscribe requests to websocket. You should prefer using the
        corresponding methods to subscribe or unsubscribe to streams.

        :param symbols: The list of symbols to apply the actions to.
        :param action: Defaults to subscribe which subscribes to requested stream. Change to unsubscribe to remove an
                       existing subscription.
        :param _prefix: prefix of the stream service. See :class:`polygon.enums.StreamServicePrefix` for choices.
        :return: None
        """

        if symbols in [None, [], 'all']:
            symbols = _prefix + '*'

        elif isinstance(symbols, str):
            pass

        else:
            if self._cluster in ['options']:
                symbols = ','.join([f'{_prefix}{ensure_prefix(symbol)}' for symbol in symbols])

            else:
                symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        self._subs.append((symbols, action))
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

    # STOCKS Streams
    def subscribe_stock_trades(self, symbols: list = None):
        """
        Stream real-time trades for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is ``*`` which subscribes to ALL tickers in the market
        :return: None
        """

        _prefix = 'T.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_stock_trades(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""

        _prefix = 'T.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_stock_quotes(self, symbols: list = None):
        """
        Stream real-time Quotes for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :return: None
        """

        _prefix = 'Q.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_stock_quotes(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""

        _prefix = 'Q.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_stock_minute_aggregates(self, symbols: list = None):
        """
        Stream real-time minute aggregates for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :return: None
        """

        _prefix = 'AM.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_stock_minute_aggregates(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""

        _prefix = 'AM.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_stock_second_aggregates(self, symbols: list = None):
        """
        Stream real-time second aggregates for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :return: None
        """

        _prefix = 'A.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_stock_second_aggregates(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""

        _prefix = 'A.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_stock_limit_up_limit_down(self, symbols: list = None):
        """
        Stream real-time LULD events for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :return: None
        """

        _prefix = 'LULD.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_stock_limit_up_limit_down(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""

        _prefix = 'LULD.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_stock_imbalances(self, symbols: list = None):
        """
        Stream real-time Imbalance Events for given stock ticker symbol(s).

        :param symbols: A list of tickers. Default is * which subscribes to ALL tickers in the market
        :return: None
        """

        _prefix = 'NOI.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_stock_imbalances(self, symbols: list = None):
        """Unsubscribe from the stream service for the symbols specified. Defaults to all symbols."""

        _prefix = 'NOI.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    # OPTIONS Streams
    def subscribe_option_trades(self, symbols: list = None):
        """
        Stream real-time Options Trades for given Options contract.

        :param symbols: A list of symbols. Default is * which subscribes to ALL symbols in the market. you can pass
                        **with or without** the prefix ``O:``
        :return: None
        """

        _prefix = 'T.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_option_trades(self, symbols: list = None):
        """
        Unsubscribe real-time Options Trades for given Options contract.

        :param symbols: A list of symbols. Default is * which subscribes to ALL symbols in the market. you can pass
                        **with or without** the prefix ``O:``
        :return: None
        """

        _prefix = 'T.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_option_minute_aggregates(self, symbols: list = None):
        """
        Stream real-time Options Minute Aggregates for given Options contract(s).

        :param symbols: A list of symbols. Default is * which subscribes to ALL tickers in the market. you can pass
                        **with or without** the prefix ``O:``
        :return: None
        """

        _prefix = 'AM.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_option_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe real-time Options Minute aggregates for given Options contract.

        :param symbols: A list of symbols. Default is * which subscribes to ALL symbols in the market. you can pass
                        **with or without** the prefix ``O:``
        :return: None
        """

        _prefix = 'AM.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_option_second_aggregates(self, symbols: list = None):
        """
        Stream real-time Options Second Aggregates for given Options contract(s).

        :param symbols: A list of symbols. Default is * which subscribes to ALL tickers in the market. you can pass
                        **with or without** the prefix ``O:``
        :return: None
        """

        _prefix = 'A.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_option_second_aggregates(self, symbols: list = None):
        """
        Unsubscribe real-time Options Second Aggregates for given Options contract.

        :param symbols: A list of symbols. Default is * which subscribes to ALL symbols in the market. you can pass
                        **with or without** the prefix ``O:``
        :return: None
        """

        _prefix = 'A.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    # FOREX Streams
    def subscribe_forex_quotes(self, symbols: list = None):
        """
        Stream real-time forex quotes for given forex pair(s).

        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``.
        :return: None
        """

        _prefix = 'C.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_forex_quotes(self, symbols: list = None):
        """
        Unsubscribe from the stream service for the symbols specified. Defaults to all symbols.

        :param symbols: A list of forex tickers. Default is * which unsubscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``.
        """

        _prefix = 'C.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_forex_minute_aggregates(self, symbols: list = None):
        """
        Stream real-time forex Minute Aggregates for given forex pair(s).

        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``.
        :return: None
        """

        _prefix = 'CA.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_forex_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream service for the symbols specified. Defaults to all symbols.

        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``.
        """

        _prefix = 'CA.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    # CRYPTO Streams
    def subscribe_crypto_trades(self, symbols: list = None):
        """
        Stream real-time Trades for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XT.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_crypto_trades(self, symbols: list = None):
        """
        Unsubscribe real-time trades for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XT.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_crypto_quotes(self, symbols: list = None):
        """
        Stream real-time Quotes for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XQ.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_crypto_quotes(self, symbols: list = None):
        """
        Unsubscribe real-time quotes for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XQ.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_crypto_minute_aggregates(self, symbols: list = None):
        """
        Stream real-time Minute Aggregates for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XA.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_crypto_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe real-time minute aggregates for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XA.'

        self._modify_sub(symbols, 'unsubscribe', _prefix)

    def subscribe_crypto_level2_book(self, symbols: list = None):
        """
        Stream real-time level 2 book data for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XL2.'

        self._modify_sub(symbols, 'subscribe', _prefix)

    def unsubscribe_crypto_level2_book(self, symbols: list = None):
        """
        Unsubscribe real-time level 2 book data for given cryptocurrency pair(s).

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XL2.'

        self._modify_sub(symbols, 'subscribe', _prefix)

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

    @staticmethod
    def _change_enum(val: Union[str, Enum, float, int], allowed_type=str):
        if isinstance(val, Enum):
            try:
                return val.value

            except AttributeError:
                raise ValueError(f'The value supplied: ({val}) does not match the required type: ({allowed_type}). '
                                 f'Please consider using the  specified enum in the docs for this function or recheck '
                                 f'the value supplied.')

        if isinstance(allowed_type, list):
            if type(val) in allowed_type:
                return val

            raise ValueError(f'The value supplied: ({val}) does not match the required type: ({allowed_type}). '
                             f'Please consider using the  specified enum in the docs for this function or recheck '
                             f'the value supplied.')

        if isinstance(val, allowed_type) or val is None:
            return val

# ========================================================= #


def ensure_prefix(symbol: str, _prefix: str = 'O:'):
    """
    ensuring prefixes in symbol names. to be used internally by forex, crypto and options

    :param symbol: the symbol to check
    :param _prefix: which prefix to check for. defaults to ``O:`` which is for options
    :return: capitalized prefixed symbol.
    """

    if symbol.upper().startswith(_prefix) or symbol == '*':
        return symbol.upper()

    return f'{_prefix}{symbol.upper()}'

# ========================================================= #


if __name__ == '__main__':
    print('Don\'t You Dare Running Lib Files Directly')

# ========================================================= #
