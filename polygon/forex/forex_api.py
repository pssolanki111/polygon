# ========================================================= #
import requests
import httpx
from typing import Union
import datetime
from requests.models import Response
from httpx import Response as HttpxResponse
# ========================================================= #


class ForexClient:
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Forex REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import ForexClient`` or ``import polygon`` (which allows you to access all names easily)

    Creating the client is as simple as: ``client = ForexClient('MY_API_KEY')``
    Once you have the client, you can call its methods to get data from the APIs. All methods have sane default
    values and almost everything can be customized.

    Any method starting with ``async_`` in its name is meant to be for async programming. All methods have their sync
    and async counterparts. Any async method must be awaited while non-async (or sync) methods should be called
    directly.

    Type Hinting tells you what data type a parameter is supposed to be. You should always use ``enums`` for most
    parameters to avoid supplying error prone values.

    It is also a very good idea to visit the `official documentation <https://polygon.io/docs/getting-started>`__. I
    highly recommend using the UI there to play with the endpoints a bit. Observe the
    data you receive as the actual data received through python lib is exactly the same as shown on their page when
    you click ``Run Query``.
    """
    def __init__(self, api_key: str, use_async: bool = False):
        """
        Initiates a Client to be used to access all the endpoints.

        :param api_key: Your API Key. Visit your dashboard to get yours.
        :param use_async: Set to True to get an async client. Defaults to False which returns a non-async client.
        """
        self.KEY, self._async = api_key, use_async
        self.BASE = 'https://api.polygon.io'

        if self._async:
            self.session = httpx.AsyncClient()
        else:
            self.session = requests.session()

        self.session.headers.update({'Authorization': f'Bearer {self.KEY}'})

    # Context Managers
    def __enter__(self):
        if not self._async:
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._async:
            self.session.close()

    # Context Managers - Asyncio
    async def __aenter__(self):
        if self._async:
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._async:
            self.session: httpx.AsyncClient
            await self.session.aclose()

    def close(self):
        if not self._async:
            self.session.close()

    async def async_close(self):
        if self._async:
            self.session: httpx.AsyncClient
            await self.session.aclose()

    # Internal Functions
    def _get_response(self, path: str, params: dict = None,
                      raw_response: bool = True) -> Union[Response, dict]:
        """
        Get response on a path. Meant to be used internally but can be used if you know what you're doing. To be
        used by sync client only. For async access, see :meth:`_get_async_response`

        :param path: RESTful path for the endpoint. Available on the docs for the endpoint right above its name.
        :param params: Query Parameters to be supplied with the request. These are mapped 1:1 with the endpoint.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to check the
                             status code or inspect the headers. Defaults to True which returns the ``Response`` object.
        :return: A Response object by default. Make ``raw_response=False`` to get JSON decoded Dictionary
        """
        _res = self.session.request('GET', self.BASE + path, params=params)

        if raw_response:
            return _res

        return _res.json()

    async def _get_async_response(self, path: str, params: dict = None,
                                  raw_response: bool = True) -> Union[HttpxResponse, dict]:
        """
        Get response on a path - meant to be used internally but can be used if you know what you're doing - to be
        used by async client only. For sync access, see :meth:`_get_response`

        :param path: RESTful path for the endpoint. Available on the docs for the endpoint right above its name.
        :param params: Query Parameters to be supplied with the request. These are mapped 1:1 with the endpoint.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to check the
                             status code or inspect the headers. Defaults to True which returns the ``Response`` object.
        :return: A Response object by default. Make ``raw_response=False`` to get JSON decoded Dictionary
        """
        _res = await self.session.request('GET', self.BASE + path, params=params)

        if raw_response:
            return _res

        return _res.json()

    def get_next_page_by_url(self, url: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the next page of a response. The URl is returned within ``next_url`` attribute on endpoints which support
        pagination (eg the tickers endpoint). If the response doesn't contain this attribute, either all pages were
        received or the endpoint doesn't have pagination. Meant for internal use primarily.

        Note that this method is meant for sync programming. See :meth:`async_get_next_page_by_url` for async.

        :param url: The next URL. As contained in ``next_url`` of the response.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: Either a Dictionary or a Response object depending on value of raw_response. Defaults to Dict.
        """
        _res = self.session.request('GET', url)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_next_page_by_url(self, url: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the next page of a response. The URl is returned within ``next_url`` attribute on endpoints which support
        pagination (eg the tickers endpoint). If the response doesn't contain this attribute, either all pages were
        received or the endpoint doesn't have pagination. Meant for internal use primarily.

        Note that this method is meant for async programming. See :meth:`get_next_page_by_url` for sync.

        :param url: The next URL. As contained in ``next_url`` of the response.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: Either a Dictionary or a Response object depending on value of raw_response. Defaults to Dict.
        """
        _res = await self.session.request('GET', url)

        if raw_response:
            return _res

        return _res.json()

    # Endpoints
    def get_historic_forex_ticks(self, from_symbol: str, to_symbol: str, date, offset: Union[str, int] = None,
                                 limit: int = 500, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get historic trade ticks for a forex currency pair.
        `Official Docs <https://polygon.io/docs/get_v1_historic_forex__from___to___date__anchor>`__

        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param date: The date/day of the historic ticks to retrieve. Could be ``datetime``, ``date`` or string 
                     ``YYYY-MM-DD``
        :param offset: The timestamp offset, used for pagination. This is the offset at which to start the results.
                       Using the timestamp of the last result as the offset will give you the next page of results.
                       I'm thinking about a good way to implement this type of pagination in the lib which doesn't 
                       have a ``next_url`` in the response attributes.
        :param limit: Limit the size of the response, max 10000. Default 500
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, datetime.datetime) or isinstance(date, datetime.date):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v1/historic/forex/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'offset': offset,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_last_quote(self, from_symbol: str, to_symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the last trade tick for a forex currency pair.
        `Official Docs <https://polygon.io/docs/get_v1_last_quote_currencies__from___to__anchor>`__

        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/last_quote/currencies/{from_symbol.upper()}/{to_symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1, timespan='day',
                           adjusted: bool = True, sort='asc', limit: int = 5000,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get aggregate bars for a forex pair over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then ``5-minute`` bars will be returned.
        `Official Docs
        <https://polygon.io/docs/get_v2_aggs_ticker__forexTicker__range__multiplier___timespan___from___to__anchor>`__

        :param symbol: The ticker symbol of the forex pair. eg: ``C:EURUSD``. You can supply with or without prefix 
                       ``C:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string 
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to day candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
                         Set this to False to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. see :class:`polygon.enums.SortOrder` for available choices. 
                     Defaults to ``asc`` which is oldest at the top.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(from_date, datetime.datetime) or isinstance(from_date, datetime.date):
            from_date = from_date.strftime('%Y-%m-%d')

        if isinstance(to_date, datetime.datetime) or isinstance(to_date, datetime.date):
            to_date = to_date.strftime('%Y-%m-%d')

        timespan, sort = self._change_enum(timespan, str), self._change_enum(sort, str)

        _path = f'/v2/aggs/ticker/{self.ensure_prefix(symbol).upper()}/range/{multiplier}/{timespan}/{from_date}/' \
                f'{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_grouped_daily_bars(self, date, adjusted: bool = True, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the daily open, high, low, and close (OHLC) for the entire forex markets.
        `Official Docs <https://polygon.io/docs/get_v2_aggs_grouped_locale_global_market_fx__date__anchor>`__

        :param date: The date for the aggregate window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param adjusted:  Whether or not the results are adjusted for splits. By default, results are adjusted. Set
                          this to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, datetime.datetime) or isinstance(date, datetime.date):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/grouped/locale/global/market/fx/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_previous_close(self, symbol: str, adjusted: bool = True,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified forex pair.
        `Official Docs <https://polygon.io/docs/get_v2_aggs_ticker__forexTicker__prev_anchor>`__

        :param symbol: The ticker symbol of the forex pair.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/aggs/ticker/{symbol.upper()}/prev'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_snapshot_all(self, symbols: list, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        forex symbols
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex_tickers_anchor>`__

        :param symbols: A list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if not isinstance(symbols, list):
            raise ValueError('symbols must be supplied as a list of tickers')

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers'

        _data = {'tickers': ','.join([x.upper() for x in symbols])}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_snapshot(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded forex symbol.
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex_tickers__ticker__anchor>`__

        :param symbol: Symbol of the forex pair. eg: ``C:EURUSD``. You can supply with or without prefix ``C:``.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers/{self.ensure_prefix(symbol).upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_gainers_and_losers(self, direction='gainers', raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current top 20 gainers or losers of the day in forex markets.
        `Official docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex__direction__anchor>`__

        :param direction: The direction of the snapshot results to return. See :class:`polygon.enums.SnapshotDirection`
                          for available choices. Defaults to Gainers.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/{direction}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def real_time_currency_conversion(self, from_symbol: str, to_symbol: str, amount: float, precision: int = 2,
                                      raw_response: bool = False) -> Union[Response, dict]:
        """
        Get currency conversions using the latest market conversion rates. Note than you can convert in both directions.
        For example USD to CAD or CAD to USD.
        `Official Docs <https://polygon.io/docs/get_v1_conversion__from___to__anchor>`__

        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param amount: The amount to convert,
        :param precision: The decimal precision of the conversion. Defaults to 2 which is 2 decimal places accuracy.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/conversion/{from_symbol.upper()}/{to_symbol.upper()}'

        _data = {'amount': amount,
                 'precision': precision}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    # ASYNC Operations' Methods
    async def async_get_historic_forex_ticks(self, from_symbol: str, to_symbol: str,
                                             date,
                                             offset: Union[str, int] = None, limit: int = 500,
                                             raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get historic trade ticks for a forex currency pair - Async method.
        `Official Docs <https://polygon.io/docs/get_v1_historic_forex__from___to___date__anchor>`__

        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param date: The date/day of the historic ticks to retrieve. Could be ``datetime``, ``date`` or string
                     ``YYYY-MM-DD``
        :param offset: The timestamp offset, used for pagination. This is the offset at which to start the results.
                       Using the timestamp of the last result as the offset will give you the next page of results.
                       I'm thinking about a good way to implement this type of pagination in the lib which doesn't
                       have a ``next_url`` in the response attributes.
        :param limit: Limit the size of the response, max 10000. Default 500
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, datetime.datetime) or isinstance(date, datetime.date):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v1/historic/forex/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'offset': offset,
                 'limit': limit}

        _res = await self._get_async_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_last_quote(self, from_symbol: str, to_symbol: str,
                                   raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the last trade tick for a forex currency pair - Async method
        `Official Docs <https://polygon.io/docs/get_v1_last_quote_currencies__from___to__anchor>`__

        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/last_quote/currencies/{from_symbol.upper()}/{to_symbol.upper()}'

        _res = await self._get_async_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1,
                                       timespan='day', adjusted: bool = True, sort='asc',
                                       limit: int = 5000, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get aggregate bars for a forex pair over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then ``5-minute`` bars will be returned.
        `Official Docs
        <https://polygon.io/docs/get_v2_aggs_ticker__forexTicker__range__multiplier___timespan___from___to__anchor>`__

        :param symbol: The ticker symbol of the forex pair. eg: ``C:EURUSD``. You can supply with or without prefix 
                       ``C:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to day candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
                         Set this to False to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. see :class:`polygon.enums.SortOrder` for available choices.
                     Defaults to ``asc`` which is oldest at the top.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(from_date, datetime.datetime) or isinstance(from_date, datetime.date):
            from_date = from_date.strftime('%Y-%m-%d')

        if isinstance(to_date, datetime.datetime) or isinstance(to_date, datetime.date):
            to_date = to_date.strftime('%Y-%m-%d')

        timespan, sort = self._change_enum(timespan, str), self._change_enum(sort, str)

        _path = f'/v2/aggs/ticker/{self.ensure_prefix(symbol).upper()}/range/{multiplier}/{timespan}/{from_date}/' \
                f'{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = await self._get_async_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_grouped_daily_bars(self, date,
                                           adjusted: bool = True,
                                           raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the daily open, high, low, and close (OHLC) for the entire forex markets - Async method
        `Official Docs <https://polygon.io/docs/get_v2_aggs_grouped_locale_global_market_fx__date__anchor>`__

        :param date: The date for the aggregate window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param adjusted:  Whether or not the results are adjusted for splits. By default, results are adjusted. Set
                          this to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, datetime.datetime) or isinstance(date, datetime.date):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/grouped/locale/global/market/fx/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_async_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_previous_close(self, symbol: str, adjusted: bool = True,
                                       raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified forex pair - Async method
        `Official Docs <https://polygon.io/docs/get_v2_aggs_ticker__forexTicker__prev_anchor>`__

        :param symbol: The ticker symbol of the forex pair.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/aggs/ticker/{symbol.upper()}/prev'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_async_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_snapshot_all(self, symbols: list, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        forex symbols - Async method
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex_tickers_anchor>`__

        :param symbols: A list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if not isinstance(symbols, list):
            raise ValueError('symbols must be supplied as a list of tickers')

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers'

        _data = {'tickers': ','.join([x.upper() for x in symbols])}

        _res = await self._get_async_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_snapshot(self, symbol: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded forex symbol - Async method
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex_tickers__ticker__anchor>`__

        :param symbol: Symbol of the forex pair. eg: ``C:EURUSD``. You can supply with or without prefix ``C:``.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers/{self.ensure_prefix(symbol).upper()}'

        _res = await self._get_async_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def async_get_gainers_and_losers(self, direction='gainers',
                                           raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current top 20 gainers or losers of the day in forex markets.
        `Official docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex__direction__anchor>`__

        :param direction: The direction of the snapshot results to return. See :class:`polygon.enums.SnapshotDirection`
                          for available choices. Defaults to Gainers.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/{direction}'

        _res = await self._get_async_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def async_real_time_currency_conversion(self, from_symbol: str, to_symbol: str, amount: float,
                                                  precision: int = 2,
                                                  raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get currency conversions using the latest market conversion rates. Note than you can convert in both directions.
        For example USD to CAD or CAD to USD - Async method
        `Official Docs <https://polygon.io/docs/get_v1_conversion__from___to__anchor>`__

        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param amount: The amount to convert,
        :param precision: The decimal precision of the conversion. Defaults to 2 which is 2 decimal places accuracy.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/conversion/{from_symbol.upper()}/{to_symbol.upper()}'

        _data = {'amount': amount,
                 'precision': precision}

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

    @staticmethod
    def ensure_prefix(sym: str):
        if sym.startswith('C:'):
            return sym

        return f'C:{sym}'


# ========================================================= #


if __name__ == '__main__':  # Tests
    print('Don\'t You Dare Running Lib Files Directly')


# ========================================================= #
