import yfinance as yf
import json
import os
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

WATCHLIST_PATH = 'C:/development/stocks-finder/watchlist.json'
CATALYSTS_PATH = 'C:/development/stocks-finder/upcoming_catalysts.json'
MAX_WORKERS = 20

def check_earnings(ticker):
    try:
        stock = yf.Ticker(ticker)
        cal = stock.calendar
        
        if not cal:
            return None
            
        # yfinance stock.calendar format is typically a dict or df
        # Let's inspect potential formats
        earnings_date = None
        
        if isinstance(cal, dict):
            dates = cal.get('Earnings Date', [])
            if dates and len(dates) > 0:
                earnings_date = dates[0]
        elif isinstance(cal, list) and len(cal) > 0:
            earnings_date = cal[0]
        elif hasattr(cal, 'get'):
            # Fallback
            dates = cal.get('Earnings Date', [])
            if hasattr(dates, 'iloc'):
                earnings_date = dates.iloc[0] if len(dates) > 0 else None
            elif isinstance(dates, list) and len(dates) > 0:
                earnings_date = dates[0]
                
        if earnings_date:
            # Handle date conversion
            if hasattr(earnings_date, 'to_pydatetime'):
                dt = earnings_date.to_pydatetime()
            elif isinstance(earnings_date, (datetime, time.struct_time)):
                dt = earnings_date
            else:
                # String or date object
                dt_str = str(earnings_date).split(' ')[0]
                dt = datetime.strptime(dt_str, '%Y-%m-%d')
                
            return {
                "ticker": ticker,
                "earnings_date": dt.strftime('%Y-%m-%d'),
                "days_until": (dt.date() - datetime.today().date()).days
            }
    except Exception:
        # Fail silently
        return None

def scan_earnings():
    print("\n" + "="*80)
    print("   AUTONOMOUS FPBV EARNINGS CATALYST SCANNER (100% Automated Calendar)")
    print("="*80)
    
    if not os.path.exists(WATCHLIST_PATH):
        print(f"Error: watchlist.json not found at {WATCHLIST_PATH}.")
        return
        
    with open(WATCHLIST_PATH, 'r') as f:
        watchlist = json.load(f)
        
    stocks = [t for t, details in watchlist.items() if details.get("Type") == "Stock"]
    print(f"Scanning upcoming earnings calendars for {len(stocks)} stocks...")
    
    upcoming_catalysts = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_earnings, t): t for t in stocks}
        
        for future in as_completed(futures):
            res = future.result()
            if res:
                ticker = res["ticker"]
                days = res["days_until"]
                
                # Report if it's within the next 10 days (focusing on upcoming catalysts)
                if 0 <= days <= 10:
                    upcoming_catalysts[ticker] = {
                        "direction": "CALL",  # Default direction for long volatility plays
                        "earnings_date": res["earnings_date"],
                        "days_until": days,
                        "desc": f"Automated Catalyst: {ticker} upcoming Q earnings in {days} days."
                    }
                    print(f"  [ALERT] {ticker:<6} | Earnings on {res['earnings_date']} ({days} days away)")
                    
    with open(CATALYSTS_PATH, 'w') as f:
        json.dump(upcoming_catalysts, f, indent=4)
        
    print(f"Earnings scan complete. Saved {len(upcoming_catalysts)} upcoming catalysts to {CATALYSTS_PATH}")

if __name__ == '__main__':
    scan_earnings()
