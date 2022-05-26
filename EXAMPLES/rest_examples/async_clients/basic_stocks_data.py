import asyncio
from datetime import date
import polygon


KEY = (
    "YOUR_API_KEY"  # recommend to keep your key in a separate file and import that here
)


async def main():
    client = polygon.StocksClient(KEY, True)

    # current price for a stock
    current_price = await client.get_current_price("AMD")

    # LAST QUOTE for a stock
    last_quote = await client.get_last_quote("AMD")

    print(last_quote)

    # LAST TRADE for a stock
    last_trade = await client.get_last_trade("NVDA")

    # You get the idea, right? ...RIGHT??

    # okay a few more

    # TRADES on a specific date for a stock
    trades = await client.get_trades("AMD", date(2021, 6, 28))

    # OCHLV for a specific day for a stock
    ochlv = await client.get_daily_open_close("AMD", "2021-06-21")

    # Day's Gainers OR Losers
    gainers = await client.get_gainers_and_losers()
    losers = await client.get_gainers_and_losers("losers")

    # Snapshot for a stock

    snapshot = await client.get_snapshot("NVDA")


if __name__ == "__main__":
    asyncio.run(main())
