
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

Get Last Trade
--------------

.. automethod:: polygon.options.options.OptionsClient.get_last_trade
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.options.options.OptionsClient.get_previous_close
   :noindex:
