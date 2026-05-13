import yfinance as yf
import mplfinance as mpf

def generate_chart(stock):
    ticker = yf.Ticker(stock)
    df = ticker.history(period='3mo')
    path = f"charts/{stock}.png"
    mpf.plot(
        df,
        type='candle',
        mav=(20, 50),
        volume=True,
        savefig=path
    )
    return path
