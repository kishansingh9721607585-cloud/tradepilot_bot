import yfinance as yf

symbols = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANKNIFTY": "^NSEBANK",
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "BITCOIN": "BTC-USD"
}

def get_market_data():
    results = []
    for name, symbol in symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2d")
            latest = data['Close'].iloc[-1]
            previous = data['Close'].iloc[-2]
            change = ((latest - previous) / previous) * 100
            results.append({
                "name": name,
                "price": latest,
                "change": change
            })
        except Exception:
            pass
    return results
