import yfinance as yf
import json

def check_short_interest(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        short_percent = info.get('shortPercentOfFloat', None)
        short_ratio = info.get('shortRatio', None)
        print(f"[{ticker_symbol}] Short Percent of Float: {short_percent}")
        print(f"[{ticker_symbol}] Short Ratio (Days to Cover): {short_ratio}")
    except Exception as e:
        print(f"Error for {ticker_symbol}: {e}")

if __name__ == "__main__":
    check_short_interest('CASY')
    check_short_interest('GME')
    check_short_interest('AAPL')
