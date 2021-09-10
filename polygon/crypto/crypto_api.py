# ========================================================= #
import requests
import httpx
from typing import Union
import datetime
from requests.models import Response
from httpx import Response as HttpxResponse
# ========================================================= #


class CryptoClient:
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

    def get_historic_trades(self, from_symbol: str, to_symbol: str,
                            date: Union[datetime.date, datetime.datetime, str], offset: Union[str, int] = None,
                            limit: int = 500, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get historic trade ticks for a cryptocurrency pair.
        Official Docs: https://polygon.io/docs/get_v1_historic_crypto__from___to___date__anchor
        :param from_symbol: The "from" symbol of the crypto pair.
        :param to_symbol: The "to" symbol of the crypto pair.
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

        _path = f'/v1/historic/crypto/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'offset': offset,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_last_trade(self, from_symbol: str, to_symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the last trade tick for a cryptocurrency pair.
        Official Docs: https://polygon.io/docs/get_v1_last_crypto__from___to__anchor
        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v1/last/crypto/{from_symbol.upper()}/{to_symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_daily_open_close(self, from_symbol: str, to_symbol: str, date: Union[datetime.date, datetime.datetime, str],
                             adjusted: bool = True, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the open, close prices of a cryptocurrency symbol on a certain day.
        Official Docs: https://polygon.io/docs/get_v1_open-close_crypto__from___to___date__anchor
        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param date: The date of the requested open/close. Could be datetime, date or string `YYYY-MM-DD`.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v1/open-close/crypto/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_aggregate_bars(self, symbol: str, from_date: Union[datetime.date, datetime.datetime, str],
                           to_date: Union[datetime.date, datetime.datetime, str], multiplier: int = 1,
                           timespan: str = 'day', adjusted: bool = True, sort: str = 'asc', limit: int = 5000,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get aggregate bars for a cryptocurrency pair over a given date range in custom time window sizes.
        For example, if timespan = ‘minute’ and multiplier = ‘5’ then 5-minute bars will be returned.
        Official Docs:
         https://polygon.io/docs/get_v2_aggs_ticker__cryptoTicker__range__multiplier___timespan___from___to__anchor
        :param symbol: The ticker symbol of the currency pair. eg: X:BTCUSD
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
        Get the daily open, high, low, and close (OHLC) for the entire cryptocurrency markets.
        Official Docs: https://polygon.io/docs/get_v2_aggs_grouped_locale_global_market_crypto__date__anchor
        :param date: The date for the aggregate window. Could be datetime, date or string 'YYYY-MM-DD'
        :param adjusted:  Whether or not the results are adjusted for splits. By default, results are adjusted. Set
         this to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if isinstance(date, datetime.datetime) or isinstance(date, datetime.date):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/grouped/locale/global/market/crypto/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_previous_close(self, symbol: str, adjusted: bool = True,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified cryptocurrency pair.
        Official Docs: https://polygon.io/docs/get_v2_aggs_ticker__cryptoTicker__prev_anchor
        :param symbol: The ticker symbol of the currency pair.
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
        cryptocurrency symbols
        Official Docs: https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers_anchor
        :param symbols: A list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if not isinstance(symbols, list):
            raise ValueError('symbols must be supplied as a list of tickers')

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers'

        _data = {'tickers': ','.join([x.upper() for x in symbols])}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_snapshot(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
         traded cryptocurrency symbol.
        Official Docs: https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers__ticker__anchor
        :param symbol: Symbol of the currency pair
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_gainers_and_losers(self, direction: str = 'gainers', raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current top 20 gainers or losers of the day in cryptocurrency markets.
        Official docs: https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto__direction__anchor
        :param direction: The direction of the snapshot results to return. Default: 'gainers'. Can be 'losers' too
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/{direction}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_level2_book(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current level 2 book of a single ticker. This is the combined book from all of the exchanges.
        Official Docs: https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers__ticker__book_anchor
        :param symbol: The cryptocurrency ticker.
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers/{symbol.upper()}/book'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


if __name__ == '__main__':
    print('Don\'t You Dare Running Lib Files Directly')

    from pprint import pprint
    from polygon import cred

    client = CryptoClient(cred.KEY)

    res = client.get_snapshot_all(raw_response=False, symbols=['X:BTCUSD', 'BTC'])

    # res2 = client.get_next_page_news(res, raw_response=False)

    pprint(res)
    # pprint(res2)

# ========================================================= #
