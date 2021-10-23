
.. _getting_started_header:

Getting Started
===============

Welcome to ``polygon``. Read this page to quickly install and configure this library to write your first Polygon Python application.

**It is highly recommended to read this page to the full as it has important information**

What you need to have
---------------------

1. A `polygon.io account <https://polygon.io/>`__ and your ``API key``. Find your api key on `Your Dashboard <https://polygon.io/dashboard/api-keys>`__
#. Python version 3.6 or higher. Don't have it installed? `Install python <https://www.python.org/downloads/>`__

Once you have done these, Proceed to the installation of the library. Skip if already done.

Installing ``polygon``
----------------------

The recommended method of installation for all users is to install using ``pip`` from PyPi. A virtual environment is highly recommended but not a necessity.

run the below command in terminal (same for all OS)

.. code-block:: shell

  pip install polygon

To confirm the install worked, try importing the package as such

.. code-block:: python

  import polygon

If this doesn't throw any errors, the install worked. You may proceed to next steps now.

.. _create_and_use_header:

General guide for clients
-------------------------
This section would provide general guidance on the clients without going into specific endpoints as stocks or options.

As you already know polygon.io has two major classes of APIs. The ``REST`` APIs and ``websockets`` streaming APIs.

This library implements all of them.

- For `REST HTTP endpoints <https://polygon.io/docs/getting-started>`__

  + Regular client is implemented for all endpoints.
  + Support for ``async`` client is also provided. See :ref:`async_support_header` for more.

- For `websocket streaming endpoints <https://polygon.io/docs/websockets/getting-started>`__

  + a ``callback`` based stream client is implemented. See :ref:`callback_streaming_header`
  + an async based stream client is also implemented. See :ref:`async_streaming_header`

Be sure to check out our special section :ref:`enums_header` for info on ``enums`` which will be used in many functions in this library to avoid passing error prone data.

**A detailed description of how to use the streaming endpoints is provided in the streamer docs linked above.**

Need examples? The `github repository <https://github.com/pssolanki111/polygon>`__ has a few you could use.

Creating and Using REST HTTP clients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section aims to outline the general procedure to create and use the http clients in both regular and async programming methods.

First up, you'd import the library. There are many ways to import names from a library and it is highly recommended to complete fundamental python if you're not aware of them.

.. code-block:: python

  import polygon

  # OR import the name you need
  from polygon import StocksClient

  # OR import the names you need
  from polygon import (StocksClient, ForexClient, StreamClient, build_option_symbol)

Now creating a client is as simple as (using stocks and forex clients as examples here)

1. Regular client: ``stocks_client = polygon.StocksClient('API_KEY')``
#. Async client: ``forex_client = polygon.ForexClient('API_KEY', True)``

**You can also specify timeouts on requests. By default the timeout is set to 10 seconds** for both connection timeout and read timeout which
should be fine for most people. You can specify both connect and read OR either one of them.
If you're unsure of what this implies, it's just the max time limit to specify for a request. Don't change it unless you
know you need to.

.. code-block:: python

  # client with a custom timeout. Default is 10 seconds
  client = polygon.StocksClient('api_key', connect_timeout=15)

  # another one
  client = polygon.StocksClient('api_key', connect_timeout=5, read_timeout=5)

  # An async one now
  client = polygon.StocksClient('key', True, read_timeout=5)

  # another async one
  client = polygon.StocksClient('key', True, read_timeout=5, connect_timeout=15)

Note that It is NOT recommended to hard code your API key or other credentials into your code unless you really have a use case.
Instead preferably do one of the following:

1. create a separate python file with credentials, import that file into main file and reference using variable names.
#. Use environment variables.

Now that you have a client, simply call its methods to get data from the API

.. code-block:: python

  current_price = stocks_client.get_current_price('AMD')
  print(f'Current price for AMD is {current_price}')


**Note that you can have instances of all 5 different types of http clients together. So you can create client for each one of the stocks, options and other APIs**

All the clients in the lib support context managers

.. code-block:: python

  with polygon.StocksClient('KEY') as client:
      last_quote = client.get_last_quote('AMD)
      print(f'Last quote for AMD: {last_quote}')

  # OR for async
  async with polygon.StocksClient('key', True) as client:
      last_quote = await client.get_last_quote('AMD')
      print(last_quote)


Using context managers ensures that the connections opened up to make requests are closed properly.

You can manually close the connections if you're not using context managers:

1. for regular non-async: ``client.close()``
#. for async: ``await client.close()``

This is not an absolute necessity but rather a good software practice to close out resources when you don't need them.

Calling the methods/functions
-----------------------------

Most methods and functions have sane default values which can be customized as needed. Required parameters need to be
supplied as positional arguments (which just means that the order of arguments matter when passing more than one).

Some options, crypto and forex endpoints expect you to append prefixes ``O:, C:, X:`` respectively in front of tickers (on options symbols,
forex pairs and crypto pairs). **the library handles this for you** so you can pass in those with or without the prefix.

**Parameters which have special values are supplied as python enums**. You can however always pass in your own values
but it is recommended to use enums as they mitigate the possibilities of an error.

All enums are available in the module ``polygon.enums`` and can be imported the way you like.

If you're still unsure about enums, see our dedicated section: :ref:`enums_header`

Return Values
-------------

Most methods would by default return a dictionary/list object containing the data from the API. If you need the underlying response object
you need to pass in ``raw_response=True`` in the function call. It might be useful for checking ``status_code`` or inspecting ``headers``.

For 99% users, the default should be good enough.

The underlying response object returned is ``requests.models.Response`` for regular client and ``httpx.Response`` for async client.
Using ``.json()`` on the response object gets you the data dict/list

Once you have the response, you can utilize the data in any way that you like. You can push it to a database,
`create a pandas dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.from_dict.html>`__, save it to a file
or process it the way you like.

Every method's documentation contains a direct link to the corresponding official documentation page where you can see what the keys in the response mean.

.. _pagination_header:

Pagination Support
------------------

So quite a few endpoints implement pagination for large response and hence the library implements a simple mechanism to get next page of the response.
(support for previous page is also available but not all endpoints will have previous page implementation. The documentation will mention which endpoint has which kinda pagination
implementation so make sure you read that)

`This blog by polygon <https://polygon.io/blog/api-pagination-patterns/>`__ explains a few concepts around pagination and other query extensions. A good read overall.

The pagination function simply parses the ``next_url`` attribute (for next page) and ``previous_url`` attribute (for previous page) and send an authorized request using your key as
header.

**The functions will return** ``False`` **if there is no next/previous page remaining** or the endpoint doesn't support pagination.

All REST clients have these functions and you will use the same function name for all endpoints. See examples below

**first here is how the functions for pagination look like:** (click on names to see definition - **you won't have to import them with this name**. They are available
with the client you create as shown in examples below)

for usual client: :meth:`polygon.base_client.BaseClient.get_next_page` and :meth:`polygon.base_client.BaseClient.get_previous_page`

For async client: :meth:`polygon.base_client.BaseAsyncClient.get_next_page` and :meth:`polygon.base_client.BaseAsyncClient.get_previous_page`

**Examples Use**

.. code-block:: python

  # assuming a client is created already
  data = client.get_trades(<blah-blah>)

  next_page_of_data = client.get_next_page(data)  # getting NEXT page
  previous_page_of_data = client.get_previous_page(data)  # getting PREVIOUS page

  # ASYNC examples
  await client.get_next_page(data)
  await client.get_previous_page(data)

  # It's wise to check if the value returned is not False.

**In practice, to get all pages (either next or previous), you'll need a while loop** An example:

.. code-block:: python

  responses = []

  response = client.get_trades(<blah-blah>)  # using get_trades as example. you can use it on all methods which support pagination
  responses.append(response)  # using a list to store all the pages of response. You can use your own approach here.

  while 'next_url' in response.keys():  # change to 'previous_url' for previous pages
      response = client.get_next_page(response)  # similarly change to get_previous_page for previous pages.

      responses.append(response)  # adding further responses to our list. you can use your own approach.

  print('all pages received.')

.. _async_support_header:

Async Support for REST endpoints
--------------------------------

As you saw above in the example, the clients have methods for each endpoint. The usual client is a sync client.
However support for async is also provided for all the endpoints on all the clients.

Here is how to make use of it (**This info is applicable to ALL rest clients**)

First up, you'd create a client. Earlier you created a client by passing in just your API key. Here you'd create the client
with an additional argument.

so instead of something like: ``StocksClient('API_KEY')``, you'd do

.. code-block:: python

  client = StocksClient('KEY', True)   # or use_async=True for second parameter

This gives you an async client. Similar to sync, you can have all 5 different clients together. You can also pass in your timeout values like you
did above here too.

**ALL the methods you'd use for async client have the same names as their sync counterpart names.**

So if a method is named ``get_trades()`` in usual client, in async client you'd have it as ``get_trades()`` as well
and this behavior is true for all methods

Here is how you can use it grab the current price of a symbol

.. code-block:: python

  import polygon

  async def main():
      stocks_client = polygon.StocksClient('API_KEY', True)

      current_price = await stocks_client.get_current_price('AMD')
      print(current_price)

  if __name__ == '__main__':
      import asyncio
      asyncio.run(main())


Special Points
--------------

* All the date parameters in any method/function in the library can be supplied as ``datetime.date`` or ``datetime.datetime``
  You may also pass in a string in format: ``YYYY-MM-DD``.
* You would notice some parameters having ``lt``, ``lte``, ``gt`` and ``gte`` in their names. Those parameters are supposed to be filters for
  ``less than``, ``less than or equal to``, ``greater than``, ``greater than or equal to`` respectively. To know more see heading **Query Filter Extensions**
  in `This blog post by polygon <https://polygon.io/blog/api-pagination-patterns/>`__
  To explain: imagine a parameter: ``fill_date_lt``. now the date you'll supply would be a filter for values less than the given value and hence you'd get results which have fill_date
  less than your specified value, which in this case is a date.
* Some endpoints may not return a dictionary and instead return a ``list``. The number of such endpoints is very low. Similarly get current price returns a float/integer.
  I'm working towards reflecting the same in individual method's docs.
* It is highly recommended to use the polygon.io documentation website's quick test functionality to play around with the endpoints.
* Type hinting in function/method definitions indicate what data type does that parameter is supposed to be. If you think the type hinting is incomplete/incorrect, let me know.
  For example you might ses: ``cost: int`` which means this parameter ``cost`` is supposed to be an integer. ``adjusted: bool`` is another example for a boolean (either ``True`` or ``False``)
* You'll notice some type hints having ``Union`` in them followed by two or more types inside a square bracket. That simply means the parameter could be of any type from that list in bracket
  . For example: ``price: Union[str, float, int]`` means the parameter ``price`` could be either a string, a float or an integer. You'd notice Union type hints more on return types
  of the functions/methods.

**so far so good? Start by taking a look at the complete docs for endpoints you need. Here is a quick list**

* :ref:`stocks_header`
* :ref:`options_header`
* :ref:`forex_header` and :ref:`crypto_header`
* :ref:`callback_streaming_header` and :ref:`async_streaming_header`
* :ref:`enums_header`
