# ========================================================= #
import requests
from typing import Union
import datetime
from requests.models import Response
# ========================================================= #


class ReferenceClient:
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

    def get_tickers(self, symbol: str = '', ticker_lt=None, ticker_lte=None, ticker_gt=None, ticker_gte=None,
                    symbol_type: str = '', market: str = '', exchange: str = '', cusip: str = None, cik: str = '',
                    date: Union[str, datetime.date, datetime.datetime] = None, search: str = None,
                    active: bool = True, sort: str = 'ticker', order: str = 'asc', limit: int = 100,
                    raw_response: bool = False) -> Union[Response, dict]:
        """
        Query all ticker symbols which are supported by Polygon.io. This API currently includes Stocks/Equities, Crypto,
         and Forex.
        Official Docs: https://polygon.io/docs/get_v3_reference_tickers_anchor
        :param symbol: Specify a ticker symbol. Defaults to empty string which queries all tickers.
        :param ticker_lt: Return results where this field is less than the value.
        :param ticker_lte: Return results where this field is less than or equal to the value.
        :param ticker_gt: Return results where this field is greater than the value.
        :param ticker_gte: Return results where this field is greater than or equal to the value.
        :param symbol_type: Specify the type of the tickers. Find the types that we support via our Ticker Types API.
        Defaults to empty string which queries all types.
        Types docs: https://polygon.io/docs/get_v2_reference_types_anchor
        :param market: Filter by market type. By default all markets are included. One of 'stocks', 'crypto', 'fx'
        :param exchange: Specify the primary exchange of the asset in the ISO code format. Find more information about
        the ISO codes at the ISO org website. Defaults to empty string which queries all exchanges.
        ISO org website: https://www.iso20022.org/market-identifier-codes
        :param cusip: Specify the CUSIP code of the asset you want to search for. Find more information about CUSIP
        codes at their website. Defaults to empty string which queries all CUSIPs.
        Website for CUSIP: https://www.cusip.com/identifiers.html#/CUSIP
        :param cik: Specify the CIK of the asset you want to search for. Find more information about CIK codes at their
         website. Defaults to empty string which queries all CIKs.
         CIK website: https://www.sec.gov/edgar/searchedgar/cik.htm
        :param date: Specify a point in time to retrieve tickers available on that date. Defaults to the most recent
         available date. Could be datetime, date or a string 'YYYY-MM-DD'
        :param search: Search for terms within the ticker and/or company name. for eg 'MS' will match matching symbols
        :param active: Specify if the tickers returned should be actively traded on the queried date. Default is true.
        :param sort: The field to sort the results on. Default is ticker. If the search query parameter is present,
        sort is ignored and results are ordered by relevance. For options, see docs.
        :param order: The order to sort the results on. Default is asc (ascending). Use 'desc' for descending
        :param limit: Limit the size of the response, default is 100 and max is 1000. Pagination is supported by the
        pagination support function
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
        status code or inspect the headers. Defaults to False which returns the json decoded dictionary.
        :return: A JSON decoded Dictionary by default. Make `raw_response=True` to get underlying response object
        """

        if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
            date = date.strftime('%Y-%m-%d')

        _path = '/v3/reference/tickers'

        _data = {'ticker': symbol,
                 'ticker.lt': ticker_lt, 'ticker.lte': ticker_lte,
                 'ticker.gt': ticker_gt, 'ticker.gte': ticker_gte,
                 'type': symbol_type,
                 'market': market,
                 'exchange': exchange,
                 'cusip': cusip,
                 'cik': cik,
                 'date': date,
                 'search': search,
                 'active': active,
                 'sort': sort,
                 'order': order,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_next_page_tickers(self, old_response: Union[Response, dict],
                              raw_response: bool = False) -> Union[Response, dict, bool]:
        """
        Get the next page using the most recent yet old response. This function simply parses the next_url attribute
        from the  existing response and uses it to get the next page. Returns False if there is no next page
        remaining (which implies that you have reached the end of all pages).
        :param old_response:
        :param raw_response:
        :return:
        """

        try:
            if not isinstance(old_response, dict):
                old_response = old_response.json()

            _next_url = old_response['next_url']

            return self.get_next_page_by_url(_next_url, raw_response=raw_response)

        except KeyError:
            return False


# ========================================================= #


if __name__ == '__main__':
    from pprint import pprint
    from polygon import cred

    print('Don\'t You Dare Running Lib Files Directly :/')
    client = ReferenceClient(cred.KEY)

    pprint(client.get_tickers(limit=500))


# ========================================================= #
