
.. _getting_started_header:

Getting Started
===============

Welcome to ``polygon``. Read this page to quickly install and configure this library to write your first Polygon Python application.

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

The clients
-----------
This section would provide general guidance on the clients without going into specific endpoints as stocks or options.

As you already know polygon.io has two major classes of APIs. The ``REST`` APIs and ``websockets`` streaming APIs.

This library implements all of them.

- For REST HTTP endpoints

  + Regular client is implemented for all endpoints.
  + Support for ``async`` client is also provided. See :ref:`async_support_header` for more.

- For websocket streaming endpoints

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


**Note that you can have multiple instances of all 5 different types of http clients together. So you can create client for each one of the stocks, options and other APIs**

All the clients in the lib support context managers ``with polygon.StocksClient('KEY') as client:``.


