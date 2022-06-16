
.. _async_streaming_header:

Async Streaming
===============

A convenient wrapper around the `Streaming API <https://polygon.io/docs/websockets/getting-started>`__

**IMPORTANT** Polygon.io allows one simultaneous connection to one cluster at a time (clusters: stocks, options, forex, crypto).
which means 4 total concurrent streams (Of course you need to have subscriptions for them).

**Connecting to a cluster which already has an existing stream connected to it would result in existing connection getting dropped and new connection would be established**

Note that This page describes the asyncio based streaming client.
If you're looking for callback based streaming client, See :ref:`callback_streaming_header`

Also note that async client has a reconnection mechanism built into it already. It is very basic at the moment. It resubscribes to the same set of services it already had
before the disconnection and restores the handlers when reconnection establishes. More info in starting the stream below.

It also exposes a few methods which you could use to create your own reconnect mechanism. Method :meth:`polygon.streaming.async_streaming.AsyncStreamClient.reconnect` is one of them

Have a reconnect mechanism to share? Share in `discussions <https://github.com/pssolanki111/polygon/discussions>`__ or on the `wiki <https://github.com/pssolanki111/polygon/wiki>`__.

Creating the client
-------------------

Creating a client is just creating an instance of ``polygon.AsyncStreamClient``. Note that this expects a few arguments where most of them have default values.

This is how the initializer looks like:

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.__init__
   :noindex:

Example use:

.. code-block:: python

  import polygon

  stream_client = polygon.AsyncStreamClient('KEY', 'stocks')  # in the simplest form

Note that you don't have to call login methods as the library does it internally itself.

Starting the Stream
-------------------

Once you have a stream client, you MUST subscribe to streams before you start the main stream loop. Note that you can alter your subscriptions from other coroutines easily even after
starting the main stream loop. See subscriptions methods below this section to know how to subscribe to streams.

AFTER you have called your initial subscription methods, you have two ways to start the main stream loop.

Without using the built-in reconnect functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case you'd need to have your own while loop, like so:

.. code-block:: python

  # assuming we create the client and sub to stream here already.
  while 1:
      await stream_client.handle_messages()

and that's basically it. handle_message would take care of receiving messages and calling appropriate handlers (see below section for info on that aspect).
You may want to implement your own reconnect mechanism here.

If that's your use case, you can basically ignore the below section completely.

Using the built-in reconnect functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

here you don't need any outer while loop of your own. The lib has inner while loops and mechanisms to trap disconnection errors and will attempt to reconnect.

Note that this function is basic and not perfect yet and will continue to improve as we move ahead. If you figure out a way to implement reconnection, feel free to share that
in `discussions <https://github.com/pssolanki111/polygon/discussions>`__ or on the `wiki <https://github.com/pssolanki111/polygon/wiki>`__.

simple use example

.. code-block:: python

  # assuming we already have a client subscribed to streams
  await stream_client.handle_messages(reconnect=True)

That's it. This should be enough for most users. For those who need more control over the behavior here; this is how the method definition looks like:

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.handle_messages
   :noindex:

Subscribing/Unsubscribing to Streams
------------------------------------

All subscription methods have names in pattern ``subscribe_service_name`` and ``unsubscribe_service_name``.

Symbols names must be specified as a list of symbols: ``['AMD', 'NVDA', 'LOL']`` is the correct way to specify symbols.
Not specifying a list of symbols results in the action being applied to ``ALL`` tickers in that service.
Note that either of ``[]``, ``None``, ``['*']`` or ``'all'`` as value of symbols would also results in ALL tickers.

The library allows specifying a string for symbol argument (that string is sent exactly as it is without processing), 
but only do that if you have the absolute need to. Most people should just specify a list. Note that a list of single
ticker is accepted.

**Options and Crypto stream endpoints expect prefixes ``O:, X:`` respectively in front of every ticker. The library handles this for you**
so you can pass symbols with or without those prefixes.

The Second argument on all unsubscribe methods is the ``handler_function`` which represents the handler function you'd like the library to call when a message from that service is
received. You can have one handler for multiple services. Not supplying a handler results in the library using the default message handler.

All methods are async coroutines which need to be awaited.

``await stream_client.subscribe_stock_trades(['AMD', 'NVDA'], handler_function=my_handler_function)``

By default, the library will also enforce upper case for all symbols being passed. To disable this enforcement, just 
pass in ``force_uppercase_symbols=False`` when subscribing in the methods below.

Handling Messages
-----------------

your handler functions should accept one argument which indicates the message.

.. code-block:: python

  async def sample_handler(msg):
      print(f'Look at me! I am the handler now. {msg}')

Note that you can also use a sync function as handler

.. code-block:: python

  def sample_handler(msg):
      print(f'I am also a handler. But sync.. {msg}')

In async streaming, **the library does the json decoding for you internally, and you will always receive a list/dict python object** (a list 99.99% of the time except the initial status
messages). **You don't have to do** ``json decoding`` **yourself**. Internally it is already done using ``json.loads(msg)``

Once you have the message in your callback handler function, you can process it the way you want. print it out, write it to a file, push it to a redis queue, write to a database,
offload to a multi-threaded queue. Just whatever.

The default handler for the messages is ``_default_process_message``.

Changing message handler functions while stream is running
----------------------------------------------------------

Library allows you to change your handlers after your main stream loop has started running.

The function you'd need is:

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.change_handler
   :noindex:

Note that you should never need to change handler for ``status`` ( which handles ``ev`` messages) unless you know you got a situation. Service prefixes just indicate which service (eg stock trades? options aggregates?)
you want to change the handler.

Closing the Stream
------------------

To turn off the streamer and shut down the websockets connection gracefully, it is advised to ``await stream_client.close_stream()``
when closing the application. Not an absolute necessity but a good software practice.

**Streams**

Stock Streams
-------------

Stock Trades
~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_stock_trades
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_stock_trades
   :noindex:

Stock Quotes
~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_stock_quotes
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_stock_quotes
   :noindex:

Stock Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_stock_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_stock_minute_aggregates
   :noindex:

Stock Second Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_stock_second_aggregates
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_stock_second_aggregates
   :noindex:

Stock Limit Up Limit Down (LULD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_stock_limit_up_limit_down
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_stock_limit_up_limit_down
   :noindex:

Stock Imbalances
~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_stock_imbalances
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_stock_imbalances
   :noindex:

Options Streams
---------------

Options Trades
~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_option_trades
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_option_trades
   :noindex:

Options Quotes
~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_option_quotes
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_option_quotes
   :noindex:

Options Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_option_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_option_minute_aggregates
   :noindex:

Options Second Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_option_second_aggregates
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_option_second_aggregates
   :noindex:


Forex Streams
-------------

Forex Quotes
~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_forex_quotes
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_forex_quotes
   :noindex:

Forex Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_forex_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_forex_minute_aggregates
   :noindex:

Crypto Streams
--------------

Crypto Trades
~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_crypto_trades
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_crypto_trades
   :noindex:

Crypto Quotes
~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_crypto_quotes
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_crypto_quotes
   :noindex:

Crypto Minute Aggregates (OCHLV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_crypto_minute_aggregates
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_crypto_minute_aggregates
   :noindex:

Crypto Level 2 Book
~~~~~~~~~~~~~~~~~~~

.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.subscribe_crypto_level2_book
   :noindex:
.. automethod:: polygon.streaming.async_streaming.AsyncStreamClient.unsubscribe_crypto_level2_book
   :noindex:


