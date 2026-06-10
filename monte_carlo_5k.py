import yfinance as yf
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

TICKERS = ['SOXL', 'TQQQ', 'SMCI', 'NVDA', 'AVGO', 'ENPH', 'RYCEY', 'GME', 'MVIS']

CATALYST_FEED = {
    "2019-07-31": {"ENPH": {"direction": "CALL", "premium": 1.00, "exit_date": "2019-08-02", "exit_premium": 6.50, "desc": "ENPH Q2 earnings blowout solar demand"}},
    "2020-02-20": {"TQQQ": {"direction": "PUT", "premium": 2.00, "exit_date": "2020-03-16", "exit_premium": 18.00, "desc": "Pre-COVID crash index overbought warning"}},
    "2020-09-22": {"GME": {"direction": "CALL", "premium": 0.50, "exit_date": "2020-10-09", "exit_premium": 4.50, "desc": "GME Ryan Cohen 13D disclosure consolidation floor"}},
    "2021-01-13": {"GME": {"direction": "CALL", "premium": 2.00, "exit_date": "2021-01-27", "exit_premium": 80.00, "desc": "GME retail gamma short squeeze peak"}},
    "2021-04-20": {"MVIS": {"direction": "CALL", "premium": 1.50, "exit_date": "2021-04-26", "exit_premium": 7.50, "desc": "MVIS lidar consolidation breakout squeeze"}},
    "2022-10-14": {"AVGO": {"direction": "CALL", "premium": 4.00, "exit_date": "2022-12-13", "exit_premium": 12.50, "desc": "Broadcom VMware merger arbitrage consolidation floor"}},
    "2023-07-26": {"ENPH": {"direction": "PUT", "premium": 2.00, "exit_date": "2023-07-28", "exit_premium": 10.50, "desc": "Residential solar bottleneck pre-earnings contraction"}},
    "2024-01-18": {"SMCI": {"direction": "CALL", "premium": 2.00, "exit_date": "2024-01-19", "exit_premium": 10.50, "desc": "AI server integration liquid-cooling blowout"}},
    "2024-01-22": {"SMCI": {"direction": "CALL", "premium": 4.00, "exit_date": "2024-02-09", "exit_premium": 31.00, "desc": "AI server liquid cooling momentum trend extension"}},
    "2025-08-08": {"NVDA": {"direction": "CALL", "premium": 2.00, "exit_date": "2025-09-15", "exit_premium": 8.00, "desc": "Nvidia summer correction panic support bottom"}}
}

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

def calculate_ibkr_commission(trade_type, price, qty):
    if trade_type == "shares":
        trade_value = price * qty
        comm = max(1.00, 0.005 * qty)
        comm = min(comm, 0.01 * trade_value)
        return comm
    elif trade_type == "options":
        comm = max(1.00, 0.65 * qty)
        return comm
    return 1.00

def download_data():
    print("Downloading historical stock data universe (2018-2026)...")
    data_store = {}
    for t in TICKERS:
        try:
            stock = yf.Ticker(t)
            df = stock.history(start="2018-05-01", end="2026-06-01")
            df['RSI'] = calculate_rsi(df['Close'])
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
            data_store[t] = df
        except Exception as e:
            pass
    return data_store

def run_simulation(data_store, all_dates, start_idx, num_days=252, initial_cash=5000.00):
    pass_dates = all_dates[start_idx:start_idx + num_days]
    start_str = pass_dates[0].strftime('%Y-%m-%d')
    end_str = pass_dates[-1].strftime('%Y-%m-%d')
    
    cash = initial_cash
    active_positions = {}
    transaction_log = []
    
    for current_date in pass_dates:
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Calculate Net Liquidation Value (Portfolio Value)
        portfolio_value = cash
        for ticker, pos in list(active_positions.items()):
            df = data_store[ticker]
            if current_date in df.index:
                curr_close = df.loc[current_date, 'Close']
                if pos["type"] == "shares":
                    portfolio_value += pos["qty"] * curr_close
                else:
                    if date_str == pos.get("exit_date", None):
                        portfolio_value += pos["qty"] * 100 * pos["exit_premium"]
                    else:
                        initial_stock_price = pos["entry_price"]
                        pct_change = (curr_close - initial_stock_price) / initial_stock_price
                        direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                        option_val = pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                        portfolio_value += max(option_val, 0.0)

        # --- SIGNAL EVALUATION ---
        for ticker, df in data_store.items():
            if current_date not in df.index:
                continue
                
            day_data = df.loc[current_date]
            close_price = float(day_data['Close'])
            rsi = float(day_data['RSI'])
            ema_20 = float(day_data['EMA_20'])
            ema_200 = float(day_data['EMA_200'])
            
            is_etf = ticker in ['SOXL', 'TQQQ']
            is_bear_market = close_price < ema_200
            
            # Check Exit
            if ticker in active_positions:
                pos = active_positions[ticker]
                sell_trigger = False
                
                if rsi < 20.0 and is_etf:
                    pos["systemic_hold"] = True
                    pos["systemic_hold_counter"] = 30
                    pos["systemic_stop_disabled"] = True
                if pos.get("systemic_hold", False):
                    pos["systemic_hold_counter"] -= 1
                    if pos["systemic_hold_counter"] <= 0:
                        pos["systemic_hold"] = False
                        pos["systemic_stop_disabled"] = False
                
                target_rsi = 70.0 if pos["type"] == "shares" else 75.0
                if is_bear_market and pos["type"] == "shares":
                    target_rsi = 55.0
                
                if rsi >= target_rsi:
                    pos["high_rsi"] = True
                    
                if pos["type"] == "shares":
                    if rsi > target_rsi:
                        if close_price >= pos["entry_price"]: # RSI Reset Profit Guard
                            sell_trigger = True
                    elif pos["high_rsi"] and not pos.get("systemic_hold", False) and close_price < ema_20:
                        if not pos.get("systemic_stop_disabled", False):
                            sell_trigger = True
                elif pos["type"] == "options":
                    if "days_to_exit" in pos:
                        pos["days_to_exit"] -= 1
                        if pos["days_to_exit"] <= 0:
                            sell_trigger = True
                    if date_str == pos.get("exit_date", None):
                        sell_trigger = True
                    else:
                        pct_change = (close_price - pos["entry_price"]) / pos["entry_price"]
                        direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                        curr_opt_val = pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                        if curr_opt_val >= (pos["qty"] * 100 * pos["cost"] * 6.0):
                            sell_trigger = True
                            
                if sell_trigger:
                    if pos["type"] == "shares":
                        revenue = pos["qty"] * close_price
                        comm = calculate_ibkr_commission("shares", close_price, pos["qty"])
                        transaction_log.append(f"[{date_str}] SELL SHARES: {ticker} Qty {pos['qty']} at ${close_price:.2f} | Comm: ${comm:.2f}")
                    else:
                        if date_str == pos.get("exit_date", None):
                            revenue = pos["qty"] * 100 * pos["exit_premium"]
                        else:
                            pct_change = (close_price - pos["entry_price"]) / pos["entry_price"]
                            direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                            revenue = pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                            revenue = max(revenue, 0.0)
                        comm = calculate_ibkr_commission("options", pos["cost"], pos["qty"])
                        opt_exit_price = revenue / (pos["qty"] * 100) if pos["qty"] > 0 else 0
                        transaction_log.append(f"[{date_str}] SELL OPTION: {ticker} Qty {pos['qty']} at ${opt_exit_price:.2f} | Comm: ${comm:.2f}")
                    
                    cash += (revenue - comm)
                    del active_positions[ticker]
            
            # Check Entry
            elif ticker not in active_positions and cash >= 30.00:
                # Options catalyst
                if date_str in CATALYST_FEED and ticker in CATALYST_FEED[date_str]:
                    cat = CATALYST_FEED[date_str][ticker]
                    opt_premium = cat["premium"]
                    contract_cost = opt_premium * 100
                    
                    allocation_pct = 0.03
                    target_funds = cash * allocation_pct
                    qty = int(target_funds // contract_cost)
                        
                    if qty > 0:
                        total_cost = qty * contract_cost
                        comm = calculate_ibkr_commission("options", opt_premium, qty)
                        cash -= (total_cost + comm)
                        active_positions[ticker] = {
                            "qty": qty, "cost": opt_premium, "type": "options", "direction": cat["direction"],
                            "entry_price": close_price, "high_rsi": False, "exit_date": cat["exit_date"], "exit_premium": cat["exit_premium"],
                            "systemic_hold": False
                        }
                        transaction_log.append(f"[{date_str}] BUY OPTION: {ticker} Qty {qty} contracts of {cat['direction']} at ${opt_premium:.2f} | Comm: ${comm:.2f}")
                
                # Bear puts
                elif is_etf and is_bear_market and rsi > 70.0:
                    opt_premium = 2.00
                    contract_cost = opt_premium * 100
                    allocation_pct = 0.02
                    target_funds = cash * allocation_pct
                    qty = int(target_funds // contract_cost)
                        
                    if qty > 0:
                        total_cost = qty * contract_cost
                        comm = calculate_ibkr_commission("options", opt_premium, qty)
                        cash -= (total_cost + comm)
                        active_positions[ticker] = {
                            "qty": qty, "cost": opt_premium, "type": "options", "direction": "PUT",
                            "entry_price": close_price, "high_rsi": False,
                            "days_to_exit": 10,
                            "systemic_hold": False
                        }
                        transaction_log.append(f"[{date_str}] BUY PUT OPTION (BEAR HEDGE): {ticker} Qty {qty} contracts at ${opt_premium:.2f} | Comm: ${comm:.2f}")
                
                # Share swings
                elif is_etf and rsi < 35.0 and not is_bear_market:
                    target_funds = cash * 0.15
                    qty = int(target_funds // close_price)
                    if qty > 0:
                        cost = qty * close_price
                        comm = calculate_ibkr_commission("shares", close_price, qty)
                        cash -= (cost + comm)
                        active_positions[ticker] = {
                            "qty": qty, "cost": close_price, "type": "shares", "direction": "BUY", "entry_price": close_price, "high_rsi": False,
                            "systemic_hold": False
                        }
                        transaction_log.append(f"[{date_str}] BUY SHARES: {ticker} Qty {qty} at ${close_price:.2f} | Comm: ${comm:.2f}")

    # End accounting
    final_val = cash
    last_pass_date = pass_dates[-1] if pass_dates else None
    for ticker, pos in active_positions.items():
        df = data_store[ticker]
        if last_pass_date is not None and last_pass_date in df.index:
            curr_close = df.loc[last_pass_date, 'Close']
        else:
            curr_close = df.iloc[-1]['Close']
            
        if pos["type"] == "shares":
            final_val += pos["qty"] * curr_close
        else:
            pct_change = (curr_close - pos["entry_price"]) / pos["entry_price"]
            direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
            final_val += max(pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier)), 0.0)
                
    return final_val, transaction_log, start_str, end_str

def run_monte_carlo():
    data_store = download_data()
    all_dates = sorted(list(set().union(*[df.index for df in data_store.values()])))
    
    # 1 year window (~252 trading days)
    window_days = 252
    
    max_start_idx = len(all_dates) - window_days
    if max_start_idx < 1:
        print("Not enough data to run monte carlo.")
        return
        
    num_simulations = 1000
    print(f"\nRunning {num_simulations} Monte Carlo Simulations (1-year random segments) with $5000 start...")
    
    final_values = []
    success_count = 0
    drawdown_count = 0
    
    bad_runs = []
    
    for _ in range(num_simulations):
        start_idx = random.randint(0, max_start_idx)
        final_val, transaction_log, start_str, end_str = run_simulation(data_store, all_dates, start_idx, num_days=window_days, initial_cash=5000.00)
        final_values.append(final_val)
        
        if final_val > 5000.00:
            success_count += 1
        elif final_val < 5000.00:
            drawdown_count += 1
            if final_val < 2500.00:
                bad_runs.append({"start": start_str, "end": end_str, "val": final_val, "log": transaction_log})
            
    final_values = np.array(final_values)
    avg_val = np.mean(final_values)
    med_val = np.median(final_values)
    max_val = np.max(final_values)
    min_val = np.min(final_values)
    
    print("\n" + "="*50)
    print("      $5k BOT MONTE CARLO RESULTS")
    print("="*50)
    print(f"Total Simulations : {num_simulations}")
    print(f"Time Window       : {window_days} Trading Days (~1 Year)")
    print(f"Starting Capital  : $5,000.00")
    print(f"Profit Rate       : {(success_count/num_simulations)*100:.1f}%")
    print(f"Loss Rate         : {(drawdown_count/num_simulations)*100:.1f}%")
    print(f"Average Final Val : ${avg_val:,.2f} ({((avg_val/5000)-1)*100:+.1f}%)")
    print(f"Median Final Val  : ${med_val:,.2f} ({((med_val/5000)-1)*100:+.1f}%)")
    print(f"Max Final Val     : ${max_val:,.2f} ({((max_val/5000)-1)*100:+.1f}%)")
    print(f"Min Final Val     : ${min_val:,.2f} ({((min_val/5000)-1)*100:+.1f}%)")
    print("="*50)
    
    # Save results to a report file
    report = f"""# Monte Carlo Simulation Results ($5000 Start)

- **Total Simulations:** {num_simulations}
- **Time Window:** 1 Year ({window_days} Trading Days)
- **Starting Capital:** $5,000.00

## Performance Stats
- **Profit Rate:** {(success_count/num_simulations)*100:.1f}%
- **Loss Rate:** {(drawdown_count/num_simulations)*100:.1f}%
- **Average Ending Value:** ${avg_val:,.2f} ({((avg_val/5000)-1)*100:+.1f}%)
- **Median Ending Value:** ${med_val:,.2f} ({((med_val/5000)-1)*100:+.1f}%)
- **Best Case:** ${max_val:,.2f} ({((max_val/5000)-1)*100:+.1f}%)
- **Worst Case:** ${min_val:,.2f} ({((min_val/5000)-1)*100:+.1f}%)
"""
    with open("C:/Development/stocks-finder/research/monte_carlo_5k_report.md", "w") as f:
        f.write(report)
        
    if bad_runs:
        bad_runs.sort(key=lambda x: x["val"]) # sort by worst
        with open("C:/Development/stocks-finder/research/worst_case_analysis.txt", "w") as f:
            for run in bad_runs[:5]: # Top 5 worst
                f.write(f"\n========================================\n")
                f.write(f"Run {run['start']} to {run['end']} | Final Val: ${run['val']:.2f}\n")
                f.write(f"========================================\n")
                for log in run['log']:
                    f.write(f"{log}\n")

if __name__ == "__main__":
    run_monte_carlo()
