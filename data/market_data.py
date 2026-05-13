import yfinance as yf


symbols = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANK NIFTY": "^NSEBANK",
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "BITCOIN": "BTC-USD"
}


def get_market_data():

    results = []

    for name, symbol in symbols.items():

        try:

            ticker = yf.Ticker(symbol)

            data = ticker.history(
                period="5d",
                interval="1d",
                auto_adjust=True
            )

            if data.empty or len(data) < 2:
                continue

            latest = float(data['Close'].dropna().iloc[-1])
            previous = float(data['Close'].dropna().iloc[-2])

            change = ((latest - previous) / previous) * 100

            results.append({
                "name": name,
                "price": latest,
                "change": change
            })

        except Exception as e:

            print(f"Error fetching {name}: {e}")

    return results