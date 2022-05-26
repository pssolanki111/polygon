import polygon
from datetime import date

KEY = (
    "YOUR_API_KEY"  # recommend to keep your key in a separate file and import that here
)

client = polygon.StocksClient(KEY)

# current price for a stock
current_price = client.get_current_price("AMD")

# LAST QUOTE for a stock
last_quote = client.get_last_quote("AMD")

print(last_quote)

# LAST TRADE for a stock
last_trade = client.get_last_trade("NVDA")

# You get the idea, right? ...RIGHT??

# okay a few more

# TRADES on a specific date for a stock
trades = client.get_trades("AMD", date(2021, 6, 28))

# OCHLV for a specific day for a stock
ochlv = client.get_daily_open_close("AMD", "2021-06-21")

# Day's Gainers OR Losers
gainers = client.get_gainers_and_losers()
losers = client.get_gainers_and_losers("losers")

# Snapshot for a stock

snapshot = client.get_snapshot("NVDA")
