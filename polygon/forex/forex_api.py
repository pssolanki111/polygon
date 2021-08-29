# ========================================================= #
import requests
from typing import Union
import datetime
from requests.models import Response


# ========================================================= #


class ForexClient:
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


# ========================================================= #


if __name__ == '__main__':  # Tests
    from pprint import pprint
    from polygon import cred

    print('Don\'t You Dare Running Lib Files Directly :/')
    client = ForexClient(cred.KEY)
    pprint(client.get_gainers_and_losers('lol', raw_response=True))
    # print(client.get_current_price('AMD'))

# ========================================================= #
