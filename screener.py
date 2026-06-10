import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
import sys
import argparse
import time

WATCHLIST_PATH = 'C:/development/stocks-finder/watchlist.json'
RESULTS_PATH = 'C:/development/stocks-finder/screener_results.json'

def load_watchlist():
    if not os.path.exists(WATCHLIST_PATH):
        # Create default watchlist if it doesn't exist
        print(f"Watchlist database not found. Creating default at {WATCHLIST_PATH}...")
        default_watchlist = {
            "SOXL": {"Name": "Direxion Semiconductor Bull 3X", "Sector": "Semiconductors", "Type": "ETF", "Thesis": "Leveraged chip cycles.", "DateAdded": "2026-06-01"},
            "TQQQ": {"Name": "ProShares UltraPro QQQ 3X", "Sector": "Technology", "Type": "ETF", "Thesis": "Leveraged Nasdaq growth.", "DateAdded": "2026-06-01"},
            "NVDA": {"Name": "NVIDIA Corporation", "Sector": "Technology", "Type": "Stock", "Thesis": "GPU bottleneck monopoly.", "DateAdded": "2026-06-01"},
            "AVGO": {"Name": "Broadcom Inc.", "Sector": "Technology", "Type": "Stock", "Thesis": "Custom ASIC/networking bottleneck.", "DateAdded": "2026-06-01"},
            "ENPH": {"Name": "Enphase Energy", "Sector": "Clean Energy", "Type": "Stock", "Thesis": "Microinverter bottleneck.", "DateAdded": "2026-06-01"},
            "VRT": {"Name": "Vertiv Holdings Co", "Sector": "Industrials", "Type": "Stock", "Thesis": "AI liquid cooling hardware.", "DateAdded": "2026-06-01"}
        }
        with open(WATCHLIST_PATH, 'w') as f:
            json.dump(default_watchlist, f, indent=4)
        return default_watchlist
    
    with open(WATCHLIST_PATH, 'r') as f:
        return json.load(f)

def save_watchlist(watchlist):
    with open(WATCHLIST_PATH, 'w') as f:
        json.dump(watchlist, f, indent=4)

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

def add_ticker(ticker, thesis, sector="N/A", is_etf=False):
    ticker = ticker.upper()
    watchlist = load_watchlist()
    if ticker in watchlist:
        print(f"Ticker {ticker} is already in the watchlist.")
        return
        
    print(f"Fetching details for {ticker} from Yahoo Finance...")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        name = info.get('longName', ticker)
        sec = info.get('sector', sector)
        typ = "ETF" if is_etf or info.get('quoteType') == 'ETF' else "Stock"
        
        watchlist[ticker] = {
            "Name": name,
            "Sector": sec,
            "Type": typ,
            "Thesis": thesis,
            "DateAdded": time.strftime("%Y-%m-%d")
        }
        save_watchlist(watchlist)
        print(f"Successfully added {ticker} ({name}) to watchlist database.")
    except Exception as e:
        print(f"Failed to fetch data to add ticker: {str(e)}")
        # Add fallback record
        watchlist[ticker] = {
            "Name": ticker,
            "Sector": sector,
            "Type": "ETF" if is_etf else "Stock",
            "Thesis": thesis,
            "DateAdded": time.strftime("%Y-%m-%d")
        }
        save_watchlist(watchlist)
        print(f"Added {ticker} to watchlist with fallback data.")

def remove_ticker(ticker):
    ticker = ticker.upper()
    watchlist = load_watchlist()
    if ticker not in watchlist:
        print(f"Ticker {ticker} is not in the watchlist.")
        return
    
    del watchlist[ticker]
    save_watchlist(watchlist)
    print(f"Successfully removed {ticker} from watchlist database.")

def scan_watchlist():
    watchlist = load_watchlist()
    print("=" * 115)
    print("    DYNAMIC FPBV SCREENER: RUNNING HEDGE FUND MANAGER BRAIN SETUP")
    print("=" * 115)
    print(f"Loaded {len(watchlist)} assets from database.")
    
    results = {}
    gems = []
    
    for idx, (ticker, details) in enumerate(watchlist.items(), 1):
        print(f"[{idx}/{len(watchlist)}] Scanning {ticker}...", end="\r")
        sys.stdout.flush()
        
        try:
            # 1. Gather technical prices
            stock = yf.Ticker(ticker)
            df = stock.history(period="100d")
            
            if df.empty or len(df) < 20:
                print(f"\n  [Error] Insufficient price data for {ticker}")
                continue
                
            df['RSI'] = calculate_rsi(df['Close'], period=14)
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            
            latest = df.iloc[-1]
            close_price = latest['Close']
            rsi = latest['RSI']
            ema_20 = latest['EMA_20']
            ema_50 = latest['EMA_50']
            
            # Technical signals
            signal_status = "NEUTRAL"
            signal_details = "Hold / Monitor."
            
            if rsi < 35.0:
                signal_status = "BUY_SIGNAL"
                signal_details = f"Oversold Daily RSI ({rsi:.1f} < 35). Potential accumulation."
            elif rsi > 70.0:
                signal_status = "OVERBOUGHT_ALERT"
                signal_details = f"Overbought Daily RSI ({rsi:.1f} > 70). Enforce trailing exits if close below 20-day EMA."
                
            if close_price < ema_20 and rsi > 50.0:
                signal_details += f" Warning: Crossed below 20-day EMA (${ema_20:.2f})."
                
            # 2. Solvency Checks (Only for Stocks, exempt ETFs)
            warnings = []
            gross_margin = np.nan
            fcf = np.nan
            net_debt_ebitda = np.nan
            debt_to_equity = np.nan
            
            is_etf = details.get('Type') == 'ETF'
            
            if not is_etf:
                info = stock.info
                # Margins check
                gross_margin = info.get('grossMargins', np.nan)
                if gross_margin is not None and not np.isnan(gross_margin):
                    gross_margin *= 100
                    if gross_margin < 20.0:
                        warnings.append(f"LOW_MARGIN ({gross_margin:.1f}%)")
                else:
                    warnings.append("NO_MARGIN_DATA")
                    
                # Free Cash Flow check
                fcf = info.get('freeCashflow', np.nan)
                if fcf is not None and not np.isnan(fcf):
                    if fcf < 0:
                        warnings.append(f"NEGATIVE_FCF (-${abs(fcf)/1e6:.1f}M)")
                else:
                    warnings.append("NO_FCF_DATA")
                    
                # Leverage Net Debt/EBITDA & Debt/Equity check
                total_debt = info.get('totalDebt', 0.0)
                total_cash = info.get('totalCash', 0.0)
                net_debt = total_debt - total_cash if total_debt is not None and total_cash is not None else 0.0
                ebitda = info.get('ebitda', np.nan)
                
                if ebitda is not None and ebitda > 0:
                    net_debt_ebitda = net_debt / ebitda
                    if net_debt_ebitda > 4.0:
                        warnings.append(f"HIGH_LEVERAGE ({net_debt_ebitda:.2f}x)")
                elif net_debt > 0:
                    net_debt_ebitda = np.nan
                    warnings.append("HIGH_LEVERAGE (Neg. EBITDA / Pos. Debt)")
                else:
                    net_debt_ebitda = 0.0
                    
                debt_to_equity = info.get('debtToEquity', np.nan)
                if debt_to_equity is not None and not np.isnan(debt_to_equity):
                    debt_to_equity /= 100.0
                    if debt_to_equity > 2.0:
                        warnings.append(f"HIGH_DEBT ({debt_to_equity:.2f})")
            
            solvency_status = "PASS" if len(warnings) == 0 else f"WARN ({', '.join(warnings)})"
            
            results[ticker] = {
                "Ticker": ticker,
                "Name": details.get('Name', ticker),
                "Sector": details.get('Sector', 'N/A'),
                "Type": details.get('Type', 'Stock'),
                "Thesis": details.get('Thesis', ''),
                "Close": float(close_price),
                "RSI_14": float(rsi),
                "EMA_20": float(ema_20),
                "EMA_50": float(ema_50),
                "Signal_Status": signal_status,
                "Signal_Details": signal_details,
                "Solvency_Status": solvency_status,
                "Warnings": warnings
            }
            
            # Surface as Tradeable Gem if RSI is pullbacked and Solvency is clean
            # We ease the gate slightly (RSI < 45) to capture early consolidation setups
            if rsi < 45.0 and len(warnings) == 0 and not is_etf:
                gems.append({
                    "Ticker": ticker,
                    "Close": float(close_price),
                    "RSI": float(rsi),
                    "Margin": gross_margin,
                    "FCF": fcf,
                    "Thesis": details.get('Thesis', '')
                })
                
            time.sleep(0.05)
            
        except Exception as e:
            print(f"\n  [Error] Failed to scan {ticker}: {str(e)}")
            
    # Print formatted output table
    print("\n" + "=" * 120)
    print(f"{'Ticker':<8} | {'Close':<8} | {'RSI':<6} | {'EMA(20)':<8} | {'Signal Status':<16} | {'Solvency':<20} | {'Thesis'}")
    print("-" * 120)
    for ticker, data in results.items():
        thesis_short = data['Thesis'][:35] + "..." if len(data['Thesis']) > 35 else data['Thesis']
        print(f"{ticker:<8} | ${data['Close']:<7.2f} | {data['RSI_14']:<6.1f} | ${data['EMA_20']:<7.2f} | {data['Signal_Status']:<16} | {data['Solvency_Status']:<20} | {thesis_short}")
    print("=" * 120)
    
    # Print Surfaced Gems
    if len(gems) > 0:
        print("\n" + "\033[92m" + "=== SURFACED TRADEABLE DIPS (RSI < 45 & SOLVENCY PASS) ===" + "\033[0m")
        print("-" * 120)
        for g in gems:
            fcf_str = f"${g['FCF']/1e6:,.1f}M" if not np.isnan(g['FCF']) else "N/A"
            margin_str = f"{g['Margin']:.1f}%" if not np.isnan(g['Margin']) else "N/A"
            print(f"  \033[92m* {g['Ticker']:<6} (Close: ${g['Close']:.2f} | RSI: {g['RSI']:.1f} | Margin: {margin_str} | FCF: {fcf_str})\033[0m")
            print(f"    Thesis: {g['Thesis']}")
        print("-" * 120)
    else:
        print("\nNo tradeable stock dips surfaced (RSI < 45 and PASS solvency). Maintain capital buffer.")
        
    # Print Solvency Warnings for Existing Portfolio Watchlist
    critical_alerts = [t for t, d in results.items() if len(d['Warnings']) > 0]
    if len(critical_alerts) > 0:
        print("\n" + "\033[91m" + "!!! MANAGER WARNING: WATCHLIST ASSETS WITH ACTIVE SOLVENCY THREATS !!!" + "\033[0m")
        print("-" * 120)
        for t in critical_alerts:
            print(f"  \033[93m* {t:<6} triggers: {', '.join(results[t]['Warnings'])}\033[0m")
            print(f"    Action: Avoid new longs. Check if thesis has deteriorated; consider swapping for VRT, HUBB, or PH.")
        print("-" * 120)
        
    # Save output report
    with open(RESULTS_PATH, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"\nScreener run completed. Results saved to: {RESULTS_PATH}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hedge Fund Manager Dynamic FPBV Screener")
    parser.add_argument('--add', type=str, help="Add a ticker to the dynamic watchlist")
    parser.add_argument('--remove', type=str, help="Remove a ticker from the watchlist")
    parser.add_argument('--thesis', type=str, help="The qualitative bottleneck thesis when adding a ticker")
    parser.add_argument('--sector', type=str, default="N/A", help="The sector when adding a ticker")
    parser.add_argument('--etf', action='store_true', help="Flag ticker as an ETF")
    
    args = parser.parse_args()
    
    if args.add:
        if not args.thesis:
            print("[Error] You must provide a --thesis when adding a ticker.")
            sys.exit(1)
        add_ticker(args.add, args.thesis, args.sector, args.etf)
    elif args.remove:
        remove_ticker(args.remove)
    else:
        scan_watchlist()
