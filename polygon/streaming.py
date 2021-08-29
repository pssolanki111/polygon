# ========================================================= #
import websockets as wss
import websocket as ws_client
import threading
import signal
from typing import Union
# ========================================================= #

STOCKS = 'stocks'
CRYPTO = 'crypto'
FOREX = 'forex'
HOST = 'socket.polygon.io'
DELAYED_HOST = 'delayed.polygon.io'


# ========================================================= #


class StreamClient:
    def __init__(self, api_key: str, market: str = STOCKS, host: str = HOST, on_message=None, on_close=None,
                 on_error=None, ping_interval: int = 21, ping_timeout: int = 20, ping_payload: str = '',
                 skip_utf8_validation: bool = True, enable_connection_logs: bool = False):
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
        :param ping_interval: client would send a ping every specified number of seconds to server to keep connection
        alive. Set to 0 to disable pinging. Defaults to 21 seconds
        :param ping_timeout: Timeout in seconds if a pong (response to ping from server) is not received. The Stream
        is terminated as it is considered to be dead if no pong is received within the specified timeout. default: 20
        :param ping_payload: The option message to be sent with the ping. Better to leave it empty string.
        :param skip_utf8_validation: Whether to skip utf validation of messages. Defaults to False. Setting it to
        True may result in some performance downgrade.
        :param enable_connection_logs: Whether or not to print useful debug info related to the stream connection.
        Helpful for trying to debug something. Defaults to False.
        """

        if enable_connection_logs:  # enable connection logs if requested.
            ws_client.enableTrace(True)

        self._host, self._url, self.KEY = host, f'wss://{host}/{market}', api_key

        self._ping_interval, self._ping_timeout, self._ping_payload = ping_interval, ping_timeout, ping_payload

        self._skip_utf8_validation, self._enable_connection_logs = skip_utf8_validation, enable_connection_logs

        self.WS = ws_client.WebSocketApp(self._url, on_message=self._default_on_msg, on_close=self._default_on_close,
                                         on_error=self._default_on_error, on_open=self._default_on_open)

        self.WS.on_close = on_close if on_close else self._default_on_close
        self.WS.on_error = on_error if on_error else self._default_on_error
        self.WS.on_message = on_message if on_message else self._default_on_msg

        self._auth = threading.Event()  # to ensure we are logged in before sending any communication.

        self._run_in_thread: Union[threading.Thread, None] = None

        # signal Handlers
        signal.signal(signal.SIGINT, self.close_stream)
        signal.signal(signal.SIGTERM, self.close_stream)

    def start_stream(self):
        """
        Starts the Stream Event Loop. The loop is infinite and will continue to run until the stream is
        terminated, either manually or due to an exception
        """

        self.WS.run_forever(ping_interval=self._ping_interval, ping_timeout=self._ping_timeout,
                            ping_payload=self._ping_payload, skip_utf8_validation=self._skip_utf8_validation)

    def start_stream_parallel(self):
        """
        Starts the Stream event loop in a thread. This will not block the main thread. Useful for GUI applications
        and use cases where you have more than one event loop in general
        """

        self._run_in_thread = threading.Thread(target=self.start_stream)
        self._run_in_thread.start()

    def close_stream(self, *args, **kwargs):
        """
        Close the websocket connection. Wait for thread to finish if running.
        :param args: Arguments supplied by signal handlers
        :param kwargs: KWArguments supplied by signal handlers
        :return: None
        """

        print('Terminating Stream...')
        self.WS.close()
        if self._run_in_thread:
            self._run_in_thread.join()

    def _default_on_msg(self, msg, *args):
        """

        :param msg:
        :param args:
        :return: None
        """
        print('Args: ', args)

        print('message received:\n', str(msg))

    def _default_on_close(self, close_code, close_msg, *args):
        """

        :param close_code:
        :param close_msg:
        :param args:
        :return:
        """
        print('Args: ', args)

        print(f'Close code: {close_code}\nClose message:\n', str(close_msg))

    def _default_on_error(self, error, *args):
        """

        :param error:
        :return:
        """
        print('Args: ', *args)

        print('Error Encountered:\n', str(error))

    def _default_on_open(self, *args):
        """

        :param args:
        :return:
        """
        print('Args: ', args)

        print('Open called...')


# ========================================================= #


class AsyncStreamClient:
    def __init__(self, api_key: str):
        pass


# ========================================================= #


if __name__ == '__main__':
    print('Don\'t You Dare Running Lib Files Directly')
    from polygon import cred
    from pprint import pprint

    client = StreamClient(cred.KEY)
    client.start_stream()


# ========================================================= #
