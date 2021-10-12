
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

**A detailed description of how to use the streaming endpoints is provided in the streamer docs linked above.**

Creating and Using REST HTTP clients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section aims to outline the general procedure to create and use the http clients in both regular and async programming methods.

First up, you'd import the library. There are many ways to import names from a library and it is highly recommended to complete fundamental python if you're not aware of them.

.. code-block:: python

  import polygon

Now creating a client is as simple as (using stocks client as an example here)

1. Regular client: ``stocks_client = polygon.StocksClient('API_KEY')``
#. Async client: ``forex_client = polygon.ForexClient('API_KEY', True)``

Note that It is NOT recommended to hard code your API key or other credentials into your code unless you really have a use case. Instead preferably do one of the following:

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


Using context managers ensures that the connections opened up to make requests are closed properly.

You can manually close the connections if you're not using context managers:

1. for regular non-async: ``client.close()``
#. for async: ``await client.async_close()``

This is not an absolute necessity but rather a good software practice to close out resources when you don't need them.

Calling the methods/functions
-----------------------------

Most methods and functions have sane default values which can be customized as needed. Required parameters need to be
supplied as positional arguments (which just means that the order of arguments matter when passing more than one).

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

This gives you an async client. Similar to sync, you can have all 5 different clients together.

**ALL the methods you'd use for async client have** ``async_`` **in front of their sync counterpart names.**

So if a method is named ``get_trades()`` in usual client, in async client you'd have it as ``async_get_trades()``
and this behavior is true for all methods

Here is how you can use it grab the current price of a symbol

.. code-block:: python

  import polygon

  async def main():
      stocks_client = polygon.StocksClient('API_KEY', True)

      current_price = await stocks_client.async_get_current_price('AMD')
      print(current_price)

  if __name__ == '__main__':
      import asyncio
      asyncio.run(main())


Note that I'm working towards avoiding this name difference across sync and async clients. Feedback is appreciated.

**so good so far? Start by taking a look at the complete docs for endpoints you need. Here is a quick list**

* :ref:`stocks_header`
* :ref:`options_header`
* :ref:`forex_header` and :ref:`crypto_header`
* :ref:`callback_streaming_header` and :ref:`async_streaming_header`
* :ref:`enums_header`
