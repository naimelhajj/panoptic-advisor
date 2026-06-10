import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime, timedelta

WATCHLIST_PATH = 'C:/development/stocks-finder/watchlist.json'
CATALYSTS_PATH = 'C:/development/stocks-finder/upcoming_catalysts.json'

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

def run_daily_advisor():
    print("\n" + "="*80)
    print(" [BOT] YOUR DAILY TRADING ADVISOR ($5k LOW-RISK BOT) ")
    print("="*80)
    print("Welcome! I'm here to tell you exactly what the algorithms are seeing today")
    print("in plain English. You can verify these setups on any charting software like")
    print("TradingView or Yahoo Finance by looking at the price and the 14-day RSI.\n")

    watchlist = load_json(WATCHLIST_PATH)
    catalysts = load_json(CATALYSTS_PATH)
    
    if not watchlist:
        print("Your watchlist is empty! Please add some stocks first.")
        return

    today_str = datetime.now().strftime('%Y-%m-%d')
    print(f"Today's Date: {today_str}\n")

    for ticker, info in watchlist.items():
        try:
            # Download recent data
            stock = yf.Ticker(ticker)
            df = stock.history(period="1y")
            
            if df.empty or len(df) < 200:
                print(f"[{ticker}] Not enough data to analyze right now.")
                continue
                
            df['RSI'] = calculate_rsi(df['Close'])
            df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
            
            latest = df.iloc[-1]
            close_price = latest['Close']
            rsi = latest['RSI']
            ema_200 = latest['EMA_200']
            
            is_bear_market = close_price < ema_200
            is_etf = info.get("Type", "Stock").upper() == "ETF"
            name = info.get("Name", ticker)
            
            print(f"--- {ticker} ({name}) ---")
            print(f"Current Price: ${close_price:.2f} | RSI: {rsi:.1f} | 200-Day Average: ${ema_200:.2f}")
            
            # Advice logic
            advice_given = False
            
            # 1. Systemic Crash Warning
            if is_etf and rsi < 20.0:
                print("[!!!] ACTION: EXTREME PANIC DETECTED (WAIT)")
                print("Explanation: The RSI is under 20. This means the market is in a severe panic and selling off violently.")
                print("If you hold shares, do NOT sell them now. You are at the absolute bottom. Hold for 30 days until the central banks step in to save the market.")
                advice_given = True
                
            # 2. Oversold ETF Bounce
            elif is_etf and rsi < 35.0 and not is_bear_market:
                print("[BUY] ACTION: BUY SHARES (Use 15% of your cash)")
                print("Explanation: The price is above its 200-day average, meaning the overall, long-term trend is UP.")
                print(f"However, {ticker} has recently dropped (RSI under 35), meaning short-term sellers got exhausted.")
                print("This is a classic 'buy the dip' setup. Buy shares with 15% of your cash, and plan to sell when RSI hits 70.")
                advice_given = True
                
            # 3. Bear Market ETF Put Hedge
            elif is_etf and is_bear_market and rsi > 70.0:
                print("[PUT] ACTION: BUY PUT OPTIONS (Use 2% of your cash)")
                print("Explanation: The price is below its 200-day average, meaning we are in a BEAR MARKET (long-term trend is DOWN).")
                print(f"Right now, {ticker} just had a fast spike upward and is 'overbought' (RSI over 70).")
                print("In bear markets, these upward spikes almost always fail. Buy Put Options (which profit when prices fall) with a tiny safe amount of cash (2%).")
                advice_given = True
                
            # 4. Stock Catalyst
            if not is_etf and ticker in catalysts:
                cat = catalysts[ticker]
                days = cat.get('days_until', 0)
                if 0 <= days <= 14:
                    print(f"[CALL] ACTION: BUY CALL OPTIONS (Use 3% of your cash)")
                    print(f"Explanation: {ticker} has a massive event coming up in {days} days: {cat.get('desc', 'Earnings')}.")
                    print("Instead of risking lots of cash on the stock, we buy Call Options with just 3% of our cash.")
                    print("If the stock explodes upward, the options will multiply in value. If it crashes, we only lose that tiny 3%.")
                    advice_given = True
                    
            if not advice_given:
                print("[HOLD] ACTION: DO NOTHING (HOLD / WAIT)")
                print("Explanation: The stock is floating in the middle right now. It's not overly cheap, and it's not dangerously expensive. ")
                print("The best traders wait patiently like a sniper. Check back tomorrow.")
                
            print("\n")
            
        except Exception as e:
            print(f"[{ticker}] Error checking data: {e}")

if __name__ == "__main__":
    run_daily_advisor()
