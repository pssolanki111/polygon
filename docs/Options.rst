
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

**NOTE** if you don't want to use the option symbol helper functions, then you can just go to the desired endpoint documentation from the list to left

.. _option_symbols_header:

Working with Option Symbols
---------------------------

So when you're working with options (rest/websockets), you'll certainly need the option symbols which contain the information about their underlying symbol, expiry, call_or_put and the
strike price in a certain format. There are many formats to represent them and every data source/brokerage uses a 
different format to represent them.

for example Polygon.io tends to use `This Format <https://www.optionstaxguy.com/option-symbols-osi>`__ . For those who want to understand how this formatting works,
`Here is a guide <https://docs.google.com/document/d/15WYmleETJwB2S80vuj8muWr6DNBIFmcmiB_UmHTosFg/edit>`__ (thanks to Ian from polygon support team).

The library is equipped with a few functions to make it easier for you to **build, parse, convert, and detect 
format** of option symbols without worrying about how the structure works.

The library supports the following symbol formats at the moment

===================  ====================
  Full Name            Shorthand String
===================  ====================
Polygon.io           polygon
Tradier              tradier
Trade Station        trade_station
Interactive Brokers  ibkr
TD Ameritrade        tda
Think Or Swim        tos
===================  ====================

This section on option symbols is divided into these sections below. 

1. **Creating** Option symbols from info as underlying, expiry, strike price, option type
#. **Parsing** Option symbols to **extract** info as underlying, expiry, strike price, option type
#. **Converting** an option symbol from one format to another. Works between all supported formats.
#. **Detecting** format of an option symbol. Basic detection based on some simple rules.

Creating Option Symbols
~~~~~~~~~~~~~~~~~~~~~~~

The function in this sub-section help you to build option symbols from info as underlying symbol, expiry, strike 
price & option type (call/put)

The function to use is ``polygon.build_option_symbol``

Since the default format is polygon.io you don't need to worry about passing in the format explicitly.

-  Polygon has a rest endpoint in reference client to get all active contracts which you can filter based on 
   many values such as underlying symbol and expiry dates.

-  In polygon format, If you wonder whether you need to worry about the ``O:`` prefix which some/all option endpoints 
   expect, then to your ease, the library handles that for you (So you can pass a symbol without prefix to let's say
   Option Snapshot function and the prefix will be added internally). If you want to be explicit, just pass 
   ``prefix_o=True`` when building symbol.

-  Note that both tradier and polygon happen to use the exact same symbol format and hence can be used interchangeably.

Example Code & Output for polygon/tradier format

.. code-block:: python

  import polygon
  
  symbol1 = polygon.build_option_symbol('AMD', datetime.date(2022, 6, 28), 'call', 546.56)
  symbol2 = polygon.build_option_symbol('TSLA', '220628', 'c', 546, _format='polygon')
  symbol3 = polygon.build_option_symbol('A', '220628', 'put', 66.01, prefix_o=True)
  
  # Outputs
  # symbol1 -> AMD220628C00546560
  # symbol2 -> TSLA220628C00546000
  # symbol3 -> O:A220628P00066010
  
  
The same function can be used to create option symbols for any of the supported formats, just pass in the format you 
need, either as a shorthand string from the table above, or use an enum from :class:`polygon.enums.OptionSymbolFormat`

-  Using enums (like ``OptionSymbolFormat.POLYGON`` in example below) is a good way to ensure you only pass in 
   correct shorthand strings. Your IDE auto completion would make your life much easier when working with enums.

Example code & outputs for multiple formats

.. code-block:: python

  from polygon import build_option_symbol  # you can import the way you like, just showing the alternates
  from polygon.enums import OptionSymbolFormat  # optional, you can pass in shorthand strings too
  
  symbol1 = polygon.build_option_symbol('AMD', datetime.date(2022, 6, 28), 'call', 546.56, format_='tda')
  symbol2 = polygon.build_option_symbol('NVDA', '220628', 'c', 546, format_='tos')
  symbol3 = polygon.build_option_symbol('TSLA', datetime.date(2022, 6, 28), 'put', 46.01, format_='tradier')
  symbol4 = polygon.build_option_symbol('A', datetime.date(2022, 6, 28), 'p', 46.1, format_='ibkr')
  symbol5 = polygon.build_option_symbol('AB', datetime.date(2022, 6, 28), 'p', 46.01, format_='trade_station')
  symbol6 = polygon.build_option_symbol('PTON', '220628', 'p', 46, format_=OptionSymbolFormat.POLYGON)  # using enum
  
  # outputs
  # symbol1 -> AMD_062822C546.56
  # symbol2 -> .NVDA062822C546
  # symbol3 -> TSLA220628P00046010
  # symbol4 -> A 220628P00046100
  # symbol5 -> AB 220628P46.01
  # symbol5 -> PTON220628P00046000

For those who want more control, here is how the function signature and arguments look

.. autofunction:: polygon.options.options.build_option_symbol
   :noindex:

Parsing Option Symbols
~~~~~~~~~~~~~~~~~~~~~~

Converting Option Symbol Formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detecting Option Symbol Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parsing Option Symbols6
-----------------------

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

Example use:

.. code-block:: python

  from polygon import parse_option_symbol_from_tda

  parsed_details = parse_option_symbol_from_tda('GOOG_012122P620')

  # another one!
  parsed_details = parse_option_symbol_from_tda('.AMD220128P81', output_format=list)  # DOT format from ThinkOrSwim

  # another one!
  parsed_details = parse_option_symbol_from_tda('SPY_121622C335', dict, expiry_format=str)

Converting option symbol formats5
----------------------------------

As a bonus function in the library, you can use the below functions to convert from polygon.io option symbol format to the
TD Ameritrade option symbol format and vice versa.

**this is useful for people who use TDA API for brokerage and polygon as their data source**.
**If you need a python package to work with TDA API, check out** `tda-api <https://github.com/alexgolec/tda-api>`__

.. _option_endpoints_header:

**Endpoints**

To use any of the below method, simply call it on the client you created above. so if you named your client ``client``,
you'd call the methods as ``client.get_trades`` and so on. Async methods will need to be awaited, see :ref:`async_support_header`.

Get Trades
----------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.options.options.SyncOptionsClient.get_trades
   :noindex:

Get Quotes
----------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.options.options.SyncOptionsClient.get_quotes
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

The library added a better aggregate function if you're looking to get data for large time frames at minute/hour granularity.

(for example 15 years historical data , 1 minute candles)

See :ref:`better_aggs_header` for complete details on how to use it well and control how it behaves.

.. automethod:: polygon.options.options.SyncOptionsClient.get_aggregate_bars
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.options.options.SyncOptionsClient.get_previous_close
   :noindex:

Get Snapshot
------------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.options.options.SyncOptionsClient.get_snapshot
   :noindex:
