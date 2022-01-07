
.. _options_header:

Options
=======

Read this page to know everything you need to know about using the various Options HTTP endpoints.

See :ref:`async_support_header` for asynchronous use cases.

Docs below assume you have already read getting started page and know how to create the client.
If you do not know how to create the client, first see :ref:`create_and_use_header` and create client as below. As always you can have all 5 different clients together.

.. code-block:: python

  import polygon

  options_client = polygon.OptionsClient('KEY')  # for usual sync client
  async_options_client = polygon.OptionsClient('KEY', True)  # for an async client

here is how the client initializer looks like:

.. autofunction:: polygon.options.options.OptionsClient

**NOTE** if you don't want to use the option symbol helper functions, then you can just go to the data :ref:`option_endpoints_header` documentation

.. _option_symbols_header:

Creating Option Symbols
-----------------------

So when you're working with options (rest/websockets), you'll certainly need the option symbols which contain the information about their underlying symbol, expiry, call_or_put and the
strike price in a certain format. Many organizations tend to use different formats to represent these.

Polygon.io tends to use `This Format <https://www.optionstaxguy.com/option-symbols-osi>`__ . For those who want to understand how this formatting works,
`Here is a guide <https://docs.google.com/document/d/15WYmleETJwB2S80vuj8muWr6DNBIFmcmiB_UmHTosFg/edit>`__ (thanks to Ian from their support team).

Fortunately for you, the library comes with a few functions to help ya out with it. **first function in that list is creating an option symbol**

The library also has two bonus functions which allow you to create and parse option symbols using the format supported by TD Ameritrade. See below for more info on how to use them.

Building polygon formatted option symbols
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note that polygon has a rest endpoint in reference API to get all active contracts which you can filter based on many values.

You might have noticed (you didn't notice, did ya?) that polygon endpoints expect a prefix: ``O:`` before option symbols. For convenience, this library handles all of it internally.
what that means for you is that you can pass in option symbols **with or without the prefix O:** and both will be handled. In the below function, you can make the argument ``prefix_o=True``
to get the prefix in the output. By defaults it returns this format: ``AMD211205P00149000`` (example symbol)

here is how the function looks. just supply the details.

.. autofunction:: polygon.options.options.build_option_symbol
   :noindex:

Example use:

.. code-block:: python

  from polygon import build_option_symbol

  symbol = build_option_symbol('AMD', date(year=2021, month=12, day=5), 'c', 158)  # date is just a datetime.date object

  # another one!
  symbol = build_option_symbol('NVDA', '211205', 'call', 124.56)
  # you can use these variable as you like on polygon's endpoints

Building TDA formatted option symbols
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

don't use this formatting on polygon endpoints. only on td ameritrade. this is just a bonus function.

.. autofunction:: polygon.options.options.build_option_symbol_for_tda
   :noindex:

Example use:

.. code-block:: python

  from polygon import build_option_symbol_for_tda

  symbol = build_option_symbol_for_tda('AMD', date(year=2021, month=12, day=5), 'c', 158)  # date is just a datetime.date object

  # another one!
  symbol = build_option_symbol_for_tda('NVDA', '120522', 'call', 124.56)

Parsing Option Symbols
----------------------

So the above function was to build an option symbol from details. This function would help you do the opposite. That is, extracting information from an option symbol.

This function parses the symbol based on
`This spec <https://docs.google.com/document/d/15WYmleETJwB2S80vuj8muWr6DNBIFmcmiB_UmHTosFg/edit>`__. Note that
you can pass the value with or without the ``O:`` prefix. The lib would handle that like it does everywhere else.

parsing Polygon formatted option symbols
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Important** So it appears that some option symbols as returned by polygon endpoints happen to have a **correction number** within the symbol. The additional number is always
between the underlying symbol and expiry. **The lib handles that for you** and hence returns the corrected parsed symbol.

To elaborate: sometimes you'd see something like: ``MS1221015C00234000``. Notice the extra 1 right after symbol MS and before expiry 221015. This symbol should actually be
``MS221015C00234000`` without that 1 (which could be any number based on the info I have from support team).

If you ever need to get the corrected symbol without that additional number, use the lib to parse the symbol and the attribute ``option_symbol`` would contain the full option symbol
without the extra number and any prefixes.

By default the expiry date in the results would be a ``datetime.date`` object. Change it to ``string`` to get a
string in format ``YYYY-MM-DD``

You can choose to get your output in any one out of 3 different formats provided by the lib. To change the format, change the output_format arg in the function below.

The OptionSymbol object (default)
 by default it would return a :class:`polygon.options.options.OptionSymbol` object. The object would allow you to
 access values using attributes. For example: ``parsed_symbol.expiry``, ``parsed_symbol.underlying_symbol``,
 ``parsed_symbol.strike_price``, ``parsed_symbol.call_or_put`` and ``parse_symbol.option_symbol``

output as a list
 You can also choose to get your output as a ``list``. The list would just have all the parsed values as:
 ``[underlying_symbol, expiry, call_or_put, strike_price, option_symbol]``

output as a dict
 You can also choose to get your results as a ``dict``. The dict will have all the values as usual pairs.
 keys would be: ``'underlying_symbol', 'strike_price', 'expiry', 'call_or_put', 'option_symbol'``

While other values are self explanatory, the value ``option_symbol`` in parsed symbol is simply the full option symbol without any extra correction numbers or prefixes. For example
if you passed in ``MS221015C00234000``, option_symbol attribute will have the exact same value supplied. If you passed ``MS1221015C00234000`` or ``O:MS221015C00234000``, option_symbol would have
``MS221015C00234000`` removing those extra numbers and prefixes.

here is how the function looks.

.. autofunction:: polygon.options.options.parse_option_symbol
   :noindex:

Example use:

.. code-block:: python

  from polygon import (build_option_symbol, parse_option_symbol)

  parsed_details = parse_option_symbol('AMD211205C00156000')

  # another one!
  parsed_details = parse_option_symbol('AMD211205C00156000', output_format=list)

  # another one!
  parsed_details = parse_option_symbol('AMD211205C00156000', dict, expiry_format=str)

parsing TDA formatted option symbols
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

don't use this function on polygon endpoints. this is a bonus function meant for td ameritrade formatting.

The output_format and expiry_format have the same behavior as above. Only difference is in the formatting.

the dot format (symbol starting with a ``.``, usually found **when you export some file through ThinkOrSwim** or similar tda tool) is also supported

.. autofunction:: polygon.options.options.parse_option_symbol
   :noindex:

Example use:

.. code-block:: python

  from polygon import parse_option_symbol_from_tda

  parsed_details = parse_option_symbol_from_tda('GOOG_012122P620')

  # another one!
  parsed_details = parse_option_symbol_from_tda('TSLA_112020C1360', output_format=list)

  # another one!
  parsed_details = parse_option_symbol_from_tda('SPY_121622C335', dict, expiry_format=str)

Converting option symbol formats
--------------------------------

As a bonus function in the library, you can use the below functions to convert from polygon.io option symbol format to the
TD Ameritrade option symbol format and vice versa.

**this is useful for people who use TDA API for brokerage and polygon as their data source**.
**If you need a python package to work with TDA API, check out** `tda-api <https://github.com/alexgolec/tda-api>`__ by Alex Golec.

Converting from polygon to TDA format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**you might wanna use this when you want to place a trade on TDA for example using data from polygon.**

.. autofunction:: polygon.options.options.convert_from_polygon_to_tda_format
   :noindex:

Converting from TDA to polygon format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for when you grab a option symbol from tda, and want to get relevant data from polygon

.. autofunction:: polygon.options.options.convert_from_tda_to_polygon_format
   :noindex:

Detecting what format is a symbol in
------------------------------------

as the name suggests, when you want to programmatically determine what format is a symbol in. Might be useful for symbol lookups, for instance.

.. autofunction:: polygon.options.options.detect_symbol_format
   :noindex:

.. _option_endpoints_header:

**Endpoints**

To use any of the below method, simply call it on the client you created above. so if you named your client ``client``,
you'd call the methods as ``client.get_trades`` and so on. Async methods will need to be awaited, see :ref:`async_support_header`.

Get Trades
----------

This endpoint supports pagination. The library has support for pagination. See :ref:`pagination_header` for info and examples

.. automethod:: polygon.options.options.SyncOptionsClient.get_trades
   :noindex:

Get Last Trade
--------------

.. automethod:: polygon.options.options.SyncOptionsClient.get_last_trade
   :noindex:

Get Daily Open Close
--------------------

.. automethod:: polygon.options.options.SyncOptionsClient.get_daily_open_close
   :noindex:

Get Aggregate Bars
------------------

.. automethod:: polygon.options.options.SyncOptionsClient.get_aggregate_bars
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.options.options.SyncOptionsClient.get_previous_close
   :noindex:

Get Snapshot
------------

This endpoint supports pagination. The library has support for pagination. See :ref:`pagination_header` for info and examples

.. automethod:: polygon.options.options.SyncOptionsClient.get_snapshot
   :noindex:
