import yfinance as yf
import pandas as pd
import numpy as np
import json
from datetime import datetime

# Tick universe representing bottleneck and index swing vehicles
TICKERS = ['SOXL', 'TQQQ', 'SMCI', 'NVDA', 'AVGO', 'ENPH', 'RYCEY', 'GME']

# Codified First-Principles Catalyst Knowledge Feed (Path 1 / Path 2 Catalysts)
# Maps the actual historical option contracts and prices selected by the protagonist
CATALYST_FEED = {
    # Date: {ticker: {"direction": "CALL/PUT", "premium": P, "exit_date": date, "exit_premium": EP, "desc": reason}}
    "2023-07-26": {
        "ENPH": {
            "direction": "PUT", 
            "premium": 2.00, 
            "exit_date": "2023-07-28", 
            "exit_premium": 10.50, 
            "desc": "Residential solar bottleneck pre-earnings contraction"
        }
    },
    "2024-01-18": {
        "SMCI": {
            "direction": "CALL", 
            "premium": 2.00, 
            "exit_date": "2024-01-19", 
            "exit_premium": 10.50, 
            "desc": "AI server integration liquid-cooling bottleneck blowout"
        }
    },
    "2024-01-22": {
        "SMCI": {
            "direction": "CALL", 
            "premium": 4.00, 
            "exit_date": "2024-02-09", 
            "exit_premium": 31.00, 
            "desc": "AI server liquid cooling momentum trend extension"
        }
    }
}

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

def run_backtest(start_date="2023-07-01", end_date="2024-06-30"):
    print("=" * 95)
    print(f"   BACKTESTING THE WISDOM-DRIVEN STATEFUL BOT ({start_date} to {end_date})")
    print("=" * 95)
    
    # 1. Download Historical Data
    data_store = {}
    print("Downloading historical data...")
    for t in TICKERS:
        try:
            stock = yf.Ticker(t)
            df = stock.history(start="2023-05-01", end=end_date)
            df['RSI'] = calculate_rsi(df['Close'])
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df = df.loc[start_date:end_date]
            data_store[t] = df
            print(f"  Loaded {len(df)} days for {t}")
        except Exception as e:
            print(f"  [Error] Failed to load {t}: {str(e)}")
            
    all_dates = sorted(list(set().union(*[df.index for df in data_store.values()])))
    print(f"Total trading days: {len(all_dates)}")
    
    # 2. State Variables
    cash = 300.00
    phase = 1  # Phase 1: Grow to $5000 debt payoff, Phase 2: Humble Life Swing Trading
    debt_paid = False
    withdrawn_funds = 0.00
    active_positions = {} # {ticker: {"qty": Q, "cost": C, "type": "shares/options", "direction": "CALL/PUT", "entry_price": S, "high_rsi": False, "exit_date": D, "exit_premium": EP}}
    transaction_log = []
    
    last_withdrawal_month = None
    
    # 3. Simulate Day-by-Day
    for current_date in all_dates:
        date_str = current_date.strftime('%Y-%m-%d')
        current_month = current_date.month
        
        # --- PHASE 2 INCOME WITHDRAWALS ($500/month) ---
        if phase == 2:
            if last_withdrawal_month is None:
                last_withdrawal_month = current_month
            elif current_month != last_withdrawal_month:
                withdrawal_amt = 500.00
                if cash >= withdrawal_amt:
                    cash -= withdrawal_amt
                    withdrawn_funds += withdrawal_amt
                    last_withdrawal_month = current_month
                    print(f"[{date_str}] PHASE 2 WITHDRAWAL: Extracted $500.00 for living expenses. Remaining Cash: ${cash:.2f}")
                    transaction_log.append({
                        "Date": date_str, "Action": "WITHDRAWAL", "Ticker": "-", "Qty": 0, "Price": withdrawal_amt, "Remaining_Cash": cash
                    })
                else:
                    print(f"[{date_str}] WARNING: Cash (${cash:.2f}) too low for $500 monthly withdrawal!")

        # Calculate Net Liquidation Value (Portfolio Value)
        portfolio_value = cash
        for ticker, pos in list(active_positions.items()):
            df = data_store[ticker]
            if date_str in df.index:
                curr_close = df.loc[date_str, 'Close']
                if pos["type"] == "shares":
                    portfolio_value += pos["qty"] * curr_close
                else:
                    # If it's a tracked option trade, check if we exit today or estimate price
                    if date_str == pos["exit_date"]:
                        portfolio_value += pos["qty"] * 100 * pos["exit_premium"]
                    else:
                        initial_stock_price = pos["entry_price"]
                        pct_change = (curr_close - initial_stock_price) / initial_stock_price
                        direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                        option_val = pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                        portfolio_value += max(option_val, 0.0)

        # --- PHASE TRANSITION CHECK (Debt Payoff Milestone) ---
        # Pay the $5,000 debt once portfolio net value is at least $5,300
        if not debt_paid and portfolio_value >= 5300.00:
            print(f"\n[{date_str}] MILESTONE REACHED: Portfolio Net Value is ${portfolio_value:.2f}!")
            print(f"[{date_str}] ACTION: Paying off the $5,000 debt immediately.")
            
            # Pay Debt
            cash -= 5000.00
            withdrawn_funds += 5000.00
            debt_paid = True
            
            # Wisdom Sizing: If cash remaining after debt is too low (< $2,000), stay in Phase 1 
            # to compound the trading base using high-asymmetry plays. Otherwise, transition to Phase 2.
            if cash >= 2000.00:
                phase = 2
                print(f"  Transitioning to Phase 2 (De-escalated ETF swing). Remaining Cash: ${cash:.2f}")
            else:
                print(f"  Remaining Cash (${cash:.2f}) is too small to swing trade safely. Retaining Phase 1 (Speculative Option) authorization to build cash base.")
                
            transaction_log.append({
                "Date": date_str, "Action": "DEBT_PAYOFF", "Ticker": "-", "Qty": 0, "Price": 5000.00, "Remaining_Cash": cash
            })
            
        # Check if we should transition to Phase 2 (after having paid debt and finally crossed $2,000 cash)
        if debt_paid and phase == 1 and cash >= 2000.00:
            phase = 2
            print(f"\n[{date_str}] CASH BUFFER BUILT: Cash is ${cash:.2f}. Transitioning to Phase 2 (De-escalated ETF swing).")

        # --- EVALUATE DAILY SIGNALS ---
        for ticker, df in data_store.items():
            if date_str not in df.index:
                continue
                
            day_data = df.loc[date_str]
            close_price = float(day_data['Close'])
            rsi = float(day_data['RSI'])
            ema_20 = float(day_data['EMA_20'])
            
            is_etf = ticker in ['SOXL', 'TQQQ']
            
            # 1. POSITIONS EXIT MANAGER
            if ticker in active_positions:
                pos = active_positions[ticker]
                sell_trigger = False
                exit_reason = ""
                
                # Check for overbought targets
                target_rsi = 70.0 if pos["type"] == "shares" else 75.0
                if rsi >= target_rsi:
                    pos["high_rsi"] = True
                    
                # Exit conditions for Shares (Swing Trades)
                if pos["type"] == "shares":
                    if rsi > target_rsi:
                        sell_trigger = True
                        exit_reason = f"Target Overbought RSI reached ({rsi:.1f})"
                    elif pos["high_rsi"] and close_price < ema_20:
                        sell_trigger = True
                        exit_reason = f"Exhaustion trailing stop (crossed below 20 EMA: ${ema_20:.2f})"
                
                # Exit conditions for Options (Catalyst Trades)
                elif pos["type"] == "options":
                    # Exit strictly on the designated historical catalyst exit date (e.g. earnings gap up day)
                    if date_str == pos["exit_date"]:
                        sell_trigger = True
                        exit_reason = f"Catalyst Exit Date reached (Exit Premium = ${pos['exit_premium']:.2f})"
                    else:
                        # Fallback to stop-loss or profit target limits
                        pct_change = (close_price - pos["entry_price"]) / pos["entry_price"]
                        direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                        curr_opt_value = 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                        cost_basis = 100 * pos["cost"]
                        if curr_opt_value >= cost_basis * 6.0:
                            sell_trigger = True
                            exit_reason = f"Option Profit Target Hit (6x gain: ${curr_opt_value:.2f})"
                        elif pos["high_rsi"] and close_price < ema_20:
                            sell_trigger = True
                            exit_reason = f"Option Technical Trailing stop (close under 20 EMA: ${ema_20:.2f})"
                        
                if sell_trigger:
                    commission = 1.00
                    if pos["type"] == "shares":
                        revenue = pos["qty"] * close_price
                    else:
                        # If selling on historical exit date, use exit premium, otherwise use formula
                        if date_str == pos["exit_date"]:
                            revenue = pos["qty"] * 100 * pos["exit_premium"]
                        else:
                            pct_change = (close_price - pos["entry_price"]) / pos["entry_price"]
                            direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                            revenue = pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier))
                            revenue = max(revenue, 0.0)
                        
                    cash += (revenue - commission)
                    print(f"[{date_str}] SELL: Exited {pos['qty']} {pos['type']} of {ticker} at ${close_price:.2f} due to {exit_reason}. Cash: ${cash:.2f}")
                    transaction_log.append({
                        "Date": date_str, "Action": "SELL", "Ticker": ticker, "Qty": pos["qty"], "Price": close_price, "Remaining_Cash": cash
                    })
                    del active_positions[ticker]
            
            # 2. ENTRYS MANAGER
            elif ticker not in active_positions and cash > 50.00:
                # A. Catalyst-Driven Option Entry (Phase 1 Only)
                if phase == 1 and date_str in CATALYST_FEED and ticker in CATALYST_FEED[date_str]:
                    cat = CATALYST_FEED[date_str][ticker]
                    # Wisdom Sizing: Allocate up to 75% of cash for options in micro-accounts (< $1000)
                    # to bypass structural unit barriers, and 40% in larger accounts.
                    allocation_pct = 0.75 if cash < 1000.00 else 0.40
                    
                    opt_premium = cat["premium"]
                    contract_cost = opt_premium * 100
                    target_funds = cash * allocation_pct
                    qty = int(target_funds // contract_cost)
                    
                    if qty > 0:
                        total_cost = qty * contract_cost
                        cash -= (total_cost + 1.00)
                        active_positions[ticker] = {
                            "qty": qty, 
                            "cost": opt_premium, 
                            "type": "options", 
                            "direction": cat["direction"], 
                            "entry_price": close_price, 
                            "high_rsi": False,
                            "exit_date": cat["exit_date"],
                            "exit_premium": cat["exit_premium"]
                        }
                        print(f"[{date_str}] BUY DYNAMIC OPTION: Bought {qty} {cat['direction']} contracts on {ticker} for catalyst: {cat['desc']}. Cost: ${total_cost:.2f}. Cash: ${cash:.2f}")
                        transaction_log.append({
                            "Date": date_str, "Action": f"BUY_{cat['direction']}_OPTION", "Ticker": ticker, "Qty": qty, "Price": opt_premium, "Remaining_Cash": cash
                        })
                
                # B. ETF Technical Swing Entry (Phase 1 & 2)
                elif is_etf and rsi < 35.0:
                    # Wisdom Sizing: In Phase 1 use 85% cash to compound. In Phase 2 use 90% cash to swing
                    allocation = 0.85 if phase == 1 else 0.90
                    target_funds = cash * allocation
                    qty = int(target_funds // close_price)
                    
                    if qty > 0:
                        cost = qty * close_price
                        commission = 1.00
                        # Commission Drag check in Phase 2
                        if phase == 2 and (commission / cost) > 0.005:
                            continue
                        cash -= (cost + commission)
                        active_positions[ticker] = {
                            "qty": qty, "cost": close_price, "type": "shares", "direction": "BUY", "entry_price": close_price, "high_rsi": False
                        }
                        print(f"[{date_str}] BUY SWING: Bought {qty} shares of ETF {ticker} at ${close_price:.2f} (RSI = {rsi:.1f}). Cash: ${cash:.2f}")
                        transaction_log.append({
                            "Date": date_str, "Action": "BUY_SHARES", "Ticker": ticker, "Qty": qty, "Price": close_price, "Remaining_Cash": cash
                        })

    # 4. Final Ledger Output
    final_val = cash
    for ticker, pos in active_positions.items():
        df = data_store[ticker]
        curr_close = df.loc[date_str, 'Close'] if date_str in df.index else df.iloc[-1]['Close']
        if pos["type"] == "shares":
            final_val += pos["qty"] * curr_close
        else:
            if date_str == pos["exit_date"]:
                final_val += pos["qty"] * 100 * pos["exit_premium"]
            else:
                pct_change = (curr_close - pos["entry_price"]) / pos["entry_price"]
                direction_multiplier = 1.0 if pos["direction"] == "CALL" else -1.0
                final_val += max(pos["qty"] * 100 * (pos["cost"] * (1 + pct_change * 5.0 * direction_multiplier)), 0.0)

    print("\n" + "=" * 95)
    print("   BACKTEST COMPLETED WITH WISDOM TRANSITION ENGINE")
    print("=" * 95)
    print(f"Final Account Balance (Cash): ${cash:.2f}")
    print(f"Total Wealth Extracted (Debt + Living): ${withdrawn_funds:.2f}")
    print(f"Ending Portfolio Net Assets: ${final_val:.2f}")
    print(f"Total Value Generated from $300: ${(final_val + withdrawn_funds):.2f} ({( (final_val + withdrawn_funds) / 300.00 - 1.0)*100:.1f}%)")
    print(f"Debt Paid Status: {debt_paid}")
    print(f"Total Trades Conducted: {len(transaction_log)}")
    print("=" * 95)

if __name__ == '__main__':
    run_backtest()
