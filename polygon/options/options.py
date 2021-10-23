# ========================================================= #
from .. import base_client
from typing import Union
import datetime
from requests.models import Response
from httpx import Response as HttpxResponse
# ========================================================= #


# Functions for option symbol parsing and creation

def build_option_symbol(underlying_symbol: str, expiry, call_or_put, strike_price, prefix_o: bool = False):
    """
    Build the option symbol from the details provided.

    :param underlying_symbol: The underlying stock ticker symbol.
    :param expiry: The expiry date for the option. You can pass this argument as ``datetime.datetime`` or
                   ``datetime.date`` object. Or a string in format: ``YYMMDD``. Using datetime objects is recommended.
    :param call_or_put: The option type. You can specify: ``c`` or ``call`` or ``p`` or ``put``. Capital letters are
                        also supported.
    :param strike_price: The strike price for the option. ALWAYS pass this as one number. ``145``, ``240.5``,
                         ``15.003``, ``56``, ``129.02`` are all valid values. It shouldn't have more than three
                         numbers after decimal point.
    :param prefix_o: Whether or not to prefix the symbol with 'O:'. It is needed by polygon endpoints. However all the
                     library functions will automatically add this prefix if you pass in symbols without this prefix.
    :return: The option symbol in the format specified by polygon
    """

    if isinstance(expiry, datetime.datetime) or isinstance(expiry, datetime.date):
        expiry = expiry.strftime('%y%m%d')

    elif isinstance(expiry, str) and len(expiry) != 6:
        raise ValueError('Expiry string must have 6 characters. Format is: YYMMDD')

    call_or_put = 'C' if call_or_put.lower() in ['c', 'call'] else 'P'

    if '.' in str(strike_price):
        strike, strike_dec = str(strike_price).split('.')[0].rjust(5, '0'), str(
            strike_price).split('.')[1].ljust(3, '0')[:3]
    else:
        strike, strike_dec = str(int(strike_price)).rjust(5, '0'), '000'

    if prefix_o:
        return f'O:{underlying_symbol.upper()}{expiry}{call_or_put}{strike}{strike_dec}'

    return f'{underlying_symbol.upper()}{expiry}{call_or_put}{strike}{strike_dec}'


def parse_option_symbol(option_symbol: str, output_format='object', expiry_format='date'):
    """
    Function to parse an option symbol.

    :param option_symbol: the symbol you want to parse. Both ``TSLA211015P125000`` and ``O:TSLA211015P125000`` are valid
    :param output_format: Output format of the result. defaults to object. Set it to ``dict`` or ``list`` as needed.
    :param expiry_format: The format for the expiry date in the results. Defaults to ``date`` object. change this
                          param to ``string`` to get the value as a string: ``YYYY-MM-DD``
    :return: The parsed values either as an object, list or a dict as indicated by ``output_format``.
    """

    _obj = OptionSymbol(option_symbol, output_format, expiry_format)

    if output_format in ['list', list]:
        _obj = [_obj.underlying_symbol, _obj.expiry, _obj.call_or_put, _obj.strike_price, _obj.option_symbol]

    elif output_format in ['dict', dict]:
        _obj = {'underlying_symbol': _obj.underlying_symbol,
                'strike_price': _obj.strike_price,
                'expiry': _obj.expiry,
                'call_or_put': _obj.call_or_put,
                'option_symbol': _obj.option_symbol}

    return _obj


def build_option_symbol_for_tda(underlying_symbol: str, expiry, call_or_put, strike_price):
    """
    Only use this function if you need to create option symbol for TD ameritrade API. This function is just a bonus.

    :param underlying_symbol: The underlying stock ticker symbol.
    :param expiry: The expiry date for the option. You can pass this argument as ``datetime.datetime`` or
                   ``datetime.date`` object. Or a string in format: ``MMDDYY``. Using datetime objects is recommended.
    :param call_or_put: The option type. You can specify: ``c`` or ``call`` or ``p`` or ``put``. Capital letters are
                        also supported.
    :param strike_price: The strike price for the option. ALWAYS pass this as one number. ``145``, ``240.5``,
                         ``15.003``, ``56``, ``129.02`` are all valid values. It shouldn't have more than three
                         numbers after decimal point.
    :return: The option symbol built in the format supported by TD Ameritrade.
    """

    if isinstance(expiry, datetime.date) or isinstance(expiry, datetime.datetime):
        expiry = expiry.strftime('%m%d%y')

    call_or_put = 'C' if call_or_put.lower() in ['c', 'call'] else 'P'

    return f'{underlying_symbol}_{expiry}{call_or_put}{strike_price}'


def parse_option_symbol_from_tda(option_symbol: str, output_format='object', expiry_format='date'):
    """
    Function to parse an option symbol in format supported by TD Ameritrade.

    :param option_symbol: the symbol you want to parse. Both ``TSLA211015P125000`` and ``O:TSLA211015P125000`` are valid
    :param output_format: Output format of the result. defaults to object. Set it to ``dict`` or ``list`` as needed.
    :param expiry_format: The format for the expiry date in the results. Defaults to ``date`` object. change this
                          param to ``string`` to get the value as a string: ``YYYY-MM-DD``
    :return: The parsed values either as an object, list or a dict as indicated by ``output_format``.
    """

    _obj = OptionSymbol(option_symbol, output_format, expiry_format, symbol_format='tda')

    if output_format in ['list', list]:
        _obj = [_obj.underlying_symbol, _obj.expiry, _obj.call_or_put, _obj.strike_price, _obj.option_symbol]

    elif output_format in ['dict', dict]:
        _obj = {'underlying_symbol': _obj.underlying_symbol,
                'strike_price': _obj.strike_price,
                'expiry': _obj.expiry,
                'call_or_put': _obj.call_or_put,
                'option_symbol': _obj.option_symbol}

    return _obj

# ========================================================= #


class OptionsClient(base_client.BaseClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Options REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import OptionsClient`` or ``import polygon`` (which allows you to access all names easily)

    Creating the client is as simple as: ``client = OptionsClient('MY_API_KEY')``
    Once you have the client, you can call its methods to get data from the APIs. All methods have sane default
    values and almost everything can be customized.

    Any method starting with ``async_`` in its name is meant to be for async programming. All methods have their
    sync
    and async counterparts. Any async method must be awaited while non-async (or sync) methods should be called
    directly.

    Type Hinting tells you what data type a parameter is supposed to be. You should always use ``enums`` for most
    parameters to avoid supplying error prone values.

    It is also a very good idea to visit the `official documentation <https://polygon.io/docs/getting-started>`__. I
    highly recommend using the UI there to play with the endpoints a bit. Observe the
    data you receive as the actual data received through python lib is exactly the same as shown on their page when
    you click ``Run Query``.
    """
    def __init__(self, api_key: str, use_async: bool = False, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, use_async, connect_timeout, read_timeout)

    # Endpoints
    def get_trades(self, option_symbol: str, timestamp=None, timestamp_lt=None, timestamp_lte=None,
                   timestamp_gt=None, timestamp_gte=None, sort='timestamp', limit: int = 100, order='asc',
                   raw_response: bool = False):
        """
        Get trades for an options ticker symbol in a given time range. Note that you need to have an option symbol in
        correct format for this endpoint. You can use
        :meth:`polygon.reference_apis.reference_api.ReferenceClient.get_option_contracts` to query option contracts
        using many filter parameters such as underlying symbol etc.
        `Official Docs <https://polygon.io/docs/get_vX_trades__optionsTicker__anchor>`__

        :param option_symbol: The options ticker symbol to get trades for. for eg ``O:TSLA210903C00700000``. you can
                              pass the symbol with or without the prefix ``O:``
        :param timestamp: Query by trade timestamp. You can supply a ``date``, ``datetime`` object or a ``nanosecond
                          UNIX timestamp`` or a string in format: ``YYYY-MM-DD``.
        :param timestamp_lt: query results where timestamp is less than the supplied value
        :param timestamp_lte: query results where timestamp is less than or equal to the supplied value
        :param timestamp_gt: query results where timestamp is greater than the supplied value
        :param timestamp_gte: query results where timestamp is greater than or equal to the supplied value
        :param sort: Sort field used for ordering. Defaults to timestamp. See :class:`polygon.enums.OptionTradesSort`
                     for available choices.
        :param limit: Limit the number of results returned. Defaults to 100. max is 50000.
        :param order: order of the results. Defaults to ``asc``. See :class:`polygon.enums.SortOrder` for info and
                      available choices.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: Either a Dictionary or a Response object depending on value of ``raw_response``. Defaults to Dict.
        """

        _path = f'/vX/trades/{ensure_prefix(option_symbol)}'

        _data = {'timestamp': timestamp, 'timestamp_lt': timestamp_lt, 'timestamp_lte': timestamp_lte,
                 'timestamp_gt': timestamp_gt, 'timestamp_gte': timestamp_gte, 'order': order, 'sort': sort,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_last_trade(self, ticker: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the most recent trade for a given options contract.
        `Official Docs <https://polygon.io/docs/get_v2_last_trade__optionsTicker__anchor>`__

        :param ticker: The ticker symbol of the options contract. Eg: ``O:TSLA210903C00700000``
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: Either a Dictionary or a Response object depending on value of ``raw_response``. Defaults to Dict.
        """

        _path = f'/v2/last/trade/{ensure_prefix(ticker)}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_previous_close(self, ticker: str, adjusted: bool = True,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified option contract.
        `Official Docs <https://polygon.io/docs/get_v2_aggs_ticker__optionsTicker__prev_anchor>`__

        :param ticker: The ticker symbol of the options contract. Eg: ``O:TSLA210903C00700000``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
                         Set this to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: Either a Dictionary or a Response object depending on value of ``raw_response``. Defaults to Dict.
        """

        _path = f'/v2/aggs/ticker/{ensure_prefix(ticker)}/prev'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    # ASYNC Methods
    async def async_get_trades(self, option_symbol: str, timestamp=None, timestamp_lt=None, timestamp_lte=None,
                               timestamp_gt=None, timestamp_gte=None, sort='timestamp', limit: int = 100, order='asc',
                               raw_response: bool = False):
        """
        Get trades for an options ticker symbol in a given time range. Note that you need to have an option symbol in
        correct format for this endpoint. You can use
        :meth:`polygon.reference_apis.reference_api.ReferenceClient.async_get_option_contracts` to query option
        contracts using many filter parameters such as underlying symbol etc.
        `Official Docs <https://polygon.io/docs/get_vX_trades__optionsTicker__anchor>`__

        :param option_symbol: The options ticker symbol to get trades for. for eg ``O:TSLA210903C00700000``. you can
                              pass the symbol with or without the prefix ``O:``
        :param timestamp: Query by trade timestamp. You can supply a ``date``, ``datetime`` object or a ``nanosecond
                          UNIX timestamp`` or a string in format: ``YYYY-MM-DD``.
        :param timestamp_lt: query results where timestamp is less than the supplied value
        :param timestamp_lte: query results where timestamp is less than or equal to the supplied value
        :param timestamp_gt: query results where timestamp is greater than the supplied value
        :param timestamp_gte: query results where timestamp is greater than or equal to the supplied value
        :param sort: Sort field used for ordering. Defaults to timestamp. See :class:`polygon.enums.OptionTradesSort`
                     for available choices.
        :param limit: Limit the number of results returned. Defaults to 100. max is 50000.
        :param order: order of the results. Defaults to ``asc``. See :class:`polygon.enums.SortOrder` for info and
                      available choices.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: Either a Dictionary or a Response object depending on value of ``raw_response``. Defaults to Dict.
        """

        _path = f'/vX/trades/{ensure_prefix(option_symbol)}'

        _data = {'timestamp': timestamp, 'timestamp_lt': timestamp_lt, 'timestamp_lte': timestamp_lte,
                 'timestamp_gt': timestamp_gt, 'timestamp_gte': timestamp_gte, 'order': order, 'sort': sort,
                 'limit': limit}

        _res = await self._get_async_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_last_trade(self, ticker: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the most recent trade for a given options contract - Async
        `Official Docs <https://polygon.io/docs/get_v2_last_trade__optionsTicker__anchor>`__

        :param ticker: The ticker symbol of the options contract. Eg: ``O:TSLA210903C00700000``
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: Either a Dictionary or a Response object depending on value of ``raw_response``. Defaults to Dict.
        """

        _path = f'/v2/last/trade/{ensure_prefix(ticker)}'

        _res = await self._get_async_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_previous_close(self, ticker: str, adjusted: bool = True,
                                       raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified option contract - Async
        `Official Docs <https://polygon.io/docs/get_v2_aggs_ticker__optionsTicker__prev_anchor>`__

        :param ticker: The ticker symbol of the options contract. Eg: ``O:TSLA210903C00700000``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
                         Set this to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: Either a Dictionary or a Response object depending on value of ``raw_response``. Defaults to Dict.
        """

        _path = f'/v2/aggs/ticker/{ensure_prefix(ticker)}/prev'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_async_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    @staticmethod
    def _change_enum(val, allowed_type=str):
        if isinstance(allowed_type, list):
            if type(val) in allowed_type:
                return val

        if isinstance(val, allowed_type) or val is None:
            return val

        return val.value


# ========================================================= #


class OptionSymbol:
    """
    The custom object for parsed details from option symbols.
    """
    def __init__(self, option_symbol: str, output_format, expiry_format, symbol_format='polygon'):
        """
        Parses the details from symbol and creates attributes for the object.

        :param option_symbol: the symbol you want to parse. Both ``TSLA211015P125000`` and ``O:TSLA211015P125000`` are
                              valid
        :param expiry_format: The format for the expiry date in the results. Defaults to ``date`` object. change this
                              param to ``string`` to get the value as a string: ``YYYY-MM-DD``
        :param symbol_format: Which formatting spec to use. Defaults to polygon. also supports ``tda`` which is the
                              format supported by TD Ameritrade
        """
        if symbol_format == 'polygon':
            if option_symbol.startswith('O:'):
                option_symbol = option_symbol[2:]

            self.underlying_symbol = option_symbol[:-15]

            _len = len(self.underlying_symbol)

            # optional filter for those Corrections Ian talked about
            self.underlying_symbol = ''.join([x for x in self.underlying_symbol if not x.isdigit()])

            self._expiry = option_symbol[_len:_len + 6]

            self.expiry = datetime.date(int(datetime.date.today().strftime('%Y')[:2] + self._expiry[:2]),
                                        int(self._expiry[2:4]), int(self._expiry[4:6]))

            self.call_or_put = option_symbol[_len + 6].upper()

            self.strike_price = int(option_symbol[_len + 7:]) / 1000

            self.option_symbol = f'{self.underlying_symbol}{option_symbol[_len:]}'

            if expiry_format in ['string', 'str', str]:
                self.expiry = self.expiry.strftime('%Y-%m-%d')

        elif symbol_format == 'tda':
            _split = option_symbol.split('_')

            self.underlying_symbol = _split[0]

            self._expiry = _split[1][:6]

            self.expiry = datetime.date(int(datetime.date.today().strftime('%Y')[:2] + self._expiry[4:6]),
                                        int(self._expiry[:2]), int(self._expiry[2:4]))

            self.call_or_put = _split[1][6]

            self.strike_price = float(_split[1][7:])

            self.option_symbol = option_symbol

            if expiry_format in ['string', 'str', str]:
                self.expiry = self.expiry.strftime('%Y-%m-%d')

    def __repr__(self):
        return f'Underlying: {self.underlying_symbol} || expiry: {self.expiry} || type: {self.call_or_put} || ' \
               f'strike_price: {self.strike_price}'


def ensure_prefix(symbol: str):
    """
    Ensure that the option symbol has the prefix ``O:`` as needed by polygon endpoints. If it does, make no changes. If
    it doesn't, add the prefix and return the new value.

    :param symbol: the option symbol to check
    """
    if symbol.upper().startswith('O:'):
        return symbol

    return f'O:{symbol}'


# ========================================================= #


if __name__ == '__main__':  # Tests
    print('Don\'t You Dare Running Lib Files Directly')


# ========================================================= #
