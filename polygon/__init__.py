# ========================================================= #
from . import enums
from .base_client import BaseClient, BaseAsyncClient
from .crypto import CryptoClient
from .forex import ForexClient
from .options import (
    OptionsClient,
    build_option_symbol,
    parse_option_symbol,
    OptionSymbol,
    build_polygon_option_symbol,
    parse_polygon_option_symbol,
    convert_option_symbol_formats,
    detect_option_symbol_format,
)
from .reference_apis import ReferenceClient
from .stocks import StocksClient
from .streaming import StreamClient, AsyncStreamClient

# ========================================================= #


__version__ = "1.2.6"

# ========================================================= #
