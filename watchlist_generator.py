import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
import time
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

WATCHLIST_PATH = 'C:/development/stocks-finder/watchlist.json'
MAX_WORKERS = 20  # Limit to avoid rate limiting from Yahoo Finance

CORE_TICKERS = {
    "SOXL": {
        "Name": "Direxion Daily Semiconductor Bull 3X Shares",
        "Sector": "Semiconductors",
        "Type": "ETF",
        "Thesis": "Leveraged instrument to capture macro chip cycles and sector pullbacks.",
        "DateAdded": "2026-06-01"
    },
    "TQQQ": {
        "Name": "ProShares UltraPro QQQ",
        "Sector": "Technology",
        "Type": "ETF",
        "Thesis": "Leveraged instrument to capture broad Nasdaq structural bull runs.",
        "DateAdded": "2026-06-01"
    },
    "NVDA": {
        "Name": "NVIDIA Corporation",
        "Sector": "Technology",
        "Type": "Stock",
        "Thesis": "GPU bottleneck monopoly.",
        "DateAdded": "2026-06-01"
    },
    "AVGO": {
        "Name": "Broadcom Inc.",
        "Sector": "Technology",
        "Type": "Stock",
        "Thesis": "Custom ASIC/networking bottleneck.",
        "DateAdded": "2026-06-01"
    },
    "ENPH": {
        "Name": "Enphase Energy, Inc.",
        "Sector": "Clean Energy",
        "Type": "Stock",
        "Thesis": "Solar microinverter bottleneck.",
        "DateAdded": "2026-06-01"
    },
    "RYCEY": {
        "Name": "Rolls-Royce Holdings plc",
        "Sector": "Aerospace & Defense",
        "Type": "Stock",
        "Thesis": "Wide-body aircraft turbine aftermarket bottleneck.",
        "DateAdded": "2026-06-01"
    },
    "GME": {
        "Name": "GameStop Corp.",
        "Sector": "Consumer Cyclical",
        "Type": "Stock",
        "Thesis": "High-retail-attention volatility catalyst play.",
        "DateAdded": "2026-06-01"
    },
    "MVIS": {
        "Name": "MicroVision, Inc.",
        "Sector": "Technology",
        "Type": "Stock",
        "Thesis": "Speculative high-beta Lidar IP play.",
        "DateAdded": "2026-06-01"
    },
    "VRT": {
        "Name": "Vertiv Holdings Co",
        "Sector": "Industrials",
        "Type": "Stock",
        "Thesis": "AI liquid cooling hardware.",
        "DateAdded": "2026-06-01"
    },
    "HUBB": {
        "Name": "Hubbell Incorporated",
        "Sector": "Industrials",
        "Type": "Stock",
        "Thesis": "Transmission and distribution grid components.",
        "DateAdded": "2026-06-01"
    },
    "PH": {
        "Name": "Parker-Hannifin Corporation",
        "Sector": "Industrials",
        "Type": "Stock",
        "Thesis": "Motion and control technologies.",
        "DateAdded": "2026-06-01"
    },
    "HWM": {
        "Name": "Howmet Aerospace Inc.",
        "Sector": "Aerospace & Defense",
        "Type": "Stock",
        "Thesis": "High-temperature titanium castings for jet engines.",
        "DateAdded": "2026-06-01"
    }
}

def scrape_sp500_tickers():
    print("Scraping S&P 500 ticker list from Wikipedia...")
    try:
        req = urllib.request.Request(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read()
        tables = pd.read_html(html)
        df = tables[0]
        tickers = df['Symbol'].tolist()
        # Replace dot with dash for Yahoo Finance compatibility (e.g. BRK.B -> BRK-B)
        tickers = [t.replace('.', '-') for t in tickers]
        print(f"Scraped {len(tickers)} tickers successfully.")
        return tickers
    except Exception as e:
        err_msg = str(e)
        if len(err_msg) > 200: err_msg = err_msg[:200] + "... [HTML TRUNCATED]"
        print(f"Error scraping S&P 500 tickers: {err_msg}")
        # Fallback to a small list of highly liquid tech stocks
        return ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "AVGO", "VRT", "ENPH", "RYCEY"]

def audit_ticker(ticker):
    """Audits a single ticker's fundamentals. Returns details if it passes solvency checks, else None."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or 'longName' not in info:
            return None
            
        # 1. Gross Margin Gate (>= 20%)
        gross_margin = info.get('grossMargins', None)
        if gross_margin is None or np.isnan(gross_margin) or gross_margin < 0.20:
            return None
            
        # 2. Free Cash Flow Gate (> 0)
        fcf = info.get('freeCashflow', None)
        if fcf is None or np.isnan(fcf) or fcf <= 0:
            return None
            
        # 3. Leverage Gate (Net Debt/EBITDA < 4.0x)
        total_debt = info.get('totalDebt', 0)
        total_cash = info.get('totalCash', 0)
        net_debt = (total_debt - total_cash) if total_debt is not None and total_cash is not None else 0
        ebitda = info.get('ebitda', None)
        
        if ebitda is not None and not np.isnan(ebitda) and ebitda > 0:
            net_debt_ebitda = net_debt / ebitda
            if net_debt_ebitda > 4.0:
                return None
        elif net_debt > 0:
            # Positive net debt with negative/zero EBITDA is high risk
            return None
            
        # 4. Debt to Equity Gate (< 2.0)
        debt_to_equity = info.get('debtToEquity', None)
        if debt_to_equity is not None and not np.isnan(debt_to_equity):
            if (debt_to_equity / 100.0) > 2.0:
                return None
                
        # All checks passed! Return structured metadata
        return {
            "Name": info.get('longName', ticker),
            "Sector": info.get('sector', 'N/A'),
            "Type": "Stock",
            "Thesis": f"Dynamic secular leader in {info.get('sector', 'N/A')} passing all automated solvency gates.",
            "DateAdded": time.strftime("%Y-%m-%d")
        }
    except Exception:
        # Silently fail for individual tickers to keep output clean during parallel runs
        return None

def generate_watchlist():
    print("\n" + "="*80)
    print("   AUTONOMOUS FPBV WATCHLIST GENERATOR (100% Automated Discovery & Audit)")
    print("="*80)
    
    sp500_tickers = scrape_sp500_tickers()
    
    # We load existing watchlist to preserve CORE_TICKERS or other manually locked assets
    existing_watchlist = {}
    if os.path.exists(WATCHLIST_PATH):
        try:
            with open(WATCHLIST_PATH, 'r') as f:
                existing_watchlist = json.load(f)
        except Exception:
            pass
            
    new_watchlist = {}
    
    # Enforce CORE_TICKERS (leveraged ETFs) are always present
    for ticker, details in CORE_TICKERS.items():
        new_watchlist[ticker] = details
        
    print(f"Auditing {len(sp500_tickers)} stocks in parallel (Max Workers: {MAX_WORKERS})...")
    
    passed_count = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(audit_ticker, ticker): ticker for ticker in sp500_tickers}
        
        for future in as_completed(futures):
            ticker = futures[future]
            result = future.result()
            if result:
                new_watchlist[ticker] = result
                passed_count += 1
                print(f"  [PASS] {ticker:<6} | {result['Name'][:35]:<35} | Margin: {result['Sector']}", end="\r")
                sys.stdout.flush()
                
    print(f"\nAudit complete. {passed_count} S&P 500 stocks passed all solvency checks.")
    
    # Save the new watchlist
    try:
        with open(WATCHLIST_PATH, 'w') as f:
            json.dump(new_watchlist, f, indent=4)
        print(f"Successfully saved {len(new_watchlist)} total tickers to {WATCHLIST_PATH}")
    except Exception as e:
        print(f"Error saving watchlist: {e}")

if __name__ == '__main__':
    generate_watchlist()
