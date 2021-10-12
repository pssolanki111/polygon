
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

Example use:

.. code-block:: python

  import polygon

  stream_client = polygon.StreamClient('KEY', 'stocks', on_message=my_own_handler_function)  # in the simplest form


Starting the Stream
-------------------

Once you have a stream client, you can start the stream thread by calling the method: ``start_stream_thread``.

This method has default values which should be good enough for most people. For those who need customization, here is how it looks like:

.. automethod:: polygon.streaming.streaming.StreamClient.start_stream_thread

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

All subscription methods have names in pattern ``subscribe_service_name`` and ``unsubscribe_service_name``.

Symbols names must be specified as a list of symbols: ``['AMD', 'NVDA', 'LOL']`` is the correct way to specify symbols.
Not specifying a list of symbols results in the action being applied to ``ALL`` tickers in that service.

You'd also notice that subscribe methods have an argument with name ``action`` which defaults to subscribe. You should never need to change/specify that parameter at all.
To unsubscribe, use the relevant methods instead.

Handling messages
~~~~~~~~~~~~~~~~~

Your handler function should accept one argument which is the message received.

.. code-block:: python

  def sample_handler(msg):
      print(msg)

Once you have the message in your callback handler function, you can process it the way you want. print it out, write it to a file, push it to a redis queue, write to a database,
offload to a multi-threaded queue. Just whatever.

The default handler for the messages is ``_default_on_msg`` which does some checks on messages having event as ``status``. and prints out other messages.
Messages from polygon having the key ``ev`` equal to ``status`` are status updates from polygon about login and relevant actions you take (ev indicates event)

The data messages will have different ``ev`` value than the string 'status'. The ev values would match the :class:`polygon.enums.StreamServicePrefix` values.

You can specify your own handlers for other callbacks too or leave those to defaults.

Closing Stream
~~~~~~~~~~~~~~

To turn off the streamer and shut down the websockets connection gracefully, it is advised to call ``stream_client.close_stream()`` method
when closing the application. Not an absolute necessity but a good software practice.

Stocks Streams
--------------

Stock Trades
~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_trades
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_trades

Stock Quotes
~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_quotes
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_quotes

Stock Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_minute_aggregates
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_minute_aggregates

Stock Second Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_second_aggregates
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_second_aggregates

Stock Limit Up Limit Down (LULD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_limit_up_limit_down
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_limit_up_limit_down

Stock Imbalances
~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_stock_imbalances
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_stock_imbalances

Options Streams
---------------

Options Trades
~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_option_trades
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_option_trades

Options Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_option_minute_aggregates
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_option_minute_aggregates

Options Second Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_option_second_aggregates
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_option_second_aggregates


Forex Streams
-------------

Forex Quotes
~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_forex_quotes
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_forex_quotes

Forex Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_forex_minute_aggregates
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_forex_minute_aggregates

Crypto Streams
--------------

Crypto Trades
~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_crypto_trades
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_crypto_trades

Crypto Quotes
~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_crypto_quotes
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_crypto_quotes

Crypto Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_crypto_minute_aggregates
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_crypto_minute_aggregates

Crypto Level 2 Book
~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.streaming.StreamClient.subscribe_crypto_level2_book
.. automethod:: polygon.streaming.streaming.StreamClient.unsubscribe_crypto_level2_book





