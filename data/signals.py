import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD

def generate_signal(stock):
    try:
        ticker = yf.Ticker(stock)
        df = ticker.history(period="6mo")

        if df.empty:
            return {
                "error": "No market data found"
            }

        # Drop rows where Close is missing before any calculations
        df = df.dropna(subset=["Close"])

        if df.empty:
            return {
                "error": "No valid close prices found"
            }

        close_prices = df['Close']
        close_prices = close_prices.astype(float).dropna()

        if close_prices.empty:
            return {
                "error": "No valid close prices found"
            }

        rsi = RSIIndicator(close_prices).rsi()
        latest_rsi = rsi.iloc[-1]
        macd = MACD(close_prices)
        macd_line = macd.macd().iloc[-1]
        signal_line = macd.macd_signal().iloc[-1]
        latest_price = float(close_prices.iloc[-1])
        signal = "HOLD"
        reason = "Neutral market"

        if latest_rsi < 30 and macd_line > signal_line:
            signal = "BUY"
            reason = "Oversold + bullish MACD"
        elif latest_rsi > 70 and macd_line < signal_line:
            signal = "SELL"
            reason = "Overbought + bearish MACD"

        return {
            "stock": stock,
            "price": latest_price,
            "rsi": latest_rsi,
            "signal": signal,
            "reason": reason
        }
    except Exception as e:
        return {
            "error": str(e)
        }