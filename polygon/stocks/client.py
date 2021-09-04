# ========================================================= #
import requests
from typing import Union
import datetime
from requests.models import Response
# ========================================================= #


class PolygonClient:
    def __init__(self, api_key: str):
        """
        Initiates a Client to be used to access all the endpoints.
        :param api_key: Your API Key. Visit your dashboard to get yours.
        """
        self.KEY = api_key
        self.BASE = 'https://api.polygon.io'
        self.session = requests.session()
        self.session.headers.update({'Authorization': f'Bearer {self.KEY}'})

    def _get_response(self, path: str, params: dict = None,
                      raw_response: bool = True) -> Union[Response, dict]:
        """
        Get response on a path. The structure will be changed later on and this method would be used as underlying
        function for convenience methods
        :param path: RESTful path for the endpoint
        :param params: Query Parameters to be supplied with the request
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to True which returns the Response object.
        :return: A Response object by default. Make `raw_response=False` to get JSON decoded Dictionary
        """
        _res = self.session.request('GET', self.BASE + path, params=params)

        if raw_response:
            return _res

        return _res.json()

    def get_next_page_by_url(self, url: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the next page of a response. The URl is returned within next_url attribute on endpoints which support
        pagination (eg the tickers endpoint). If the response doesn't contain this attribute, either all pages were
        received or the endpoint doesn't have pagination.
        :param url: The next URL. As contained in next_url of the response.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: Either a Dictionary or a Response object depending on value of raw_response. Defaults to Dict.
        """
        _res = self.session.request('GET', url)

        if raw_response:
            return _res

        return _res.json()

    def get_trades(self, symbol: str, date: Union[str, datetime.datetime, datetime.date], timestamp: int = None,
                   timestamp_limit: int = None, reverse: bool = True, limit: int = 5000,
                   raw_response: bool = False) -> Union[Response, dict]:
        """
        Get trades for a given ticker symbol on a specified date. The response from polygon seems to have a `map`
        attribute which gives a mapping of attribute names to readable values.
        Official Docs: https://polygon.io/docs/get_v2_ticks_stocks_trades__ticker___date__anchor

        :param symbol: The ticker symbol we want trades for.
        :param date: The date/day of the trades to retrieve. Could be `datetime` or `date` or string `YYYY-MM-DD`
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
        results. Using the `timestamp` of the last result as the offset will give you the next page of results.
        Default: None

        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
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

    def get_quotes(self, symbol: str, date: Union[str, datetime.datetime, datetime.date], timestamp: int = None,
                   timestamp_limit: int = None, reverse: bool = True, limit: int = 5000,
                   raw_response: bool = False) -> Union[Response, dict]:
        """
        Get Quotes for a given ticker symbol on a specified date. The response from polygon seems to have a `map`
        attribute which gives a mapping of attribute names to readable values.
        Official Docs: https://polygon.io/docs/get_v2_ticks_stocks_nbbo__ticker___date__anchor

        :param symbol: The ticker symbol we want quotes for.
        :param date: The date/day of the quotes to retrieve. Could be `datetime` or `date` or string `YYYY-MM-DD`
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
        results. Using the `timestamp` of the last result as the offset will give you the next page of results.
        Default: None

        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
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

    def get_last_trade(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the most recent trade for a given stock.
        Official Docs: https://polygon.io/docs/get_v2_last_trade__stocksTicker__anchor
        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v2/last/trade/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_last_quote(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the most recent NBBO (Quote) tick for a given stock.
        Official Docs: https://polygon.io/docs/get_v2_last_nbbo__stocksTicker__anchor
        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v2/last/nbbo/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_daily_open_close(self, symbol: str, date: Union[str, datetime.datetime, datetime.date],
                             adjusted: bool = True, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the OCHLV and after-hours prices of a stock symbol on a certain date.
        Official Docs: https://polygon.io/docs/get_v1_open-close__stocksTicker___date__anchor
        :param symbol: The ticker symbol we want daily-OCHLV for.
        :param date: The date/day of the daily-OCHLV to retrieve. Could be `datetime` or `date` or string `YYYY-MM-DD`
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
        to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v1/open-close/{symbol.upper()}/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_aggregate_bars(self, symbol: str, from_date: Union[str, datetime.datetime, datetime.date],
                           to_date: Union[str, datetime.datetime, datetime.date], adjusted: bool = True,
                           sort: str = 'asc', limit: int = 5000, multiplier: int = 1,
                           timespan: str = 'day', raw_response: bool = False) -> Union[Response, dict]:
        """
        Get aggregate bars for a stock over a given date range in custom time window sizes.
        For example, if timespan = ‘minute’ and multiplier = ‘5’ then 5-minute bars will be returned.
        Official Docs:
          https://polygon.io/docs/get_v2_aggs_ticker__stocksTicker__range__multiplier___timespan___from___to__anchor
        :param symbol: The ticker symbol of the stock/equity.
        :param from_date: The start of the aggregate time window. Could be `datetime` or `date` or string `YYYY-MM-DD`
        :param to_date: The end of the aggregate time window. Could be `datetime` or `date` or string `YYYY-MM-DD`
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
         to false to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. 'asc' -> oldest at the top. 'desc' -> newest at the top
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
         Default 5000.
        :param multiplier: The size of the timespan multiplier. Must be a positive whole number.
        :param timespan: The size of the time window. Must be one of 'minute', 'hour', 'day', 'week', 'month',
        'quarter', 'year'
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if isinstance(from_date, datetime.date) or isinstance(from_date, datetime.datetime):
            from_date = from_date.strftime('%Y-%m-%d')

        if isinstance(to_date, datetime.date) or isinstance(to_date, datetime.datetime):
            to_date = to_date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/ticker/{symbol.upper()}/range/{multiplier}/{timespan}/{from_date}/{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_grouped_daily_bars(self, date: Union[str, datetime.datetime, datetime.date],
                               adjusted: bool = True, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the daily OCHLV for the entire stocks/equities markets.
        Official docs: https://polygon.io/docs/get_v2_aggs_grouped_locale_us_market_stocks__date__anchor
        :param date: The date to get the data for. Could be `datetime` or `date` or string `YYYY-MM-DD`
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """
        if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
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
        Official Docs: https://polygon.io/docs/get_v2_aggs_ticker__stocksTicker__prev_anchor
        :param symbol: The ticker symbol of the stock/equity.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
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
        Official Docs:
          https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks_tickers__stocksTicker__anchor
        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_current_price(self, symbol: str) -> float:
        """
        get current market price for the ticker symbol specified. Uses the LastTrade endpoint under the hood
        Official Docs: https://polygon.io/docs/get_v2_last_trade__stocksTicker__anchor
        :param symbol: The ticker symbol of the stock/equity.
        :return: The current price. A KeyError indicates the request wasn't successful.
        """

        return self.get_last_trade(symbol)['results']['p']

    def get_snapshot_all(self, symbols: list, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        stock symbols.
        Official Docs: https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks_tickers_anchor
        :param symbols: A comma separated list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if not isinstance(symbols, list):
            raise ValueError('symbols must be supplied as a list of tickers')

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers'

        _data = {'tickers': ','.join([x.upper() for x in symbols])}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_gainers_and_losers(self, direction: str = 'gainers', raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current top 20 gainers or losers of the day in stocks/equities markets.
        Official Docs: https://polygon.io/docs/get_v2_snapshot_locale_us_markets_stocks__direction__anchor
        :param direction: The direction of results. Defaults to gainers. Must be one of 'gainers', 'losers'.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/{direction}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


if __name__ == '__main__':  # Tests
    print('Don\'t You Dare Running Lib Files Directly')

    from pprint import pprint
    from polygon import cred

    client = PolygonClient(cred.KEY)
    pprint(client.get_gainers_and_losers('lol', raw_response=True))
    # print(client.get_current_price('AMD'))

# ========================================================= #
