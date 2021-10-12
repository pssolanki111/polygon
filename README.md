# `polygon`: A Polygon.io API Wrapper

## what is `polygon`
`polygon` is a Complete Python Wrapper for [Polygon.io APIs](https://polygon.io/). It offers 
simple and elegant programmatic access over each endpoint. Functionalities include but not limited to:

-  Stocks and Options data
-  Forex and Crypto data
-  Websocket streaming (both callback and async based)
-  Market Info, News, Holidays, Schedules
-  Async support for REST endpoints

and more...

## How do I use `polygon`

The complete description of everything you need to know is available in the [Documentation](https://polygon.readthedocs.io/)

Before you do anything, you'll need to have a polygon account and get your API key. 
Visit [your dashboard](https://polygon.io/dashboard/api-keys) to get your API key.

Next, you'd need to install `polygon`

```shell
pip install polygon
```

**and You're good to Go!** For a quick show, here is how you can use the lib to fetch the current market price
for a ticker symbol

```python
import polygon

api_key = 'YOUR_KEY'

stocks_client = polygon.StocksClient(api_key)

current_price = stocks_client.get_current_price('AMD')

print(current_price)
```

See the documentation to start using the library in its full capabilities.

## what if I need help?

See [Getting Help](https://polygon.readthedocs.io/en/latest/getting_help.html)

## anything else?

Bug reports, suggestions and pull requests are always welcome. 

See [Contributing](https://polygon.readthedocs.io/en/latest/contrib_and_license.html)
if you wish to contribute.

Read [This](https://polygon.readthedocs.io/en/latest/bugs_discussions_wikis_faqs.html) before raising a bug.

`polygon` is released under the [MIT License](https://github.com/pssolanki111/polygon/blob/main/LICENSE)