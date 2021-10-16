
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


Creating Option Symbols
-----------------------

So when you're working with options (rest/websockets), you'll certainly need the option symbols which contain the information about their underlying symbol, expiry, call_or_put and the
strike price in a certain format. Many organizations tend to use different formats to represent these.

Polygon.io tends to use `This Format <https://www.optionstaxguy.com/option-symbols-osi>`__ . For those who want to understand how this formatting works,
`Here is a guide <https://docs.google.com/document/d/15WYmleETJwB2S80vuj8muWr6DNBIFmcmiB_UmHTosFg/edit>`__ (thanks to Ian from their support team).

Fortunately for you, the library comes with a few functions to help ya out with it. **first function in that list is creating an option symbol**

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

Parsing Option Symbols
----------------------

So the above function was to build an option symbol from details. This function would help you do the opposite. That is, extracting information from an option symbol.

This function parses the symbol based on
`This spec <https://docs.google.com/document/d/15WYmleETJwB2S80vuj8muWr6DNBIFmcmiB_UmHTosFg/edit>`__. Note that
you can pass the value with or without the ``O:`` prefix. The lib would handle that like it does everywhere else.

By default the expiry date in the results would be a ``datetime.date`` object. Change it to ``string`` to get a
string in format ``YYYY-MM-DD``

You can choose to get your output in any one out of 3 different formats provided by the lib. To change the format, change the output_format arg in the function below.

The OptionSymbol object (default)
 by default it would return a :class:`polygon.options.options.OptionSymbol` object. The object would allow you to
 access values using attributes. For example: ``parsed_symbol.expiry``, ``parsed_symbol.underlying_symbol``,
 ``parsed_symbol.strike_price`` and ``parsed_symbol.call_or_put`` where parsed_symbol is simply the value returned by this function that you assign to a variable.

output as a list
 You can also choose to get your output as a ``list``. The list would just have all the parsed values as:
 ``[underlying_symbol, expiry, call_or_put, strike_price]``

output as a dict
 You can also choose to get your results as a ``dict``. The dict will have all the values as usual pairs.
 keys would be: ``'underlying_symbol', 'strike_price', 'expiry', 'call_or_put'``

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
  parsed_detailed = parse_option_symbol('AMD211205C00156000', dict, expiry_format=str)

Get Last Trade
--------------

.. automethod:: polygon.options.options.OptionsClient.get_last_trade
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.options.options.OptionsClient.get_previous_close
   :noindex:
