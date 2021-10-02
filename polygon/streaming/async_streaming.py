# ========================================================= #
import signal
import asyncio
import inspect
import websockets as wss
import logging
import json
from typing import Union
from enum import Enum
import platform
import sys
import os
# ========================================================= #


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


class AsyncStreamClient:
    def __init__(self, api_key: str, market: str, host: str = HOST, ping_interval: int = 20,
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
        self.KEY, self._market, self.WS, self._subs, self._re = api_key, market, None, [], 0

        self._apis, self._handlers = self._default_handlers_and_apis()

        self._url, self._attempts = f'wss://{host}/{self._market}', 0

        self._ping_interval, self._ping_timeout = ping_interval, ping_timeout

        self._max_message_size, self._max_memory_queue = max_message_size, max_memory_queue

        self._read_limit, self._write_limit, self._auth = read_limit, write_limit, False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('exit handler of async context manager called')
        await self.WS.close()
        return

    async def login(self, key: str = None):
        """
        Creates Websocket Socket client using the configuration and Logs to the stream with credentials.
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

    async def start_stream(self, reconnect: bool = False, max_reconnection_attempts: Union[int, bool] = 5,
                           reconnection_delay: Union[int, float] = 5):
        """
        The Main method to start the stream. Connects & Logs in.Allows Reconnecting by simply specifying a parameter.
        :param reconnect: Defaults to False. Setting True creates an inner loop which traps disconnection errors
        except login failed due to invalid Key, and reconnects to the stream with the same subscriptions it had
        earlier before getting disconnected.
        :param max_reconnection_attempts: Determines max how many times should the program attempt to reconnect in
        case of failed attempts. The Counter is reset as soon as a successful connection is re-established. Setting
        to False disables the limit which is NOT recommended unless you know you got a situation. This value is
        ignored if reconnect is False (The default)
        :param reconnection_delay: Number of seconds to sleep before attempting to reconnect after a disconnection.
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
                  'Server has an outage\nor when the client loses access to internet. It is suggested to Re-start '
                  'stream with a finite limit for attempts')
            max_reconnection_attempts = float('inf')

        elif max_reconnection_attempts < 1:
            raise ValueError('max_reconnection_attempts must be a positive whole number')

        if platform.system() in ['Linux', 'Darwin']:  # making signal handlers OS specific
            loop = asyncio.get_running_loop()

            loop.add_signal_handler(signal.SIGINT, lambda *args: _terminate(self.WS))
            loop.add_signal_handler(signal.SIGTERM, lambda *args: _terminate(self.WS))

        # TODO: Check availability of handlers on OSX

        # while not killer.kill_me:
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
                                asyncio.create_task(self._handlers[self._apis[msg['ev']]](msg))

                            self._re = False

                        # Right After reconnection to ensure we can actually communicate with the stream
                        # except wss.ConnectionClosedOK as exc:  # PROD: ensure login errors are turned on
                        #     print(f'Exception: {str(exc)} || Not attempting reconnection. Terminating...')
                        #     return

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
                    asyncio.create_task(self._handlers[self._apis[msg['ev']]](msg))

            # except wss.ConnectionClosedOK as exc:  # PROD: ensure login errors are turned on
            #     print(f'Exception: {str(exc)} || Not attempting reconnection. Terminating...')
            #     return

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
        Reconnects the stream. Existing subscriptions (ones before disconnections are persisted and automatically
        subscribed when reconnection succeeds). All the handlers are also automatically restored. Returns a tuple
        based on success status. While this instance method is supposed to be used internally, it is possible to
        utilize this function in your your custom attempts of reconnection implementation. Feel free to share your
        implementations with the community if you find success :)
        :return: (True, message) if reconnection succeeds else (False, message)
        """
        print('reconnect called')

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
            if update['status'] in ['auth_success', 'connected']:
                if update['status'] == 'auth_success':
                    self._attempts = 0
                get_logger().info(update['message'])
                return

            elif update['status'] == 'error':
                get_logger().error(f'Could Not subscribe to stream requested. Reason: {update["message"]}. This '
                                   f'usually happens when you attempt to request streams which are not in your account '
                                   f'subscriptions')
                return

            else:
                get_logger().error(update['message'])
                return

        print(update)
        self._attempts = 0

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

    async def _modify_sub(self, symbols: Union[str, list, None], action: str = 'subscribe', _prefix: str = 'T.'):
        """
        Internal Function to send subscribe or unsubscribe requests to websocket.
        :param symbols: The list of symbols to apply the actions to.
        :param action: Defaults to subscribe which subscribes to requested stream. Change to unsubscribe to remove an
        existing subscription.
        :return: None
        """

        if not self._auth:
            await self.login()

        if isinstance(symbols, str):
            pass

        elif symbols is None:
            symbols = _prefix + '*'
            self._subs.append((symbols, action))

        elif isinstance(symbols, list):
            symbols = ','.join([_prefix + symbol.upper() for symbol in symbols])
            self._subs.append((symbols, action))

        _payload = '{"action":"%s", "params":"%s"}' % (action.lower(), symbols)

        await self.WS.send(str(_payload))

    # STOCK Streams
    async def subscribe_stock_trades(self, symbols: list = None, handler_function=None):
        """
        Get Real time trades for provided symbol(s)
        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'T'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_trades(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'T'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_stock_quotes(self, symbols: list = None, handler_function=None):
        """
        Get Real time quotes for provided symbol(s)
        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'Q'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_quotes(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
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
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'AM'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'AM'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_stock_seconds_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time Seconds Aggregates for provided symbol(s)
        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'A'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_seconds_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
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
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'LULD'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_limit_up_limit_down(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
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
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'NOI'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_stock_imbalances(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of tickers to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'NOI'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    # OPTIONS Streams
    async def subscribe_option_trades(self, symbols: list = None, handler_function=None):
        """
        Get Real time options trades for provided ticker(s)
        :param symbols: A list of tickers to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'T'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_option_trades(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of symbols to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'T'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    # FOREX Streams
    async def subscribe_forex_quotes(self, symbols: list = None, handler_function=None):
        """
        Get Real time Forex Quotes for provided symbol(s)
        :param symbols: A list of symbol  to unsubscribe from. Defaults to ALL tickers.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'C'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_forex_quotes(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of symbol pairs to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'C'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_forex_minute_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time Forex Minute Aggregates for provided symbol(s)
        :param symbols: A list of pairs to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'CA'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_forex_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of symbol pairs to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'CA'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    # CRYPTO Streams
    async def subscribe_crypto_trades(self, symbols: list = None, handler_function=None):
        """
        Get Real time Crypto Trades for provided symbol(s)
        :param symbols: A list of pairs to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'XT'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_crypto_trades(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of symbol pairs to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'XT'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_crypto_quotes(self, symbols: list = None, handler_function=None):
        """
        Get Real time Crypto Quotes for provided symbol(s)
        :param symbols: A list of pairs to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'XQ'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_crypto_quotes(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of symbol pairs to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'XQ'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_crypto_minute_aggregates(self, symbols: list = None, handler_function=None):
        """
        Get Real time Crypto Minute Aggregates for provided symbol(s)
        :param symbols: A list of pairs to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'XA'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_crypto_minute_aggregates(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of symbol pairs to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'XA'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')

    async def subscribe_crypto_level2_book(self, symbols: list = None, handler_function=None):
        """
        Get Real time Crypto Level 2 Book Data for provided symbol(s)
        :param symbols: A list of pairs to subscribe to. Defaults to ALL ticker.
        :param handler_function: The function which you'd want to call to process messages received from this
        subscription. Defaults to None which uses the default process message function. The function supplied MUST be
        either one of a coroutine, a task, a future or an await-able.
        :return: None
        """

        _prefix = 'XL2'

        if inspect.isawaitable(handler_function) or inspect.iscoroutinefunction(handler_function) or \
                inspect.iscoroutine(handler_function):
            self._handlers[self._apis[_prefix]] = handler_function

        await self._modify_sub(symbols, _prefix=f'{_prefix}.')

    async def unsubscribe_crypto_level2_book(self, symbols: list = None):
        """
        Unsubscribe from the stream in concern.
        :param symbols: A list of symbol pairs to unsubscribe from. Defaults to ALL tickers.
        :return: None
        """

        _prefix = 'XL2'

        await self._modify_sub(symbols, action='unsubscribe', _prefix=f'{_prefix}.')


# ========================================================= #


def _terminate(_ws):
    get_logger().info('Stop Signal Received, Terminating & Exiting... This may take up to a few seconds to close all '
                      'handlers and exit safely...')
    sys.exit(0)


# ========================================================= #

if __name__ == '__main__':
    from polygon import cred

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: (%(asctime)s) : %(message)s')

    async def test():
        client = AsyncStreamClient(cred.KEY, market=STOCKS)
        # client = AsyncStreamClient(cred.KEY+'l')

        await client.subscribe_stock_trades(['AMD'])
        # await client.subscribe_stock_quotes(['AMD'])

        # await client.subscribe_option_trades(['AMD'])

        # await client.unsubscribe_stock_trades(['MSFT'])

        await client.start_stream(reconnect=True, max_reconnection_attempts=2)

        # while 1:
        #     await client.start_stream()

    asyncio.run(test())
