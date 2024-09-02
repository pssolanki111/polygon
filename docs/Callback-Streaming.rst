
.. _callback_streaming_header:

Callback Streaming
==================

A convenient wrapper around the `Streaming API <https://polygon.io/docs/websockets/getting-started>`__

**IMPORTANT** Polygon.io allows one simultaneous connection to one cluster at a time (clusters: stocks, options, forex, crypto).
which means 4 total concurrent streams (Of course you need to have subscriptions for them).

**Connecting to a cluster which already has an existing stream connected to it would result in existing connection getting dropped and new connection would be established**

Note that This page describes the callback based streaming client.
If you're looking for async based streaming client, See :ref:`async_streaming_header`

Also note that callback based streamer is supposed to get a builtin functionality to reconnect in the library. Async streamer has it already. It's on TODO for this client.
Have a reconnect mechanism to share? Share in `discussions <https://github.com/pssolanki111/polygon/discussions>`__ or on the `wiki <https://github.com/pssolanki111/polygon/wiki>`__.

Creating the client
-------------------

Creating a client is just creating an instance of ``polygon.StreamClient``. Note that this expects a few arguments where most of them have default values.

This is how the initializer looks like:

.. automethod:: polygon.streaming.streaming.StreamClient.__init__
   :noindex:

Example use:

.. code-block:: python

  import polygon

  stream_client = polygon.StreamClient('KEY', 'stocks', on_message=my_own_handler_function)  # in the simplest form

Note that you don't have to call login methods as the library does it internally itself.

Starting the Stream
-------------------

Once you have a stream client, you can start the stream thread by calling the method: ``start_stream_thread``.

This method has default values which should be good enough for most people. For those who need customization, here is how it looks like:

.. automethod:: polygon.streaming.streaming.StreamClient.start_stream_thread
   :noindex:

Example use:

.. code-block:: python

  import polygon

  stream_client = polygon.StreamClient('KEY', 'stocks', on_message=my_own_handler_function)

  stream_client.start_stream_thread()

  # subscriptions here.

Important Concepts
------------------

Important stuff to know before you connect your first stream. Note that when writing applications, you should create the client and start the stream thread before subscribing.

Subscribing/Unsubscribing to Streams
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All subscription methods have names in pattern ``subscribe_service_name`` and ``unsubscribe_service_name`` (listed below)

Symbols names must be specified as a list of symbols: ``['AMD', 'NVDA', 'LOL']`` is the correct way to specify symbols.
Not specifying a list of symbols results in the action being applied to ``ALL`` tickers in that service.
Note that either of ``[]``, ``None``, ``['*']`` or ``'all'`` as value of symbols would also results in ALL tickers.

The library allows specifying a string for symbol argument (that string is sent exactly as it is without processing), 
but only do that if you have the absolute need to. Most people should just specify a list. Note that a list of single
ticker is accepted.

**Options and Crypto stream endpoints expect prefixes ``O:, X:`` respectively in front of every ticker. The library handles this for you**
so you can pass symbols with or without those prefixes.

By default, the library will also enforce upper case for all symbols being passed. To disable this enforcement, just 
pass in ``force_uppercase_symbols=False`` when subscribing in the methods below.

Handling messages
~~~~~~~~~~~~~~~~~

Your handler function should accept two arguments. You can ignore the first argument which is going to be the websocket instance itself. The second argument is the actual message.

In callback streaming, **the library can't do the json decoding for you internally, and you will always receive a raw string** as received from the websocket server.
messages). **You will have to do** ``json decoding`` **yourself**.

.. code-block:: python

  def sample_handler(ws, msg):
      print(msg)  # here msg is the raw string which contains the msg. to convert it to a list/dict, it needs to be decoded.

      # DECODING the msg from string to list/dict
      # ensure you have 'import json' at the top of file in imports

      msg = json.loads(msg)  # now msg is a python object which you can use easily to access data from.

Once you have the message in your callback handler function, you can process it the way you want. print it out, write it to a file, push it to a redis queue, write to a database,
offload to a multi-threaded queue. Just whatever.

The default handler for the messages is ``_default_on_msg`` which does some checks on messages having event as ``status``. and prints out other messages.
Messages from polygon having the key ``ev`` equal to ``status`` are status updates from polygon about login and relevant actions you take (ev indicates event)

The data messages will have different ``ev`` value than the string 'status'. The ev values for those would match the :class:`polygon.enums.StreamServicePrefix` values.

You can specify your own handlers for other callbacks (``on_error``, ``on_close`` etc) too or leave those to defaults.

**if you choose to override default handlers for** ``on_error`` **and** ``on_close``, **here is how they need to be written**

``on_error`` handler must accept two arguments. You can ignore the first argument which is just the websocket instance itself. The second argument is going to be the actual error

.. code-block:: python

  def sample_error_handler(ws, error):
      print(error)

``on_close`` handler must accept three arguments. you can ignore the first arg which is just the websocket instance itself. The second arg is close code, and third would be the
close message. note that this handler is only called when the stream is being closed.

.. code-block:: python

  def sample_close_handler(ws, close_code, close_msg):
      print(f'Stream close with code: {close_code} || msg: {close_msg}')

Closing Stream
~~~~~~~~~~~~~~

To turn off the streamer and shut down the websockets connection gracefully, it is advised to call ``stream_client.close_stream()`` method
when closing the application. Not an absolute necessity but a good software practice.

**Streams**

Common Streams
--------------

these streams are available in 4 clusters (stocks, options, forex, crypto) EXCEPT indices

Fair Market Value (FMV)
~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_fair_market_value
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_fair_market_value
   :noindex:


Stocks Streams
--------------

Stock Trades
~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_trades
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_trades
   :noindex:

Stock Quotes
~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_quotes
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_quotes
   :noindex:

Stock Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_minute_aggregates
   :noindex:

Stock Second Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_second_aggregates
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_second_aggregates
   :noindex:

Stock Limit Up Limit Down (LULD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_limit_up_limit_down
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_limit_up_limit_down
   :noindex:

Stock Imbalances
~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_imbalances
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_imbalances
   :noindex:

Options Streams
---------------

Options Trades
~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_option_trades
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_option_trades
   :noindex:

Options Quotes
~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_option_quotes
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_option_quotes
   :noindex:

Options Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_option_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_option_minute_aggregates
   :noindex:

Options Second Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_option_second_aggregates
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_option_second_aggregates
   :noindex:


Forex Streams
-------------

Forex Quotes
~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_forex_quotes
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_forex_quotes
   :noindex:

Forex Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_forex_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_forex_minute_aggregates
   :noindex:

Crypto Streams
--------------

Crypto Trades
~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_crypto_trades
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_crypto_trades
   :noindex:

Crypto Quotes
~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_crypto_quotes
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_crypto_quotes
   :noindex:

Crypto Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_crypto_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_crypto_minute_aggregates
   :noindex:

Crypto Level 2 Book
~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_crypto_level2_book
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_crypto_level2_book
   :noindex:

Indices Streams
---------------

Minute Aggregates
~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_indices_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_indices_minute_aggregates
   :noindex:

Second Aggregates
~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_indices_second_aggregates
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_indices_second_aggregates
   :noindex:

Value
~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_index_value
   :noindex:
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_indices_value
   :noindex:



