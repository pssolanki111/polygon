# ========================================================= #
from .. import base_client
from typing import Union
import datetime
from requests.models import Response
from httpx import Response as HttpxResponse

# ========================================================= #


def StocksClient(api_key: str, use_async: bool = False, connect_timeout: int = 10, read_timeout: int = 10):
    """
    Initiates a Client to be used to access all REST Stocks endpoints.

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
        return SyncStocksClient(api_key, connect_timeout, read_timeout)

    return AsyncStocksClient(api_key, connect_timeout, read_timeout)


# ========================================================= #


class SyncStocksClient(base_client.BaseClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Stocks REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import StocksClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    # Endpoints
    def get_trades(self, symbol: str, date, timestamp: int = None, timestamp_limit: int = None, reverse: bool = True,
                   limit: int = 5000, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get trades for a given ticker symbol on a specified date. The response from polygon seems to have a ``map``
        attribute which gives a mapping of attribute names to readable values.
        `Official Docs <https://polygon.io/docs/get_v2_ticks_stocks_trades__ticker___date__anchor>`__

        :param symbol: The ticker symbol we want trades for.
        :param date: The date/day of the trades to retrieve. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
                          results. Using the ``timestamp`` of the last result as the offset will give you the next page
                          of results. Default: None. I'm trying to think of a good way to implement pagination
                          support for this type of pagination.
        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.date, datetime.datetime)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/ticks/stocks/trades/{symbol.upper()}/{date}'

        _data = {'timestamp': timestamp,
                 'timestampimit': timestamp_limit,
                 'reverse': 'true' if reverse else 'false',
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_trades_vx(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                      timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                      raw_response: bool = False) -> Union[Response, dict]:
        """
        Get trades for a ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/get_vX_trades__stockTicker__anchor>`__

        :param symbol: The ticker symbol you want trades for.
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.StocksTradesSort` for
                     choices
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param timestamp_lt: return results where timestamp is less than the given value. Can be date or date string.
        :param timestamp_lte: return results where timestamp is less than/equal to the given value. Can be date or date
                              string.
        :param timestamp_gt: return results where timestamp is greater than the given value. Can be date or date
                             string.
        :param timestamp_gte: return results where timestamp is greater than/equal to the given value. Can be date or
                              date string.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(timestamp, (datetime.date, datetime.datetime)):
            timestamp = timestamp.strftime('%Y-%m-%d')

        if isinstance(timestamp_lt, (datetime.date, datetime.datetime)):
            timestamp_lt = timestamp_lt.strftime('%Y-%m-%d')

        if isinstance(timestamp_lte, (datetime.date, datetime.datetime)):
            timestamp_lte = timestamp_lte.strftime('%Y-%m-%d')

        if isinstance(timestamp_gt, (datetime.date, datetime.datetime)):
            timestamp_gt = timestamp_gt.strftime('%Y-%m-%d')

        if isinstance(timestamp_gte, (datetime.date, datetime.datetime)):
            timestamp_gte = timestamp_gte.strftime('%Y-%m-%d')

        _path = f'/vX/trades/{symbol}'

        _data = {'timestamp': timestamp, 'timestamp_lt': timestamp_lt, 'timestamp_lte': timestamp_lte,
                 'timestamp_gt': timestamp_gt, 'timestamp_gte': timestamp_gte, 'limit': limit,
                 'sort': self._change_enum(sort, str), 'order': self._change_enum(order, str)}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_quotes(self, symbol: str, date, timestamp: int = None, timestamp_limit: int = None, reverse: bool = True,
                   limit: int = 5000, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get Quotes for a given ticker symbol on a specified date. The response from polygon seems to have a ``map``
        attribute which gives a mapping of attribute names to readable values.
        `Official Docs <https://polygon.io/docs/get_v2_ticks_stocks_nbbo__ticker___date__anchor>`__

        :param symbol: The ticker symbol we want quotes for.
        :param date: The date/day of the quotes to retrieve. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
                         results. Using the ``timestamp`` of the last result as the offset will give you the next
                         page of results. Default: None. Thinking of a good way to implement this pagination here.
        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.date, datetime.datetime)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/ticks/stocks/nbbo/{symbol.upper()}/{date}'

        _data = {'timestamp': timestamp,
                 'timestampimit': timestamp_limit,
                 'reverse': 'true' if reverse else 'false',
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_quotes_vx(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                      timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                      raw_response: bool = False) -> Union[Response, dict]:
        """
        Get NBBO Quotes for a ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/get_vX_quotes__stockTicker__anchor>`__

        :param symbol: The ticker symbol you want quotes for.
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.StocksQuotesSort` for
                     choices
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param timestamp_lt: return results where timestamp is less than the given value. Can be date or date string.
        :param timestamp_lte: return results where timestamp is less than/equal to the given value. Can be date or date
                              string.
        :param timestamp_gt: return results where timestamp is greater than the given value. Can be date or date
                             string.
        :param timestamp_gte: return results where timestamp is greater than/equal to the given value. Can be date or
                              date string.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(timestamp, (datetime.date, datetime.datetime)):
            timestamp = timestamp.strftime('%Y-%m-%d')

        if isinstance(timestamp_lt, (datetime.date, datetime.datetime)):
            timestamp_lt = timestamp_lt.strftime('%Y-%m-%d')

        if isinstance(timestamp_lte, (datetime.date, datetime.datetime)):
            timestamp_lte = timestamp_lte.strftime('%Y-%m-%d')

        if isinstance(timestamp_gt, (datetime.date, datetime.datetime)):
            timestamp_gt = timestamp_gt.strftime('%Y-%m-%d')

        if isinstance(timestamp_gte, (datetime.date, datetime.datetime)):
            timestamp_gte = timestamp_gte.strftime('%Y-%m-%d')

        _path = f'/vX/quotes/{symbol}'

        _data = {'timestamp': timestamp, 'timestamp_lt': timestamp_lt, 'timestamp_lte': timestamp_lte,
                 'timestamp_gt': timestamp_gt, 'timestamp_gte': timestamp_gte, 'limit': limit,
                 'sort': self._change_enum(sort, str), 'order': self._change_enum(order, str)}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_last_trade(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the most recent trade for a given stock.
        `Official Docs <https://polygon.io/docs/get_v2_last_trade__stocksTicker__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/last/trade/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_last_quote(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the most recent NBBO (Quote) tick for a given stock.
        `Official Docs <https://polygon.io/docs/get_v2_last_nbbo__stocksTicker__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/last/nbbo/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_daily_open_close(self, symbol: str, date, adjusted: bool = True,
                             raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the OCHLV and after-hours prices of a stock symbol on a certain date.
        `Official Docs <https://polygon.io/docs/get_v1_open-close__stocksTicker___date__anchor>`__

        :param symbol: The ticker symbol we want daily-OCHLV for.
        :param date: The date/day of the daily-OCHLV to retrieve. Could be ``datetime`` or ``date`` or string
                     ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.date, datetime.datetime)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v1/open-close/{symbol.upper()}/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_aggregate_bars(self, symbol: str, from_date, to_date, adjusted: bool = True,
                           sort='asc', limit: int = 5000, multiplier: int = 1, timespan='day',
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get aggregate bars for a stock over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/get_v2_aggs_ticker__stocksTicker__range__multiplier___timespan___from___to__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param from_date: The start of the aggregate time window. Could be ``datetime`` or ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. See :class:`polygon.enums.SortOrder` for choices. ``asc`` default.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param multiplier: The size of the timespan multiplier. Must be a positive whole number.
        :param timespan: The size of the time window. See :class:`polygon.enums.Timespan` for choices. defaults to
                         ``day``
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(from_date, (datetime.date, datetime.datetime)):
            from_date = from_date.strftime('%Y-%m-%d')

        if isinstance(to_date, (datetime.date, datetime.datetime)):
            to_date = to_date.strftime('%Y-%m-%d')

        timespan, sort = self._change_enum(timespan, str), self._change_enum(sort, str)

        _path = f'/v2/aggs/ticker/{symbol.upper()}/range/{multiplier}/{timespan}/{from_date}/{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_grouped_daily_bars(self, date, adjusted: bool = True, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the daily OCHLV for the entire stocks/equities markets.
        `Official docs <https://polygon.io/docs/get_v2_aggs_grouped_locale_us_market_stocks__date__anchor>`__

        :param date: The date to get the data for. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """
        if isinstance(date, (datetime.date, datetime.datetime)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/grouped/locale/us/market/stocks/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_previous_close(self, symbol: str, adjusted: bool = True,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the previous day's OCHLV for the specified stock ticker.
        `Official Docs <https://polygon.io/docs/get_v2_aggs_ticker__stocksTicker__prev_anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
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

    def get_snapshot(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded stock ticker.
        `Official Docs
        <https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks_tickers__stocksTicker__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_current_price(self, symbol: str) -> float:
        """
        get current market price for the ticker symbol specified.

        Uses :meth:`get_last_trade` under the hood
        `Official Docs <https://polygon.io/docs/get_v2_last_trade__stocksTicker__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :return: The current price. A ``KeyError`` indicates the request wasn't successful.
        """

        _res = self.get_last_trade(symbol)

        try:
            return _res['results']['p']
        except KeyError:
            raise ValueError('Request failed. Make sure your API key is correct and your subscription has access to '
                             f'the data you requested. Response from the API: {_res}')

    def get_snapshot_all(self, symbols: list = None, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        stock symbols.
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks_tickers_anchor>`__

        :param symbols: A comma separated list of tickers to get snapshots for. Defaults to ALL tickers
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers'

        if symbols is not None:
            _data = {'tickers': ','.join([x.upper() for x in symbols])}
        else:
            _data = {'tickers': None}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_gainers_and_losers(self, direction='gainers', raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current top 20 gainers or losers of the day in stocks/equities markets.
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks__direction__anchor>`__

        :param direction: The direction of results. Defaults to gainers. See :class:`polygon.enums.SnapshotDirection`
                          for choices
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/{self._change_enum(direction, str)}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


class AsyncStocksClient(base_client.BaseAsyncClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Stocks REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import StocksClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    # Endpoints
    async def get_trades(self, symbol: str, date,
                         timestamp: int = None, timestamp_limit: int = None, reverse: bool = True,
                         limit: int = 5000, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get trades for a given ticker symbol on a specified date. The response from polygon seems to have a ``map``
        attribute which gives a mapping of attribute names to readable values - Async method
        `Official Docs <https://polygon.io/docs/get_v2_ticks_stocks_trades__ticker___date__anchor>`__

        :param symbol: The ticker symbol we want trades for.
        :param date: The date/day of the trades to retrieve. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
                          results. Using the ``timestamp`` of the last result as the offset will give you the next page
                          of results. Default: None. I'm trying to think of a good way to implement pagination
                          support for this type of pagination.
        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.date, datetime.datetime)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/ticks/stocks/trades/{symbol.upper()}/{date}'

        _data = {'timestamp': timestamp,
                 'timestampimit': timestamp_limit,
                 'reverse': 'true' if reverse else 'false',
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_trades_vx(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                            timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                            raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get trades for a ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/get_vX_trades__stockTicker__anchor>`__

        :param symbol: The ticker symbol you want trades for.
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.StocksTradesSort` for
                     choices
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param timestamp_lt: return results where timestamp is less than the given value. Can be date or date string.
        :param timestamp_lte: return results where timestamp is less than/equal to the given value. Can be date or date
                              string.
        :param timestamp_gt: return results where timestamp is greater than the given value. Can be date or date
                             string.
        :param timestamp_gte: return results where timestamp is greater than/equal to the given value. Can be date or
                              date string.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(timestamp, (datetime.date, datetime.datetime)):
            timestamp = timestamp.strftime('%Y-%m-%d')

        if isinstance(timestamp_lt, (datetime.date, datetime.datetime)):
            timestamp_lt = timestamp_lt.strftime('%Y-%m-%d')

        if isinstance(timestamp_lte, (datetime.date, datetime.datetime)):
            timestamp_lte = timestamp_lte.strftime('%Y-%m-%d')

        if isinstance(timestamp_gt, (datetime.date, datetime.datetime)):
            timestamp_gt = timestamp_gt.strftime('%Y-%m-%d')

        if isinstance(timestamp_gte, (datetime.date, datetime.datetime)):
            timestamp_gte = timestamp_gte.strftime('%Y-%m-%d')

        _path = f'/vX/trades/{symbol}'

        _data = {'timestamp': timestamp, 'timestamp_lt': timestamp_lt, 'timestamp_lte': timestamp_lte,
                 'timestamp_gt': timestamp_gt, 'timestamp_gte': timestamp_gte, 'limit': limit,
                 'sort': self._change_enum(sort, str), 'order': self._change_enum(order, str)}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_quotes(self, symbol: str, date, timestamp: int = None, timestamp_limit: int = None,
                         reverse: bool = True, limit: int = 5000,
                         raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get Quotes for a given ticker symbol on a specified date. The response from polygon seems to have a ``map``
        attribute which gives a mapping of attribute names to readable values - Async method
        `Official Docs <https://polygon.io/docs/get_v2_ticks_stocks_nbbo__ticker___date__anchor>`__

        :param symbol: The ticker symbol we want quotes for.
        :param date: The date/day of the quotes to retrieve. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
                         results. Using the ``timestamp`` of the last result as the offset will give you the next
                         page of results. Default: None. Thinking of a good way to implement this pagination here.
        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.date, datetime.datetime)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/ticks/stocks/nbbo/{symbol.upper()}/{date}'

        _data = {'timestamp': timestamp,
                 'timestampimit': timestamp_limit,
                 'reverse': 'true' if reverse else 'false',
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_quotes_vx(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                            timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                            raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get NBBO Quotes for a ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/get_vX_quotes__stockTicker__anchor>`__

        :param symbol: The ticker symbol you want quotes for.
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.StocksQuotesSort` for
                     choices
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param timestamp_lt: return results where timestamp is less than the given value. Can be date or date string.
        :param timestamp_lte: return results where timestamp is less than/equal to the given value. Can be date or date
                              string.
        :param timestamp_gt: return results where timestamp is greater than the given value. Can be date or date
                             string.
        :param timestamp_gte: return results where timestamp is greater than/equal to the given value. Can be date or
                              date string.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(timestamp, (datetime.date, datetime.datetime)):
            timestamp = timestamp.strftime('%Y-%m-%d')

        if isinstance(timestamp_lt, (datetime.date, datetime.datetime)):
            timestamp_lt = timestamp_lt.strftime('%Y-%m-%d')

        if isinstance(timestamp_lte, (datetime.date, datetime.datetime)):
            timestamp_lte = timestamp_lte.strftime('%Y-%m-%d')

        if isinstance(timestamp_gt, (datetime.date, datetime.datetime)):
            timestamp_gt = timestamp_gt.strftime('%Y-%m-%d')

        if isinstance(timestamp_gte, (datetime.date, datetime.datetime)):
            timestamp_gte = timestamp_gte.strftime('%Y-%m-%d')

        _path = f'/vX/quotes/{symbol}'

        _data = {'timestamp': timestamp, 'timestamp_lt': timestamp_lt, 'timestamp_lte': timestamp_lte,
                 'timestamp_gt': timestamp_gt, 'timestamp_gte': timestamp_gte, 'limit': limit,
                 'sort': self._change_enum(sort, str), 'order': self._change_enum(order, str)}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_last_trade(self, symbol: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the most recent trade for a given stock - Async method
        `Official Docs <https://polygon.io/docs/get_v2_last_trade__stocksTicker__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/last/trade/{symbol.upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_last_quote(self, symbol: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the most recent NBBO (Quote) tick for a given stock - Async method
        `Official Docs <https://polygon.io/docs/get_v2_last_nbbo__stocksTicker__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/last/nbbo/{symbol.upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_daily_open_close(self, symbol: str, date, adjusted: bool = True,
                                   raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the OCHLV and after-hours prices of a stock symbol on a certain date - Async method
        `Official Docs <https://polygon.io/docs/get_v1_open-close__stocksTicker___date__anchor>`__

        :param symbol: The ticker symbol we want daily-OCHLV for.
        :param date: The date/day of the daily-OCHLV to retrieve. Could be ``datetime`` or ``date`` or string
                     ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.date, datetime.datetime)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v1/open-close/{symbol.upper()}/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_aggregate_bars(self, symbol: str, from_date, to_date, adjusted: bool = True,
                                 sort='asc', limit: int = 5000, multiplier: int = 1,
                                 timespan='day', raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get aggregate bars for a stock over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then 5-minute bars will be returned - Async
        method
        `Official Docs
        <https://polygon.io/docs/get_v2_aggs_ticker__stocksTicker__range__multiplier___timespan___from___to__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param from_date: The start of the aggregate time window. Could be ``datetime`` or ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. See :class:`polygon.enums.SortOrder` for choices. ``asc`` default.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param multiplier: The size of the timespan multiplier. Must be a positive whole number.
        :param timespan: The size of the time window. See :class:`polygon.enums.Timespan` for choices. defaults to
                         ``day``
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(from_date, (datetime.date, datetime.datetime)):
            from_date = from_date.strftime('%Y-%m-%d')

        if isinstance(to_date, (datetime.date, datetime.datetime)):
            to_date = to_date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/ticker/{symbol.upper()}/range/{multiplier}/{timespan}/{from_date}/{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_grouped_daily_bars(self, date,
                                     adjusted: bool = True,
                                     raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the daily OCHLV for the entire stocks/equities markets - Async method
        `Official docs <https://polygon.io/docs/get_v2_aggs_grouped_locale_us_market_stocks__date__anchor>`__

        :param date: The date to get the data for. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """
        if isinstance(date, (datetime.date, datetime.datetime)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/grouped/locale/us/market/stocks/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_previous_close(self, symbol: str, adjusted: bool = True,
                                 raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the previous day's OCHLV for the specified stock ticker - Async method
        `Official Docs <https://polygon.io/docs/get_v2_aggs_ticker__stocksTicker__prev_anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
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

    async def get_snapshot(self, symbol: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded stock ticker - Async method
        `Official Docs
        <https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks_tickers__stocksTicker__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers/{symbol.upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_current_price(self, symbol: str) -> float:
        """
        get current market price for the ticker symbol specified - Async method

        Uses :meth:`get_last_trade` under the hood
        `Official Docs <https://polygon.io/docs/get_v2_last_trade__stocksTicker__anchor>`__

        :param symbol: The ticker symbol of the stock/equity.
        :return: The current price. A ``KeyError`` indicates the request wasn't successful.
        """

        _res = await self.get_last_trade(symbol)

        return _res['results']['p']

    async def get_snapshot_all(self, symbols: list = None, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        stock symbols - Async method
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks_tickers_anchor>`__

        :param symbols: A comma separated list of tickers to get snapshots for. Defaults to ALL tickers
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers'

        if symbols is not None:
            _data = {'tickers': ','.join([x.upper() for x in symbols])}
        else:
            _data = {'tickers': None}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_gainers_and_losers(self, direction='gainers',
                                     raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current top 20 gainers or losers of the day in stocks/equities markets - Async method
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks__direction__anchor>`__

        :param direction: The direction of results. Defaults to gainers. See :class:`polygon.enums.SnapshotDirection`
                          for choices
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/{self._change_enum(direction, str)}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


if __name__ == '__main__':  # Tests
    print('Don\'t You Dare Running Lib Files Directly')

# ========================================================= #
