import yfinance as yf
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

def download_data(tickers, start_date, end_date):
    print(f"Downloading historical data for {tickers} from {start_date} to {end_date}...")
    data = {}
    for ticker in tickers:
        # download single ticker
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if not df.empty:
            # Flatten multi-index columns if present (yfinance does this sometimes)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            df['RSI'] = calculate_rsi(df['Close'])
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
            df = df.dropna()
            data[ticker] = df
    return data

def run_simulation(data, start_idx, max_days=500):
    cash = 300.0
    active_position = None  # {ticker, qty, cost_basis, high_rsi, systemic_hold, systemic_hold_counter}
    
    # We need a shared date index. Assume the first ticker dictates the trading days.
    first_ticker = list(data.keys())[0]
    trading_days = data[first_ticker].index.tolist()
    
    if start_idx + max_days >= len(trading_days):
        max_days = len(trading_days) - start_idx - 1
        
    peak_cash = cash
    lowest_cash = cash
    
    for i in range(start_idx, start_idx + max_days):
        current_date = trading_days[i]
        
        # Portfolio value (cash + position value)
        port_val = cash
        if active_position:
            ticker = active_position['ticker']
            if current_date in data[ticker].index:
                row = data[ticker].loc[current_date]
                close = float(row['Close'].iloc[0]) if isinstance(row['Close'], pd.Series) else float(row['Close'])
                port_val += active_position['qty'] * close
        
        if port_val > peak_cash:
            peak_cash = port_val
        if port_val < lowest_cash:
            lowest_cash = port_val
            
        if port_val >= 2000.0:
            return True, i - start_idx, port_val, lowest_cash
        if port_val <= 50.0 and not active_position:
            # Busted (can't buy anymore)
            return False, i - start_idx, port_val, lowest_cash

        # Process exits
        if active_position:
            ticker = active_position['ticker']
            if current_date not in data[ticker].index:
                continue
            
            row = data[ticker].loc[current_date]
            close = float(row['Close'].iloc[0]) if isinstance(row['Close'], pd.Series) else float(row['Close'])
            rsi = float(row['RSI'].iloc[0]) if isinstance(row['RSI'], pd.Series) else float(row['RSI'])
            ema_20 = float(row['EMA_20'].iloc[0]) if isinstance(row['EMA_20'], pd.Series) else float(row['EMA_20'])
            ema_200 = float(row['EMA_200'].iloc[0]) if isinstance(row['EMA_200'], pd.Series) else float(row['EMA_200'])
            
            is_bear_market = close < ema_200
            
            # Systemic Crash Easing
            if rsi < 20.0:
                active_position["systemic_hold"] = True
                active_position["systemic_hold_counter"] = 30
                
            if active_position.get("systemic_hold", False):
                active_position["systemic_hold_counter"] -= 1
                if active_position["systemic_hold_counter"] <= 0:
                    active_position["systemic_hold"] = False
                    
            target_rsi = 55.0 if is_bear_market else 70.0
            if rsi >= target_rsi:
                active_position['high_rsi'] = True
                
            sell_trigger = False
            if rsi > target_rsi:
                # Profit guard
                if close >= active_position['cost_basis']:
                    sell_trigger = True
            elif active_position.get("high_rsi", False) and not active_position.get("systemic_hold", False) and close < ema_20:
                sell_trigger = True
                
            if sell_trigger:
                revenue = active_position['qty'] * close
                # Calculate commission roughly (0.005/share, min $1.00)
                comm = max(1.00, 0.005 * active_position['qty'])
                cash += (revenue - comm)
                active_position = None
                
        # Process entries (only if no active position)
        if not active_position and cash >= 50.0:
            # Find candidate
            best_candidate = None
            lowest_rsi = 100.0
            
            for ticker in data.keys():
                if current_date not in data[ticker].index:
                    continue
                row = data[ticker].loc[current_date]
                close = float(row['Close'].iloc[0]) if isinstance(row['Close'], pd.Series) else float(row['Close'])
                rsi = float(row['RSI'].iloc[0]) if isinstance(row['RSI'], pd.Series) else float(row['RSI'])
                
                # Phase 0 ETF logic
                if rsi < 35.0:
                    # Prefer the one with lowest RSI
                    if rsi < lowest_rsi:
                        lowest_rsi = rsi
                        best_candidate = {
                            'ticker': ticker,
                            'close': close,
                            'rsi': rsi
                        }
            
            if best_candidate:
                # Buy
                target_funds = cash * 0.85
                qty = int(target_funds // best_candidate['close'])
                if qty > 0:
                    cost = qty * best_candidate['close']
                    comm = max(1.00, 0.005 * qty)
                    if cash >= cost + comm:
                        cash -= (cost + comm)
                        active_position = {
                            'ticker': best_candidate['ticker'],
                            'qty': qty,
                            'cost_basis': best_candidate['close'],
                            'high_rsi': False,
                            'systemic_hold': False,
                            'systemic_hold_counter': 0
                        }

    # End of simulation timeout
    port_val = cash
    if active_position:
        ticker = active_position['ticker']
        last_date = trading_days[start_idx + max_days - 1]
        if last_date in data[ticker].index:
            row = data[ticker].loc[last_date]
            close = float(row['Close'].iloc[0]) if isinstance(row['Close'], pd.Series) else float(row['Close'])
            port_val += active_position['qty'] * close
            
    return False, max_days, port_val, lowest_cash

def main():
    # We will test using SOXL and TQQQ which the bot relies on in Phase 0
    tickers = ['TQQQ', 'SOXL']
    data = download_data(tickers, '2020-01-01', '2026-06-01')
    
    first_ticker = list(data.keys())[0]
    trading_days = data[first_ticker].index.tolist()
    total_days = len(trading_days)
    
    # We want to be able to run for up to 500 trading days (~2 years)
    max_start_idx = total_days - 500
    if max_start_idx < 1:
        print("Not enough data. Increase date range.")
        return
        
    num_simulations = 1000
    
    success_count = 0
    total_days_to_grad = 0
    busted_count = 0
    stagnant_count = 0
    lowest_drawdowns = []
    
    print(f"\nRunning {num_simulations} Monte Carlo Simulations (Phase 0: $300 to $2k)...")
    
    for _ in range(num_simulations):
        start_idx = random.randint(0, max_start_idx)
        
        graduated, days, final_val, lowest = run_simulation(data, start_idx, max_days=500)
        
        lowest_drawdowns.append(lowest)
        
        if graduated:
            success_count += 1
            total_days_to_grad += days
        elif final_val <= 50.0:
            busted_count += 1
        else:
            stagnant_count += 1
            
    avg_days = total_days_to_grad / success_count if success_count > 0 else 0
    avg_lowest = sum(lowest_drawdowns) / len(lowest_drawdowns)
    
    print("\n" + "="*50)
    print("      PHASE 0 MONTE CARLO RESULTS")
    print("="*50)
    print(f"Total Simulations : {num_simulations}")
    print(f"Time Limit per run: 500 Trading Days (~2 Years)")
    print(f"Graduated ($2k+)  : {success_count} ({(success_count/num_simulations)*100:.1f}%)")
    print(f"Busted (<$50)     : {busted_count} ({(busted_count/num_simulations)*100:.1f}%)")
    print(f"Stagnant (TimeOut): {stagnant_count} ({(stagnant_count/num_simulations)*100:.1f}%)")
    if success_count > 0:
        print(f"Avg Days to Grad  : {avg_days:.1f} days (~{avg_days/252:.1f} years)")
    print(f"Avg Lowest PnL Dip: ${avg_lowest:.2f} (from starting $300)")
    print("="*50)

if __name__ == "__main__":
    main()
