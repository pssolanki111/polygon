# ========================================================= #
from .. import base_client
from typing import Union
import datetime
from requests.models import Response
from httpx import Response as HttpxResponse

# ========================================================= #


def ForexClient(api_key: str, use_async: bool = False, connect_timeout: int = 10, read_timeout: int = 10):
    """
    Initiates a Client to be used to access all REST Forex endpoints.

    :param api_key: Your API Key. Visit your dashboard to get yours.
    :param use_async: Set it to ``True`` to get async client. Defaults to usual non-async client.
    :param connect_timeout: The connection timeout in seconds. Defaults to 10. basically the number of seconds to
                            wait for a connection to be established. Raises a ``ConnectTimeout`` if unable to
                            connect within specified time limit.
    :param read_timeout: The read timeout in seconds. Defaults to 10. basically the number of seconds to wait for
                         date to be received. Raises a ``ReadTimeout`` if unable to connect within the specified
                         time limit.
    """

    if not use_async:
        return SyncForexClient(api_key, connect_timeout, read_timeout)

    return AsyncForexClient(api_key, connect_timeout, read_timeout)


# ========================================================= #


class SyncForexClient(base_client.BaseClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Forex REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import ForexClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

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

        _path = f'/v2/aggs/ticker/{ensure_prefix(symbol).upper()}/range/{multiplier}/{timespan}/{from_date}/' \
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

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers/{ensure_prefix(symbol).upper()}'

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


# ========================================================= #


class AsyncForexClient(base_client.BaseAsyncClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Forex REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import ForexClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    # Endpoints
    async def get_historic_forex_ticks(self, from_symbol: str, to_symbol: str,
                                       date, offset: Union[str, int] = None, limit: int = 500,
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

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_last_quote(self, from_symbol: str, to_symbol: str,
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

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1,
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

        _path = f'/v2/aggs/ticker/{ensure_prefix(symbol).upper()}/range/{multiplier}/{timespan}/{from_date}/' \
                f'{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_grouped_daily_bars(self, date, adjusted: bool = True,
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

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_previous_close(self, symbol: str, adjusted: bool = True,
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

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_snapshot_all(self, symbols: list, raw_response: bool = False) -> Union[HttpxResponse, dict]:
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

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_snapshot(self, symbol: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
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

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers/{ensure_prefix(symbol).upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_gainers_and_losers(self, direction='gainers',
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

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def real_time_currency_conversion(self, from_symbol: str, to_symbol: str, amount: float,
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

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


def ensure_prefix(sym: str):
    if sym.upper().startswith('C:'):
        return sym.upper()

    return f'C:{sym.upper()}'


# ========================================================= #


if __name__ == '__main__':  # Tests
    print('Don\'t You Dare Running Lib Files Directly')

# ========================================================= #
