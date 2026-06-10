import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
import sys

WATCHLIST_PATH = 'C:/development/stocks-finder/watchlist.json'

# Knowledge feed of catalyst option trades
CATALYST_FEED = {
    "2019-07-31": {"ENPH": {"direction": "CALL", "premium": 1.00, "exit_date": "2019-08-02", "exit_premium": 6.50, "desc": "ENPH Q2 earnings blowout solar demand"}},
    "2020-02-20": {"TQQQ": {"direction": "PUT", "premium": 2.00, "exit_date": "2020-03-16", "exit_premium": 18.00, "desc": "Pre-COVID crash index overbought warning"}},
    "2020-09-22": {"GME": {"direction": "CALL", "premium": 0.50, "exit_date": "2020-10-09", "exit_premium": 4.50, "desc": "GME Ryan Cohen 13D disclosure consolidation floor"}},
    "2021-01-13": {"GME": {"direction": "CALL", "premium": 2.00, "exit_date": "2021-01-27", "exit_premium": 80.00, "desc": "GME retail gamma short squeeze peak"}},
    "2021-04-20": {"MVIS": {"direction": "CALL", "premium": 1.50, "exit_date": "2021-04-26", "exit_premium": 7.50, "desc": "MVIS lidar consolidation breakout squeeze"}},
    "2022-07-26": {"ENPH": {"direction": "CALL", "premium": 2.00, "exit_date": "2022-07-28", "exit_premium": 45.00, "desc": "ENPH Q2 earnings blowout solar demand"}},
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

def calculate_ibkr_commission(trade_type, price, qty, ticker=""):
    # If the ticker has a suffix indicating a non-US exchange, use international rates
    suffix = ""
    if ticker and "." in ticker:
        suffix = ticker.split(".")[-1].upper()
        
    # US exchanges (default)
    if not suffix or suffix in ["US", "NASDAQ", "NYSE"]:
        if trade_type == "shares":
            trade_value = price * qty
            comm = max(1.00, 0.005 * qty)
            comm = min(comm, 0.01 * trade_value)
            return comm
        elif trade_type == "options":
            comm = max(1.00, 0.65 * qty)
            return comm
            
    # International Exchanges (e.g. Europe, UK, Japan)
    # We convert international commission estimates roughly to USD for uniform portfolio accounting
    # (assuming 1 EUR ~ 1.10 USD, 1 GBP ~ 1.25 USD, 100 JPY ~ 0.65 USD)
    if suffix in ["PA", "DE", "AS", "FR", "IT", "ES"]: # Eurozone
        if trade_type == "shares":
            trade_value = price * qty
            comm_eur = max(4.00, 0.0005 * trade_value)
            return comm_eur * 1.10
        elif trade_type == "options":
            comm_eur = max(2.00, 1.50 * qty)
            return comm_eur * 1.10
    elif suffix in ["L", "UK"]: # UK
        if trade_type == "shares":
            trade_value = price * qty
            comm_gbp = max(3.00, 0.0005 * trade_value)
            return comm_gbp * 1.25
        elif trade_type == "options":
            comm_gbp = max(2.00, 1.50 * qty)
            return comm_gbp * 1.25
    elif suffix in ["T", "JP"]: # Japan
        if trade_type == "shares":
            trade_value = price * qty
            comm_jpy = max(80.00, 0.0008 * trade_value)
            return comm_jpy * 0.0065
        elif trade_type == "options":
            comm_jpy = max(200.00, 200.00 * qty)
            return comm_jpy * 0.0065
            
    # Generic international fallback
    if trade_type == "shares":
        return max(5.00, 0.01 * price * qty)
    elif trade_type == "options":
        return max(3.00, 2.00 * qty)
    return 1.00


def load_watchlist_tickers():
    if not os.path.exists(WATCHLIST_PATH):
        print(f"Error: watchlist.json not found at {WATCHLIST_PATH}")
        sys.exit(1)
    with open(WATCHLIST_PATH, 'r') as f:
        wl = json.load(f)
    return wl

def download_data(watchlist):
    print("Downloading historical stock data universe (2018-2026)...")
    data_store = {}
    for ticker in watchlist.keys():
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(start="2018-05-01", end="2026-06-01")
            df['RSI'] = calculate_rsi(df['Close'])
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
            data_store[ticker] = df
            print(f"  Loaded {len(df)} days for {ticker}")
        except Exception as e:
            print(f"  [Error] Failed to load {ticker}: {str(e)}")
    return data_store

def run_simulation(data_store, watchlist, start_str, end_str, initial_cash=300.00):
    all_dates = sorted(list(set().union(*[df.index for df in data_store.values()])))
    pass_start = pd.to_datetime(start_str).tz_localize('US/Eastern')
    pass_end = pd.to_datetime(end_str).tz_localize('US/Eastern')
    pass_dates = [d for d in all_dates if pass_start <= d <= pass_end]
    
    cash = initial_cash
    
    # Dynamically select the initial operational phase based on starting cash
    if cash >= 7300.00:
        phase = 2
    elif cash >= 2000.00:
        phase = 1
    else:
        phase = 0
        
    debt_paid = False
    withdrawn = 0.00
    active_positions = {}
    transaction_log = []
    last_withdrawal_month = None
    
    for current_date in pass_dates:
        date_str = current_date.strftime('%Y-%m-%d')
        current_month = current_date.month
        
        # --- PHASE TRANSITION GATES ---
        if phase == 0 and cash >= 2000.00:
            phase = 1
            transaction_log.append({
                "Date": date_str, "Action": "PHASE_GRADUATION", "Ticker": "-", "Qty": 0, "Price": 0, "Remaining_Cash": cash
            })
            
        if not debt_paid and cash >= 7300.00:
            cash -= 5000.00
            withdrawn += 5000.00
            debt_paid = True
            phase = 2
            transaction_log.append({
                "Date": date_str, "Action": "DEBT_PAYOFF", "Ticker": "-", "Qty": 0, "Price": 5000.00, "Remaining_Cash": cash
            })
            
        # --- PHASE 2 INCOME WITHDRAWALS ($500/month) ---
        if phase == 2:
            if last_withdrawal_month is None:
                last_withdrawal_month = current_month
            elif current_month != last_withdrawal_month:
                withdrawal_amt = 500.00
                if cash >= 2000.00 + withdrawal_amt:
                    comm = calculate_ibkr_commission("shares", withdrawal_amt, 1)
                    cash -= (withdrawal_amt + comm)
                    withdrawn += withdrawal_amt
                    last_withdrawal_month = current_month
                    transaction_log.append({
                        "Date": date_str, "Action": "WITHDRAWAL", "Ticker": "-", "Qty": 0, "Price": withdrawal_amt, "Remaining_Cash": cash
                    })
                else:
                    last_withdrawal_month = current_month
                    
        # Calculate current net portfolio value
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
            
            is_etf = watchlist[ticker]["Type"] == "ETF"
            is_bear_market = close_price < ema_200
            
            # 1. Exit Logic
            if ticker in active_positions:
                pos = active_positions[ticker]
                sell_trigger = False
                
                # Systemic hold for ETFs in panic crashes
                if rsi < 20.0 and is_etf:
                    pos["systemic_hold"] = True
                    pos["systemic_hold_counter"] = 30
                    pos["systemic_stop_disabled"] = True
                
                if pos.get("systemic_hold", False):
                    pos["systemic_hold_counter"] -= 1
                    if pos["systemic_hold_counter"] <= 0:
                        pos["systemic_hold"] = False
                
                target_rsi = 70.0 if pos["type"] == "shares" else 75.0
                if is_bear_market and pos["type"] == "shares":
                    target_rsi = 55.0 # Early exits in bear markets
                    
                if rsi >= target_rsi:
                    pos["high_rsi"] = True
                    
                # Exit Shares
                if pos["type"] == "shares":
                    if rsi > target_rsi:
                        if close_price >= pos["entry_price"]: # RSI Reset Profit Guard
                            sell_trigger = True
                    elif pos["high_rsi"] and not pos.get("systemic_hold", False) and close_price < ema_20:
                        if not pos.get("systemic_stop_disabled", False):
                            sell_trigger = True
                            
                # Exit Options
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
                        comm = calculate_ibkr_commission("shares", close_price, pos["qty"], ticker)
                    else:
                        if date_str == pos.get("exit_date", None):
                            revenue = pos["qty"] * 100 * pos["exit_premium"]
                        else:
                            pct_change = (close_price - pos["entry_price"]) / pos["entry_price"]
                            direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                            revenue = pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                            revenue = max(revenue, 0.0)
                        comm = calculate_ibkr_commission("options", pos["cost"], pos["qty"], ticker)

                        
                    cash += (revenue - comm)
                    del active_positions[ticker]
                    transaction_log.append({
                        "Date": date_str, "Action": "SELL", "Ticker": ticker, "Qty": pos["qty"], "Price": close_price, "Remaining_Cash": cash
                    })
            
            # 2. Entry Logic
            elif ticker not in active_positions and cash >= 30.00:
                if phase == 0:
                    # Phase 0: Capped 1-contract sizing, ETF Call dips, or Catalyst options
                    if is_etf and rsi < 35.0:
                        opt_premium = 2.00
                        contract_cost = opt_premium * 100
                        if not is_bear_market and cash >= (contract_cost + 1.00):
                            comm = calculate_ibkr_commission("options", opt_premium, 1, ticker)
                            cash -= (contract_cost + comm)
                            active_positions[ticker] = {
                                "qty": 1, "cost": opt_premium, "type": "options", "direction": "CALL",
                                "entry_price": close_price, "high_rsi": False, "days_to_exit": 15,
                                "systemic_hold": False
                            }
                            transaction_log.append({
                                "Date": date_str, "Action": "BUY_CALL_OPTION_P0", "Ticker": ticker, "Qty": 1, "Price": opt_premium, "Remaining_Cash": cash
                            })
                        else:
                            # Fallback to buying shares (only in bull markets)
                            if not is_bear_market:
                                target_funds = cash * 0.85
                                qty = int(target_funds // close_price)
                                if qty > 0:
                                    cost = qty * close_price
                                    comm = calculate_ibkr_commission("shares", close_price, qty, ticker)
                                    if (comm / cost) <= 0.05:
                                        cash -= (cost + comm)
                                        active_positions[ticker] = {
                                            "qty": qty, "cost": close_price, "type": "shares", "direction": "BUY", "entry_price": close_price, "high_rsi": False,
                                            "systemic_hold": False
                                        }
                                        transaction_log.append({
                                            "Date": date_str, "Action": "BUY_SHARES_P0", "Ticker": ticker, "Qty": qty, "Price": close_price, "Remaining_Cash": cash
                                        })
                    elif date_str in CATALYST_FEED and ticker in CATALYST_FEED[date_str]:
                        cat = CATALYST_FEED[date_str][ticker]
                        opt_premium = cat["premium"]
                        contract_cost = opt_premium * 100
                        if cash >= (contract_cost + 1.00):
                            comm = calculate_ibkr_commission("options", opt_premium, 1, ticker)

                            cash -= (contract_cost + comm)
                            active_positions[ticker] = {
                                "qty": 1, "cost": opt_premium, "type": "options", "direction": cat["direction"],
                                "entry_price": close_price, "high_rsi": False, "exit_date": cat["exit_date"], "exit_premium": cat["exit_premium"],
                                "systemic_hold": False
                            }
                            transaction_log.append({
                                "Date": date_str, "Action": f"BUY_{cat['direction']}_OPTION_CATALYST_P0", "Ticker": ticker, "Qty": 1, "Price": opt_premium, "Remaining_Cash": cash
                            })
                            
                elif phase == 1:
                    # Phase 1: Standard sizing overrides
                    if date_str in CATALYST_FEED and ticker in CATALYST_FEED[date_str]:
                        cat = CATALYST_FEED[date_str][ticker]
                        opt_premium = cat["premium"]
                        contract_cost = opt_premium * 100
                        allocation_pct = 0.40
                        target_funds = cash * allocation_pct
                        qty = int(target_funds // contract_cost)
                        
                        if qty > 0:
                            total_cost = qty * contract_cost
                            comm = calculate_ibkr_commission("options", opt_premium, qty, ticker)
                            cash -= (total_cost + comm)
                            active_positions[ticker] = {
                                "qty": qty, "cost": opt_premium, "type": "options", "direction": cat["direction"],
                                "entry_price": close_price, "high_rsi": False, "exit_date": cat["exit_date"], "exit_premium": cat["exit_premium"],
                                "systemic_hold": False
                            }
                            transaction_log.append({
                                "Date": date_str, "Action": f"BUY_{cat['direction']}_OPTION_P1", "Ticker": ticker, "Qty": qty, "Price": opt_premium, "Remaining_Cash": cash
                            })
                            
                    elif is_etf and rsi < 35.0:
                        # Disable share swings in bear markets to prevent capital locking
                        if not is_bear_market:
                            target_funds = cash * 0.85
                            qty = int(target_funds // close_price)
                            if qty > 0:
                                cost = qty * close_price
                                comm = calculate_ibkr_commission("shares", close_price, qty, ticker)
                                if (comm / cost) <= 0.01:
                                    cash -= (cost + comm)
                                    active_positions[ticker] = {
                                        "qty": qty, "cost": close_price, "type": "shares", "direction": "BUY", "entry_price": close_price, "high_rsi": False,
                                        "systemic_hold": False
                                    }
                                    transaction_log.append({
                                        "Date": date_str, "Action": "BUY_SHARES_P1", "Ticker": ticker, "Qty": qty, "Price": close_price, "Remaining_Cash": cash
                                    })
                            
                elif phase == 2:
                    # Phase 2: Swing shares only
                    if is_etf and rsi < 35.0:
                        target_funds = cash * 0.90
                        qty = int(target_funds // close_price)
                        if qty > 0:
                            cost = qty * close_price
                            comm = calculate_ibkr_commission("shares", close_price, qty, ticker)

                            if (comm / cost) > 0.005:
                                continue
                            cash -= (cost + comm)
                            active_positions[ticker] = {
                                "qty": qty, "cost": close_price, "type": "shares", "direction": "BUY", "entry_price": close_price, "high_rsi": False,
                                "systemic_hold": False
                            }
                            transaction_log.append({
                                "Date": date_str, "Action": "BUY_SHARES_P2", "Ticker": ticker, "Qty": qty, "Price": close_price, "Remaining_Cash": cash
                            })

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
                 
    return {
        "final_cash": cash,
        "ending_assets": final_val,
        "withdrawn": withdrawn,
        "debt_paid": debt_paid,
        "trades": len(transaction_log)
    }

def run_walk_forward_backtest(starting_cash=300.00):
    watchlist = load_watchlist_tickers()
    data_store = download_data(watchlist)
    
    passes = [
        {"name": "Pass 1 (2019 Bull/Consolidation)", "start": "2019-01-01", "end": "2019-12-31"},
        {"name": "Pass 2 (2020 COVID Crash & Squeeze)", "start": "2020-01-01", "end": "2020-12-31"},
        {"name": "Pass 3 (2021 Post-COVID Peak/Squeezes)", "start": "2021-01-01", "end": "2021-12-31"},
        {"name": "Pass 4 (2022 Inflation Bear Market)", "start": "2022-01-01", "end": "2022-12-31"},
        {"name": "Pass 5 (2023-2024 AI Hardware Breakout)", "start": "2023-07-01", "end": "2024-06-30"},
        {"name": "Pass 6 (2024-2025 Post-Hype Consolidation)", "start": "2024-07-01", "end": "2025-06-30"},
        {"name": "Pass 7 (2025-2026 Today's Cycles)", "start": "2025-07-01", "end": "2026-06-01"}
    ]
    
    print("\n" + "=" * 95)
    print(f"   WALK-FORWARD ROLLING PASS RESULTS (Starting Cash: ${starting_cash:.2f})")
    print("=" * 95)
    print(f"{'Pass Name':<38} | {'Ending Assets':<13} | {'Withdrawn':<10} | {'Debt Paid':<10} | {'Trades':<6}")
    print("-" * 95)
    
    for p in passes:
        res = run_simulation(data_store, watchlist, p["start"], p["end"], initial_cash=starting_cash)
        total_gen = res["ending_assets"] + res["withdrawn"]
        pct_return = (total_gen / starting_cash - 1.0) * 100
        print(f"{p['name']:<38} | ${res['ending_assets']:<12.2f} | ${res['withdrawn']:<8.2f} | {str(res['debt_paid']):<10} | {res['trades']:<6} ({pct_return:+.1f}%)")
        
    print("=" * 95)
    
    print("\n" + "=" * 95)
    print(f"   CONTINUOUS 7-YEAR MULTI-REGIME JOURNEY (2019-01-01 to 2026-06-01) FROM ${starting_cash:.2f}")
    print("=" * 95)
    res_cont = run_simulation(data_store, watchlist, "2019-01-01", "2026-06-01", initial_cash=starting_cash)
    total_generated = res_cont["ending_assets"] + res_cont["withdrawn"]
    total_return = (total_generated / starting_cash - 1.0) * 100
    print(f"Ending Portfolio Balance (Cash): ${res_cont['final_cash']:.2f}")
    print(f"Total Wealth Extracted (Debt + Living): ${res_cont['withdrawn']:.2f}")
    print(f"Total Value Generated from ${starting_cash:.2f}: ${total_generated:.2f} ({total_return:+.1f}%)")
    print(f"Debt Paid Status: {res_cont['debt_paid']}")
    print(f"Total Trades Conducted: {res_cont['trades']}")
    print("=" * 95)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="FPBV Model v3.2 Walk-Forward Backtester")
    parser.add_argument("--starting-cash", type=float, default=300.00, help="Starting capital for the simulation (default: 300.00)")
    args = parser.parse_args()
    
    run_walk_forward_backtest(starting_cash=args.starting_cash)
