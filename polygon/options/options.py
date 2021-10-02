# ========================================================= #
import requests
import httpx
from typing import Union
import datetime
from requests.models import Response
from httpx import Response as HttpxResponse
# ========================================================= #


class OptionsClient:
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