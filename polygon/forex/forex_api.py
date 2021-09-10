# ========================================================= #
import requests
import httpx
from typing import Union
import datetime
from requests.models import Response
from httpx import Response as HttpxResponse
# ========================================================= #


class ForexClient:
    def __init__(self, api_key: str, use_async: bool = False):
        """
        Initiates a Client to be used to access all the endpoints.
        :param api_key: Your API Key. Visit your dashboard to get yours.
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

    # Internal Functions
    def _get_response(self, path: str, params: dict = None,
                      raw_response: bool = True) -> Union[Response, dict]:
        """
        Get response on a path - to be used by sync client
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

    async def _get_async_response(self, path: str, params: dict = None,
                                  raw_response: bool = True) -> Union[HttpxResponse, dict]:
        """
        Get response on a path - to be used by Async operations
        :param path: RESTful path for the endpoint
        :param params: Query Parameters to be supplied with the request
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say
        check the status code or inspect the headers. Defaults to True which returns the Response object.
        :return: A Response object by default. Make `raw_response=False` to get JSON decoded Dictionary
        """
        _res = await self.session.request('GET', self.BASE + path, params=params)

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

    async def async_get_next_page_by_url(self, url: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the next page of a response. The URl is returned within next_url attribute on endpoints which support
        pagination (eg the tickers endpoint). If the response doesn't contain this attribute, either all pages were
        received or the endpoint doesn't have pagination - to be used by async operations
        :param url: The next URL. As contained in next_url of the response.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: Either a Dictionary or a Response object depending on value of raw_response. Defaults to Dict.
        """
        _res = await self.session.request('GET', url)

        if raw_response:
            return _res

        return _res.json()

    def get_historic_forex_ticks(self, from_symbol: str, to_symbol: str,
                                 date: Union[datetime.date, datetime.datetime, str], offset: Union[str, int] = None,
                                 limit: int = 500, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get historic trade ticks for a forex currency pair.
        Official Docs: https://polygon.io/docs/get_v1_historic_forex__from___to___date__anchor
        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param date: The date/day of the historic ticks to retrieve. Could be datetime, date or string 'YYYY-MM-DD'
        :param offset: The timestamp offset, used for pagination. This is the offset at which to start the results.
         Using the timestamp of the last result as the offset will give you the next page of results.
        :param limit: Limit the size of the response, max 10000. Default 500
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
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
        Official Docs: https://polygon.io/docs/get_v1_last_quote_currencies__from___to__anchor
        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v1/last_quote/currencies/{from_symbol.upper()}/{to_symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_aggregate_bars(self, symbol: str, from_date: Union[datetime.date, datetime.datetime, str],
                           to_date: Union[datetime.date, datetime.datetime, str], multiplier: int = 1,
                           timespan: str = 'day', adjusted: bool = True, sort: str = 'asc', limit: int = 5000,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get aggregate bars for a forex pair over a given date range in custom time window sizes.
        For example, if timespan = ‘minute’ and multiplier = ‘5’ then 5-minute bars will be returned.
        Official Docs:
         https://polygon.io/docs/get_v2_aggs_ticker__forexTicker__range__multiplier___timespan___from___to__anchor
        :param symbol: The ticker symbol of the forex pair. eg: C:EURUSD
        :param from_date: The start of the aggregate time window. Could be datetime, date or string 'YYYY-MM-DD'
        :param to_date: The end of the aggregate time window. Could be datetime, date or string 'YYYY-MM-DD'
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
        Set this to False to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. asc will return results in ascending order (oldest at the top),
        desc will return results in descending order (newest at the top).
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
         Default 5000.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if isinstance(from_date, datetime.datetime) or isinstance(from_date, datetime.date):
            from_date = from_date.strftime('%Y-%m-%d')

        if isinstance(to_date, datetime.datetime) or isinstance(to_date, datetime.date):
            to_date = to_date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/ticker/{symbol.upper()}/range/{multiplier}/{timespan}/{from_date}/{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_grouped_daily_bars(self, date: Union[datetime.date, datetime.datetime, str], adjusted: bool = True,
                               raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the daily open, high, low, and close (OHLC) for the entire forex markets.
        Official Docs: https://polygon.io/docs/get_v2_aggs_grouped_locale_global_market_fx__date__anchor
        :param date: The date for the aggregate window. Could be datetime, date or string 'YYYY-MM-DD'
        :param adjusted:  Whether or not the results are adjusted for splits. By default, results are adjusted. Set
         this to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
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
        Official Docs: https://polygon.io/docs/get_v2_aggs_ticker__forexTicker__prev_anchor
        :param symbol: The ticker symbol of the forex pair.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
        to False to get results that are NOT adjusted for splits.
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

    def get_snapshot_all(self, symbols: list, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        forex symbols
        Official Docs: https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex_tickers_anchor
        :param symbols: A list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
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
         Official Docs: https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex_tickers__ticker__anchor
        :param symbol: Symbol of the forex pair
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_gainers_and_losers(self, direction: str = 'gainers', raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current top 20 gainers or losers of the day in forex markets.
        Official docs: https://polygon.io/docs/get_v2_snapshot_locale_global_markets_forex__direction__anchor
        :param direction: The direction of the snapshot results to return. Default: 'gainers'. Can be 'losers' too
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
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
        Official Docs: https://polygon.io/docs/get_v1_conversion__from___to__anchor
        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param amount: The amount to convert,
        :param precision: The decimal precision of the conversion. Defaults to 2 which is 2 decimal places accuracy.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v1/conversion/{from_symbol.upper()}/{to_symbol.upper()}'

        _data = {'amount': amount,
                 'precision': precision}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


if __name__ == '__main__':  # Tests
    print('Don\'t You Dare Running Lib Files Directly')
    import antigravity  # Fly Me to The Moon
    from pprint import pprint
    from polygon import cred

    client = ForexClient(cred.KEY)
    pprint(client.get_gainers_and_losers('lol', raw_response=True))
    # print(client.get_current_price('AMD'))

# ========================================================= #
