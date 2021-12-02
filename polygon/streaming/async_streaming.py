# ========================================================= #
import asyncio
import inspect
import json
import logging
import sys
from typing import Union
import websockets as wss
from enum import Enum

# ========================================================= #


HOST = 'socket.polygon.io'
DELAYED_HOST = 'delayed.polygon.io'


# ========================================================= #


def get_logger():
    return logging.getLogger(__name__)


# ========================================================= #


class AsyncStreamClient:
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    Note that this is asyncio based stream client which is suitable for async applications. If
    you need to stream using an ``callback`` based stream client, see :ref:`callback_streamer_client_interface_header`.

    This class implements all the websocket endpoints. Note that you should always import names from top level.
    eg: ``from polygon import AsyncStreamClient`` or ``import polygon`` (which allows you to access all names easily)

    Creating the client is as simple as: ``client = AsyncStreamClient('MY_API_KEY', 'other_options')``

    Once you have the client, you can call its methods to subscribe/unsubscribe to streams, change handlers and
    process messages. All methods have sane default values and almost everything can be customized.

    Type Hinting tells you what data type a parameter is supposed to be. You should always use ``enums`` for most
    parameters to avoid supplying error prone values.

    Take a look at the `Official documentation <https://polygon.io/docs/websockets/getting-started>`__
    to get an idea of the stream, data formatting for messages and related useful stuff.
    """
    def __init__(self, api_key: str, cluster, host=HOST, ping_interval: int = 20,
                 ping_timeout: bool = 19, max_message_size: int = 1048576, max_memory_queue: int = 32,
                 read_limit: int = 65536, write_limit: int = 65536):
        """
        Initializes the stream client for async streaming
        `Official Docs <https://polygon.io/docs/websockets/getting-started>`__

        :param api_key: Your API Key. Visit your dashboard to get yours.
        :param cluster: Which market/cluster to connect to. See :class:`polygon.enums.StreamCluster` for choices.
                        NEVER connect to the same cluster again if there is an existing stream connected to it.
                        The existing connection would be dropped and new one will be established. You can have up to 4
                        concurrent streams connected to 4 different clusters.
        :param host: Host url to connect to. Default is real time. See :class:`polygon.enums.StreamHost` for choices
        :param ping_interval: Send a ``ping`` to server every specified number of seconds to keep the connection alive.
                              Defaults to 20 seconds. Setting to 0 disables pinging.
        :param ping_timeout: The number of seconds to wait after sending a ping for the response (``pong``). If no
                             response is received from the server in those many seconds, stream is considered dead
                             and exits with code ``1011``. Defaults to 19 seconds.
        :param max_message_size: The max_size parameter enforces the maximum size for incoming messages in bytes. The
                                 default value is ``1 MiB`` (not MB). None disables the limit. If a message larger
                                 than the maximum size is received, ``recv()`` will raise ``ConnectionClosedError``
                                 and the connection will be closed with code ``1009``
        :param max_memory_queue: sets the maximum length of the queue that holds incoming messages. The default value
                                 is ``32``. None disables the limit. Messages are added to an in-memory queue when
                                 they’re received; then ``recv()`` pops from that queue
        :param read_limit: sets the high-water limit of the buffer for incoming bytes. The low-water limit is half the
                           high-water limit. The default value is ``64 KiB``, half of asyncio’s default. Don't change
                           if you are unsure of what it implies.
        :param write_limit: The write_limit argument sets the high-water limit of the buffer for outgoing bytes. The
                            low-water limit is a quarter of the high-water limit. The default value is ``64 KiB``,
                            equal to asyncio’s default. Don't change if you're unsure what it implies.
        """
        self.KEY, self._market, self._re = api_key, self._change_enum(cluster, str), None

        self.WS, self._subs = None, []

        self._apis, self._handlers = self._default_handlers_and_apis()

        self._url, self._attempts = f'wss://{self._change_enum(host, str)}/{self._market}', 0

        self._ping_interval, self._ping_timeout = ping_interval, ping_timeout

        self._max_message_size, self._max_memory_queue = max_message_size, max_memory_queue

        self._read_limit, self._write_limit, self._auth = read_limit, write_limit, False

    # Context managers
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.WS.close()
        return

    async def close_stream(self):
        await self.WS.close()
        return

    async def login(self, key: str = None):
        """
        Creates Websocket Socket client using the configuration and Logs to the stream with credentials. Primarily
        meant for internal uses. You shouldn't need to call this method manually as the streamer does it
        automatically behind the scenes

        :return: None
        """

        if key is None:
            key = self.KEY

        self.WS = await wss.connect(self._url, ping_interval=self._ping_interval, ping_timeout=self._ping_timeout,
                                    max_size=self._max_message_size, max_queue=self._max_memory_queue,
                                    read_limit=self._read_limit, write_limit=self._write_limit)

        _payload = '{"action":"auth","params":"%s"}' % key  # f-strings were trippin' here.

        await self.WS.send(_payload)

        self._auth = True

    async def _send(self, data: str):
        """
        Internal function to send data to websocket server endpoint

        :param data: The formatted data string to be sent.
        :return: None
        """

        if self.WS is None:
            raise ValueError('Looks like the socket is not open. Login Failed')

        get_logger().debug(f'Sending Data: {str(data)}')

        await self.WS.send(str(data))

    async def _recv(self):
        """
        Internal function to receive messages from websocket server endpoint.

        :return: The JSON decoded message data dictionary.
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

    async def handle_messages(self, reconnect: bool = False, max_reconnection_attempts=5, reconnection_delay=5):
        """
        The primary method to start the stream. Connects & Logs in by itself. Allows Reconnecting by simply
        altering a parameter (subscriptions are persisted across reconnected streams)

        :param reconnect: If this is ``False`` (default), it simply awaits the next message and calls the
                          appropriate handler. Uses the :meth:`_default_process_message` if no handler was specified.
                          You should use the statement inside a while loop in that case. Setting it to True creates an
                          inner loop which traps disconnection errors except login failed due to invalid Key,
                          and reconnects to the stream with the same subscriptions it had earlier before getting
                          disconnected.
        :param max_reconnection_attempts: Determines how many times should the program attempt to reconnect in
                                          case of failed attempts. The Counter is reset as soon as a successful
                                          connection is re-established. Setting it to False disables the limit which is
                                          NOT recommended unless you know you got a situation. This value is ignored
                                          if ``reconnect`` is False (The default). Defaults to 5.
        :param reconnection_delay: Number of seconds to wait before attempting to reconnect after a failed
                                   reconnection attempt or a disconnection. This value is ignored if ``reconnect``
                                   is False (the default). Defaults to 5.
        :return: None
        """
        if not self._auth:
            await self.login()

        if not reconnect:
            _msg = await self._recv()

            for msg in _msg:
                handler = self._handlers[msg['ev']](msg)

                if inspect.isawaitable(handler):
                    asyncio.create_task(handler)

            return

        if not (isinstance(max_reconnection_attempts, int) or max_reconnection_attempts is False):
            raise ValueError('max_reconnection_attempts must be a positive whole number or False (False NOT '
                             'recommended as it disables the limit)')

        if not max_reconnection_attempts:
            get_logger().warning('It is never recommended to allow Infinite reconnection attempts as this does not '
                                 'account for when  Server has an outage\nor when the client loses access to '
                                 'internet. It is suggested to Re-start the stream with a finite limit for attempts')
            max_reconnection_attempts = float('inf')

        elif max_reconnection_attempts < 1:
            raise ValueError('max_reconnection_attempts must be a positive whole number')

        while 1:
            try:
                if self._re:
                    _re = await self.reconnect()

                    if _re[0]:
                        await asyncio.sleep(2)

                        try:
                            # Re-Connective Flow of receiving message
                            _msg = await self._recv()

                            for msg in _msg:
                                handler = self._handlers[msg['ev']](msg)

                                if inspect.isawaitable(handler):
                                    asyncio.create_task(handler)

                            self._re = False

                        # Right After reconnection to ensure we can actually communicate with the stream
                        except wss.ConnectionClosedOK as exc:  # PROD: ensure login errors are turned on
                            print(f'Exception: {str(exc)} || Not attempting reconnection as login/access failed. '
                                  f'Terminating...')
                            return

                        except (wss.ConnectionClosedError, Exception) as exc:
                            # Verify there are more reconnection attempts remaining
                            if self._attempts < max_reconnection_attempts:
                                print(
                                    f'Exception Encountered: {str(exc)}. Waiting for {reconnection_delay} seconds '
                                    f'and Attempting #{self._attempts + 1} '
                                    f'Reconnection...')
                                self._re = True
                                self._attempts += 1
                                self._auth = False
                                await asyncio.sleep(reconnection_delay)
                                continue

                            print('Maximum Reconnection Attempts Reached. Aborting Reconnection & Terminating...')
                            return

                    else:
                        raise RuntimeError(_re[1])

                # Usual Flow of receiving message
                _msg = await self._recv()

                for msg in _msg:  # Processing messages. Using a dict to manage handlers to avoid using if-else :D
                    handler = self._handlers[msg['ev']](msg)

                    if inspect.isawaitable(handler):
                        asyncio.create_task(handler)

            except wss.ConnectionClosedOK as exc:  # PROD: ensure login errors are turned on
                print(f'Exception: {str(exc)} || Not attempting reconnection as login/access failed. Terminating...')
                return

            except (wss.ConnectionClosedError, Exception) as exc:
                # Verify there are more reconnection attempts remaining
                if self._attempts < max_reconnection_attempts:
                    print(f'Exception Encountered: {str(exc)}. Waiting for {reconnection_delay} seconds and '
                          f'Attempting #{self._attempts + 1} '
                          f'Reconnection...')
                    self._re = True
                    self._attempts += 1
                    self._auth = False
                    await asyncio.sleep(reconnection_delay)
                    continue

                print('Maximum Reconnection Attempts Reached. Aborting Reconnection & Terminating...')
                sys.exit(0)

    async def reconnect(self) -> tuple:
        """
        Reconnects the stream. Existing subscriptions (ones before disconnections) are persisted and automatically
        re-subscribed when reconnection succeeds. All the handlers are also automatically restored. Returns a tuple
        based on success status. While this instance method is supposed to be used internally, it is possible to
        utilize this in your your custom attempts of reconnection implementation. Feel free to
        `share your implementations with the community <https://github.com/pssolanki111/polygon/wiki>`__ if you find
        success :)

        :return: ``(True, message)`` if reconnection succeeds else ``(False, message)``
        """
        get_logger().error('Attempting reconnection')

        try:
            await self.login()

            for sub in self._subs:
                await self._modify_sub(sub[0], sub[1])

            return True, 'Reconnect Successful'

        except Exception as exc:
            return False, f'Reconnect Failed. Exception: {str(exc)}'

    async def _default_process_message(self, update):
        """
        The default Handler for Message Streams which were NOT initialized with a handler function

        :param update: The update message as received after decoding the message.
        :return: None
        """

        if update['ev'] == 'status':
            print(update)

            if update['status'] in ['auth_success', 'connected']:
                if update['status'] == 'auth_success':
                    self._attempts = 0
                # get_logger().info(update['message'])
                return

            # get_logger().error(update['message'])
            return

        print(update)
        self._attempts = 0

    def _default_handlers_and_apis(self):
        """Assign default handler value to all stream setups. ONLY meant for internal use"""
        _handlers = {}

        _apis = {'T': 'trades', 'Q': 'quotes', 'AM': 'agg_min', 'A': 'agg_sec',
                 'LULD': 'stock_luld', 'NOI': 'stock_imbalances', 'C': 'forex_quotes', 'CA': 'forex_agg_min',
                 'XT': 'crypto_trades', 'XQ': 'crypto_quotes', 'XL2': 'crypto_l2', 'XA': 'crypto_agg_min',
                 'status': 'status'}

        for name in _apis.keys():
            _handlers[name] = self._default_process_message

        return _apis, _handlers

    async def _modify_sub(self, symbols: Union[str, list, None], action: str = 'subscribe', _prefix: str = 'T.'):
        """
        Internal Function to send subscribe or unsubscribe requests to websocket. You should prefer using the
        corresponding methods to subscribe or unsubscribe to streams.

        :param symbols: The list of symbols to apply the actions to.
        :param action: Defaults to subscribe which subscribes to requested stream. Change to unsubscribe to remove an
                       existing subscription.
        :param _prefix: prefix of the stream service. See :class:`polygon.enums.StreamServicePrefix` for choices.
        :return: None
        """

        if not self._auth:
            await self.login()

        if isinstance(symbols, str):
            pass

        if self._market in ['options']:
            if symbols in [None, [], 'all']:
                symbols = _prefix + '*'

            elif isinstance(symbols, list):
                symbols = ','.join([f'{_prefix}{ensure_prefix(symbol)}' for symbol in symbols])

        elif symbols in [None, [], 'all']:
            symbols = _prefix + '*'

        elif isinstance(symbols, list):
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])

        self._subs.append((symbols, action))
        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        await self.WS.send(str(_payload))

    # STOCK Streams
    async def subscribe_stock_trades(self, symbols: list = None, handler_function=None):
        """
        Get Real time trades for provided symbol(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL tickers.
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'T'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_trades(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied ticker symbols.

        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'T'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_stock_quotes(self, symbols: list = None, handler_function=None):
        """
        Get Real time quotes for provided symbol(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL tickers.
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'Q'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_quotes(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied ticker symbols.

        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'Q'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_stock_minute_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time Minute Aggregates for provided symbol(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'AM'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied ticker symbols.

        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'AM'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_stock_second_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time Seconds Aggregates for provided symbol(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'A'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_second_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied ticker symbols.

        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'A'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_stock_limit_up_limit_down(self, symbols: list = None, handler_function=None):
        """
        Get Real time LULD Events for provided symbol(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'LULD'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_limit_up_limit_down(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied ticker symbols.

        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'LULD'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_stock_imbalances(self, symbols: list = None, handler_function=None):
        """
        Get Real time Imbalance Events for provided symbol(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'NOI'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_imbalances(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied ticker symbols.

        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'NOI'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    # OPTIONS Streams
    async def subscribe_option_trades(self, symbols: list = None, handler_function=None):
        """
        Get Real time options trades for provided ticker(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker. You can specify with or without
                        the prefix ``O:``
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'T'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_option_trades(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied option symbols.

        :param symbols: A list of symbols to unsubscribe from. Defaults to ALL tickers. You can specify with or
                        without the prefix ``O:``
        :return: None
        """

        _prefix = 'T'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_option_minute_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time options minute aggregates for given ticker(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker. You can specify with or without
                        the prefix ``O:``
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'AM'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_option_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied option symbols.

        :param symbols: A list of symbols to unsubscribe from. Defaults to ALL tickers. You can specify with or
                        without the prefix ``O:``
        :return: None
        """

        _prefix = 'AM'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_option_second_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time options second aggregates for given ticker(s)

        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker. You can specify with or without
                        the prefix ``O:``
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'A'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_option_second_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied option symbols.

        :param symbols: A list of symbols to unsubscribe from. Defaults to ALL tickers. You can specify with or
                        without the prefix ``O:``
        :return: None
        """

        _prefix = 'A'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    # FOREX Streams
    async def subscribe_forex_quotes(self, symbols: list = None, handler_function=None):
        """
        Get Real time Forex Quotes for provided symbol(s)

        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``.
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'C'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_forex_quotes(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied forex symbols.

        :param symbols: A list of forex tickers. Default is * which unsubscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``.
        :return: None
        """

        _prefix = 'C'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_forex_minute_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time Forex Minute Aggregates for provided symbol(s)

        :param symbols: A list of forex tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'CA'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_forex_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied forex symbols.

        :param symbols: A list of forex tickers. Default is * which unsubscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from/to``. For example: ``USD/CNH``.
        :return: None
        """

        _prefix = 'CA'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    # CRYPTO Streams
    async def subscribe_crypto_trades(self, symbols: list = None, handler_function=None):
        """
        Get Real time Crypto Trades for provided symbol(s)

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'XT'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_crypto_trades(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied crypto symbols.

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XT'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_crypto_quotes(self, symbols: list = None, handler_function=None):
        """
        Get Real time Crypto Quotes for provided symbol(s)

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'XQ'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_crypto_quotes(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied crypto symbols.

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XQ'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_crypto_minute_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time Crypto Minute Aggregates for provided symbol(s)

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'XA'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_crypto_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied crypto symbols.

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XA'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_crypto_level2_book(self, symbols: list = None, handler_function=None):
        """
        Get Real time Crypto Level 2 Book Data for provided symbol(s)

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :param handler_function: The function which you'd want to call to process messages received from this
                                 subscription. Defaults to None which uses the default process message function.
        :return: None
        """

        _prefix = 'XL2'

        self._handlers[_prefix] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_crypto_level2_book(self, symbols: list = None):
        """
        Unsubscribe from the stream for the supplied crypto symbols.

        :param symbols: A list of Crypto tickers. Default is * which subscribes to ALL tickers in the market.
                        each Ticker must be in format: ``from-to``. For example: ``BTC-USD``. you can pass symbols
                        with or without the prefix ``X:``
        :return: None
        """

        _prefix = 'XL2'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    # Convenience Functions
    async def change_handler(self, service_prefix, handler_function):
        """
        Change your handler function for a service. Can be used to update handlers dynamically while stream is running.

        :param service_prefix: The Prefix of the service you want to change handler for. see
                               :class:`polygon.enums.StreamServicePrefix` for choices.
        :param handler_function: The new handler function to assign for this service
        :return: None
        """
        if self._change_enum(service_prefix, str) == 'status':
            self._handlers[self._apis[self._change_enum(service_prefix, str)]] = handler_function
            return

        self._handlers[self._apis[self._change_enum(service_prefix, str)]] = handler_function

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
    print('Don\'t You Dare Running Lib Files Directly :/')

# ========================================================= #
