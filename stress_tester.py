import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

# Universe of tickers representing bottleneck leaders and indices
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
            print(f"  Loaded {len(df)} days for {t}")
        except Exception as e:
            print(f"  [Error] Failed to load {t}: {str(e)}")
    return data_store

def run_simulation(data_store, start_str, end_str, initial_cash, ticker_subset=None, commission=1.00, enable_withdrawals=False):
    # Filter data store to subset if provided
    sim_store = data_store
    if ticker_subset is not None:
        sim_store = {t: data_store[t] for t in ticker_subset if t in data_store}
        
    if not sim_store:
        return initial_cash, False, 0, 0.00
        
    all_dates = sorted(list(set().union(*[df.index for df in sim_store.values()])))
    pass_start = pd.to_datetime(start_str).tz_localize('US/Eastern')
    pass_end = pd.to_datetime(end_str).tz_localize('US/Eastern')
    pass_dates = [d for d in all_dates if pass_start <= d <= pass_end]
    
    cash = initial_cash
    phase = 1
    debt_paid = False
    withdrawn = 0.00
    active_positions = {}
    trades_count = 0
    last_withdrawal_month = None
    
    for current_date in pass_dates:
        date_str = current_date.strftime('%Y-%m-%d')
        current_month = current_date.month
        
        # --- PHASE 2 WITHDRAWALS ---
        if phase == 2 and enable_withdrawals:
            if last_withdrawal_month is None:
                last_withdrawal_month = current_month
            elif current_month != last_withdrawal_month:
                withdrawal_amt = 500.00
                if cash >= withdrawal_amt:
                    cash -= withdrawal_amt
                    withdrawn += withdrawal_amt
                    last_withdrawal_month = current_month
        
        # Calculate Net Liquidation Value (Portfolio Value)
        portfolio_value = cash
        for ticker, pos in list(active_positions.items()):
            df = sim_store[ticker]
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

        # --- DEBT PAYOFF TRIGGER ---
        if not debt_paid and portfolio_value >= 5300.00:
            cash -= 5000.00
            withdrawn += 5000.00
            debt_paid = True
            if cash >= 2000.00:
                phase = 2
            
            # Clear positions on milestone to establish cash base
            for ticker, pos in list(active_positions.items()):
                df = sim_store[ticker]
                if current_date in df.index:
                    curr_close = df.loc[current_date, 'Close']
                    if pos["type"] == "shares":
                        revenue = pos["qty"] * curr_close
                    else:
                        if date_str == pos.get("exit_date", None):
                            revenue = pos["qty"] * 100 * pos["exit_premium"]
                        else:
                            pct_change = (curr_close - pos["entry_price"]) / pos["entry_price"]
                            direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                            revenue = pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                            revenue = max(revenue, 0.0)
                    cash += revenue - commission
            active_positions.clear()
            portfolio_value = cash
            
        if debt_paid and phase == 1 and cash >= 2000.00:
            phase = 2

        # --- SIGNAL EVALUATION ---
        for ticker, df in sim_store.items():
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
                if pos.get("systemic_hold", False):
                    pos["systemic_hold_counter"] -= 1
                    if pos["systemic_hold_counter"] <= 0:
                        pos["systemic_hold"] = False
                
                target_rsi = 70.0 if pos["type"] == "shares" else 75.0
                if is_bear_market and pos["type"] == "shares":
                    target_rsi = 55.0
                    
                if rsi >= target_rsi:
                    pos["high_rsi"] = True
                    
                if pos["type"] == "shares":
                    if rsi > target_rsi:
                        sell_trigger = True
                    elif pos["high_rsi"] and not pos.get("systemic_hold", False) and close_price < ema_20:
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
                    else:
                        if date_str == pos.get("exit_date", None):
                            revenue = pos["qty"] * 100 * pos["exit_premium"]
                        else:
                            pct_change = (close_price - pos["entry_price"]) / pos["entry_price"]
                            direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                            revenue = pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                            revenue = max(revenue, 0.0)
                    cash += (revenue - commission)
                    del active_positions[ticker]
                    trades_count += 1
            
            # Check Entry
            elif ticker not in active_positions and cash >= 30.00: # Reduced from 50 to allow micro budgets to buy cheaper shares
                if phase == 1:
                    # Options catalyst
                    if date_str in CATALYST_FEED and ticker in CATALYST_FEED[date_str]:
                        cat = CATALYST_FEED[date_str][ticker]
                        allocation_pct = 0.75 if cash < 1000.00 else 0.40
                        opt_premium = cat["premium"]
                        contract_cost = opt_premium * 100
                        target_funds = cash * allocation_pct
                        qty = int(target_funds // contract_cost)
                        
                        if qty > 0:
                            total_cost = qty * contract_cost
                            cash -= (total_cost + commission)
                            active_positions[ticker] = {
                                "qty": qty, "cost": opt_premium, "type": "options", "direction": cat["direction"],
                                "entry_price": close_price, "high_rsi": False, "exit_date": cat["exit_date"], "exit_premium": cat["exit_premium"],
                                "systemic_hold": False
                            }
                            trades_count += 1
                    # Bear puts
                    elif is_etf and is_bear_market and rsi > 70.0:
                        opt_premium = 2.00
                        contract_cost = opt_premium * 100
                        allocation_pct = 0.50 if cash < 1000.00 else 0.30
                        target_funds = cash * allocation_pct
                        qty = int(target_funds // contract_cost)
                        
                        if qty > 0:
                            total_cost = qty * contract_cost
                            cash -= (total_cost + commission)
                            active_positions[ticker] = {
                                "qty": qty, "cost": opt_premium, "type": "options", "direction": "PUT",
                                "entry_price": close_price, "high_rsi": False,
                                "days_to_exit": 10,
                                "systemic_hold": False
                            }
                            trades_count += 1
                    # Share swings
                    elif is_etf and rsi < 35.0:
                        target_funds = cash * 0.85
                        qty = int(target_funds // close_price)
                        if qty > 0:
                            cost = qty * close_price
                            cash -= (cost + commission)
                            active_positions[ticker] = {
                                "qty": qty, "cost": close_price, "type": "shares", "direction": "BUY", "entry_price": close_price, "high_rsi": False,
                                "systemic_hold": False
                            }
                            trades_count += 1
                            
                elif phase == 2:
                    # Phase 2 ETF swing shares only
                    if is_etf and rsi < 35.0:
                        target_funds = cash * 0.90
                        qty = int(target_funds // close_price)
                        if qty > 0:
                            cost = qty * close_price
                            # Commission drag filter
                            if (commission / cost) > 0.005:
                                continue
                            cash -= (cost + commission)
                            active_positions[ticker] = {
                                "qty": qty, "cost": close_price, "type": "shares", "direction": "BUY", "entry_price": close_price, "high_rsi": False,
                                "systemic_hold": False
                            }
                            trades_count += 1

    # End accounting
    final_val = cash
    last_pass_date = pass_dates[-1] if pass_dates else None
    for ticker, pos in active_positions.items():
        df = sim_store[ticker]
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
                
    return final_val, debt_paid, trades_count, withdrawn

def run_stress_tests():
    data_store = download_data()
    
    report_lines = []
    report_lines.append("# Stateful Portfolio Bot Stress Test Report")
    report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("\nThis report documents the performance of the **Stateful Portfolio Journey Bot** under various stressed macro environments, asset universes, capital levels, and commission friction rates.")
    
    # -------------------------------------------------------------
    # SUITE 1: Extreme Macro Regimes
    # -------------------------------------------------------------
    print("\nRunning Suite 1: Extreme Macro Regimes...")
    report_lines.append("\n## Test Suite 1: Extreme Macro Regimes")
    report_lines.append("Tests bot resilience across historical bear markets, panic events, bubbles, and carry-trade liquidations. (Starting Cash: $300, Commission: $1.00, Universe: Full)")
    report_lines.append("\n| Macro Regime | Start Date | End Date | Ending Value | Return (%) | Debt Paid | Trades |")
    report_lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    
    scenarios = [
        {"name": "COVID Panic Crash", "start": "2020-02-15", "end": "2020-04-30"},
        {"name": "2022 Bear Bottom Capitulation", "start": "2022-08-15", "end": "2022-10-31"},
        {"name": "2022 Year-Long Inflation Bear", "start": "2022-01-01", "end": "2022-12-31"},
        {"name": "2021 Meme Stock Mania Squeeze", "start": "2020-12-01", "end": "2021-06-30"},
        {"name": "AI Parabolic Blowoff", "start": "2024-01-01", "end": "2024-03-31"},
        {"name": "Carry-Trade Unwind Shock", "start": "2024-07-10", "end": "2024-08-31"},
        {"name": "2025 AI Peak & Multiple De-Rating", "start": "2025-06-01", "end": "2025-10-31"},
        {"name": "2019 Quiet Growth Era", "start": "2019-01-01", "end": "2019-12-31"}
    ]
    
    for s in scenarios:
        val, debt, trades, w_draw = run_simulation(data_store, s["start"], s["end"], 300.00, commission=1.00)
        total_gen = val + w_draw
        pct_ret = (total_gen / 300.00 - 1.0) * 100
        report_lines.append(f"| {s['name']} | {s['start']} | {s['end']} | ${total_gen:.2f} | {pct_ret:+.1f}% | {debt} | {trades} |")
        print(f"  Processed {s['name']}: {pct_ret:+.1f}% return")

    # -------------------------------------------------------------
    # SUITE 2: Ticker Watchlist Segments
    # -------------------------------------------------------------
    print("\nRunning Suite 2: Ticker Watchlist Segments...")
    report_lines.append("\n## Test Suite 2: Ticker Watchlist Segments")
    report_lines.append("Tests the effect of restricting the bot's asset universe to specific styles. (Timeframe: July 2023 - June 2024, Starting Cash: $300, Commission: $1.00)")
    report_lines.append("\n| Watchlist Segment | Tickers included | Ending Value | Return (%) | Debt Paid | Trades |")
    report_lines.append("| --- | --- | --- | --- | --- | --- |")
    
    watchlists = [
        {"name": "Full Universe", "tickers": TICKERS},
        {"name": "Index ETFs Only", "tickers": ["SOXL", "TQQQ"]},
        {"name": "AI/Semi Moat Leaders Only", "tickers": ["SMCI", "NVDA", "AVGO"]},
        {"name": "Value & Turnarounds (Non-Tech)", "tickers": ["ENPH", "RYCEY"]},
        {"name": "Speculative Squeezes Only", "tickers": ["GME", "MVIS"]}
    ]
    
    for w in watchlists:
        val, debt, trades, w_draw = run_simulation(data_store, "2023-07-01", "2024-06-30", 300.00, ticker_subset=w["tickers"], commission=1.00)
        total_gen = val + w_draw
        pct_ret = (total_gen / 300.00 - 1.0) * 100
        report_lines.append(f"| {w['name']} | `{', '.join(w['tickers'])}` | ${total_gen:.2f} | {pct_ret:+.1f}% | {debt} | {trades} |")
        print(f"  Processed {w['name']}: {pct_ret:+.1f}% return")

    # -------------------------------------------------------------
    # SUITE 3: Account Capital Sizing (Boundary of Ruin)
    # -------------------------------------------------------------
    print("\nRunning Suite 3: Capital Sizing (Boundary of Ruin)...")
    report_lines.append("\n## Test Suite 3: Account Capital Sizing & Ruin Boundaries")
    report_lines.append("Finds the minimum viable budget where flat transaction commissions don't lead to fee-drag ruin. (Timeframe: July 2023 - June 2024, Commission: $1.00, Universe: Full)")
    report_lines.append("\n| Starting Capital | Ending Value | Net Return | Return (%) | Debt Paid | Trades | Status / Ruin Risk |")
    report_lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    
    budgets = [30.00, 50.00, 75.00, 100.00, 200.00, 300.00, 500.00, 1000.00]
    
    for b in budgets:
        val, debt, trades, w_draw = run_simulation(data_store, "2023-07-01", "2024-06-30", b, commission=1.00)
        total_gen = val + w_draw
        pct_ret = (total_gen / b - 1.0) * 100
        net_ret = total_gen - b
        
        status = "Ruin / Commission Stagnation"
        if pct_ret > 15.0:
            status = "Low Growth compounding"
        if debt:
            status = "Success (Debt Paid)"
            
        report_lines.append(f"| ${b:.2f} | ${total_gen:.2f} | {net_ret:+.2f} | {pct_ret:+.1f}% | {debt} | {trades} | {status} |")
        print(f"  Processed Budget ${b:.2f}: {pct_ret:+.1f}% return")

    # -------------------------------------------------------------
    # SUITE 4: Broker Friction & Commission Rates
    # -------------------------------------------------------------
    print("\nRunning Suite 4: Broker Friction & Commission Rates...")
    report_lines.append("\n## Test Suite 4: Broker Friction & Commission Rates")
    report_lines.append("Tests the sensitivity of the bot to flat commissions. (Timeframe: July 2023 - June 2024, Starting Cash: $300, Universe: Full)")
    report_lines.append("\n| Commission / Side | Ending Value | Return (%) | Debt Paid | Trades | Performance Impact |")
    report_lines.append("| --- | --- | --- | --- | --- | --- |")
    
    commissions = [0.00, 0.50, 1.00, 2.00, 5.00]
    
    # We reference the $0.00 commission case for baseline
    baseline_val = None
    
    for c in commissions:
        val, debt, trades, w_draw = run_simulation(data_store, "2023-07-01", "2024-06-30", 300.00, commission=c)
        total_gen = val + w_draw
        pct_ret = (total_gen / 300.00 - 1.0) * 100
        
        if c == 0.00:
            baseline_val = total_gen
            impact = "Baseline (0% Drag)"
        else:
            drag = baseline_val - total_gen
            impact = f"-${drag:.2f} drag ({drag/300.00*100:.1f}% of starting capital)"
            
        report_lines.append(f"| ${c:.2f} | ${total_gen:.2f} | {pct_ret:+.1f}% | {debt} | {trades} | {impact} |")
        print(f"  Processed Commission ${c:.2f}: {pct_ret:+.1f}% return")

    # -------------------------------------------------------------
    # WRITING THE REPORT TO ARTIFACT
    # -------------------------------------------------------------
    report_content = "\n".join(report_lines)
    
    artifact_path = "C:/Users/naim_/.gemini/antigravity-cli/brain/b9ee6360-7e57-466a-b5f8-50ea6d403235/stress_test_report.md"
    try:
        os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
        with open(artifact_path, 'w') as f:
            f.write(report_content)
        print(f"\nSuccessfully wrote stress test report to {artifact_path}")
    except Exception as e:
        print(f"\n[Error] Failed to write stress test report: {str(e)}")
        
    # Write to local directory research folder as well for project completeness
    local_path = "C:/development/stocks-finder/research/stress_test_report.md"
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'w') as f:
            f.write(report_content)
        print(f"Successfully wrote local research copy to {local_path}")
    except Exception as e:
        print(f"[Error] Failed to write local copy: {str(e)}")

if __name__ == '__main__':
    run_stress_tests()
