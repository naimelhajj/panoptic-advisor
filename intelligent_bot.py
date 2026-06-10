import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
import time
from datetime import datetime

STATE_FILE = 'C:/development/stocks-finder/bot_state.json'
WATCHLIST_PATH = 'C:/development/stocks-finder/watchlist.json'

class IntelligentFPBVBot:
    def __init__(self, starting_cash=300.00):
        self.watchlist = self.load_watchlist()
        self.state = self.load_state(starting_cash)
        self.catalysts = self.load_catalysts()
        
    def load_watchlist(self):
        if not os.path.exists(WATCHLIST_PATH):
            print(f"Error: watchlist.json not found at {WATCHLIST_PATH}.")
            return {}
        with open(WATCHLIST_PATH, 'r') as f:
            return json.load(f)

    def load_catalysts(self):
        catalysts_path = 'C:/development/stocks-finder/upcoming_catalysts.json'
        if os.path.exists(catalysts_path):
            try:
                with open(catalysts_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def load_state(self, starting_cash):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                # Ensure portfolio_phase defaults to 0 if not present or legacy 1
                if "portfolio_phase" not in state or state["portfolio_phase"] == 1 and not state.get("debt_paid", False):
                    state["portfolio_phase"] = 0
                return state
                
        # Determine initial phase dynamically based on starting cash
        if starting_cash >= 7300.00:
            init_phase = 2
        elif starting_cash >= 2000.00:
            init_phase = 1
        else:
            init_phase = 0
            
        return {
            "portfolio_phase": init_phase,          # Phase 0 = Ramp-Up ($300 to $2k), Phase 1 = Debt Payoff ($2k to $7.3k), Phase 2 = Swing
            "current_cash": starting_cash,
            "debt_paid": False,
            "total_withdrawn": 0.00,
            "active_positions": {},        # format: {ticker: {"qty": X, "cost_basis": Z, "entry_date": Y, "type": "shares/options", "high_rsi": False}}
            "transaction_log": []
        }

    def save_state(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=4)

    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / (loss + 1e-10)
        return 100 - (100 / (1 + rs))

    def calculate_commission(self, trade_type, price, qty, ticker=""):
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


    def evaluate_signals(self):
        phase = self.state["portfolio_phase"]
        cash = self.state["current_cash"]
        
        print("\n" + "=" * 115)
        print(f"    INTELLIGENT FPBV BOT SCAN: PHASE {phase} | CASH: ${cash:.2f} | DEBT PAID: {self.state['debt_paid']}")
        print("=" * 115)
        
        # --- PHASE TRANSITION CHECKS ---
        if phase == 0 and cash >= 2000.00:
            phase = 1
            self.state["portfolio_phase"] = 1
            print(f">>> PHASE TRANSITION: Cash reached ${cash:.2f}. Graduating to Phase 1 (Standard Options Sizing).")
            self.save_state()
            
        if not self.state["debt_paid"] and cash >= 7300.00:
            self.state["current_cash"] -= 5000.00
            self.state["total_withdrawn"] += 5000.00
            self.state["debt_paid"] = True
            phase = 2
            self.state["portfolio_phase"] = 2
            print(f">>> DEBT PAYOFF MILESTONE: Paid $5,000.00. Remaining Cash: ${self.state['current_cash']:.2f}. Phase 2 Swing Active.")
            self.save_state()
            
        # Handle Phase 2 withdrawals
        if phase == 2:
            today_month = datetime.today().month
            last_with = self.state.get("last_withdrawal_month", None)
            if last_with is None or last_with != today_month:
                if self.state["current_cash"] >= 2500.00: # Capped safe withdrawal floor
                    self.state["current_cash"] -= 500.00
                    self.state["total_withdrawn"] += 500.00
                    self.state["last_withdrawal_month"] = today_month
                    print(f">>> P2 LIVING WITHDRAWAL: Extracted $500.00. Cash: ${self.state['current_cash']:.2f}")
                    self.save_state()

        # Download technicals for watchlist
        candidates = []
        for ticker, details in self.watchlist.items():
            try:
                stock = yf.Ticker(ticker)
                df = stock.history(period="120d")
                if df.empty or len(df) < 30:
                    continue
                    
                info = stock.info
                short_percent = info.get('shortPercentOfFloat', 0.0)
                if short_percent is None:
                    short_percent = 0.0
                    
                df['RSI'] = self.calculate_rsi(df['Close'])
                df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
                df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
                
                latest = df.iloc[-1]
                close_price = float(latest['Close'])
                rsi = float(latest['RSI'])
                ema_20 = float(latest['EMA_20'])
                ema_200 = float(latest['EMA_200'])
                
                is_etf = details.get('Type') == 'ETF'
                is_bear_market = close_price < ema_200
                
                signal = "HOLD"
                action_desc = "No trade setup."
                
                # Check active positions exits first
                if ticker in self.state["active_positions"]:
                    pos = self.state["active_positions"][ticker]
                    sell_trigger = False
                    
                    # Systemic Crash Easing
                    if rsi < 20.0 and is_etf:
                        pos["systemic_hold"] = True
                        pos["systemic_hold_counter"] = 30
                        
                    if pos.get("systemic_hold", False):
                        pos["systemic_hold_counter"] = pos.get("systemic_hold_counter", 30) - 1
                        if pos["systemic_hold_counter"] <= 0:
                            pos["systemic_hold"] = False
                            
                    # Exit Targets
                    target_rsi = 70.0 if pos["type"] == "shares" else 75.0
                    if is_bear_market and pos["type"] == "shares":
                        target_rsi = 55.0 # Bear market early target
                        
                    if rsi >= target_rsi:
                        pos["high_rsi"] = True
                        
                    # Exit conditions
                    if pos["type"] == "shares":
                        if rsi > target_rsi:
                            # RSI Reset Profit Guard: Only exit on RSI overbought if in profit
                            if close_price >= pos["cost_basis"]:
                                sell_trigger = True
                                action_desc = f"RSI Overbought Target reached ({rsi:.1f}) in profit."
                        elif pos.get("high_rsi", False) and not pos.get("systemic_hold", False) and close_price < ema_20:
                            sell_trigger = True
                            action_desc = f"Trailing Stop: Crossed below 20 EMA (${ema_20:.2f})."
                            
                    elif pos["type"] == "options":
                        # Options exit on target hits or time decay triggers
                        if rsi > target_rsi:
                            sell_trigger = True
                            action_desc = "Options Exit: overbought target reached."
                            
                    if sell_trigger:
                        signal = "SELL_EXIT"
                        
                else:
                    # Check entries based on Phase
                    if phase == 0:
                        # Phase 0: Capped Sizing & Index ETFs Focus
                        if is_etf and rsi < 35.0:
                            # Option first if bull and cash permits
                            est_premium = close_price * 0.05
                            contract_cost = est_premium * 100
                            if not is_bear_market and cash >= (contract_cost + 1.00):
                                signal = "BUY_CALL_OPTION"
                                action_desc = f"Phase 0 ETF Option: oversold ({rsi:.1f}). Buy exactly 1 contract Call."
                            else:
                                # Fallback to shares if bull
                                if not is_bear_market:
                                    signal = "BUY_SHARES"
                                    action_desc = f"Phase 0 ETF Swing Fallback: RSI oversold ({rsi:.1f}). Buy ETF shares."
                                    
                    elif phase == 1:
                        # Phase 1: High-Asymmetry
                        if is_etf and rsi < 35.0:
                            # Block ETF swings in bear market to preserve cash buffer for options
                            if not is_bear_market:
                                signal = "BUY_SHARES"
                                action_desc = f"Phase 1 ETF Swing: RSI oversold ({rsi:.1f}). Buy ETF shares."
                        elif not is_etf and rsi < 30.0:
                            if ticker in self.catalysts:
                                cat = self.catalysts[ticker]
                                if short_percent >= 0.10:
                                    signal = "BUY_CALL_OPTION"
                                    action_desc = f"Phase 1 Catalyst Option: oversold ({rsi:.1f}), high short ({short_percent*100:.1f}%) with upcoming earnings on {cat['earnings_date']}."
                                else:
                                    action_desc = f"Oversold stock ({rsi:.1f}) bypassed: short interest too low ({short_percent*100:.1f}% < 10%) for squeeze."
                            else:
                                action_desc = f"Oversold stock ({rsi:.1f}) bypassed: no upcoming earnings catalyst in catalysts database."
                            
                    elif phase == 2:
                        # Phase 2: Safe swing ETFs only (always allowed, even in bear markets)
                        if is_etf and rsi < 35.0:
                            signal = "BUY_SHARES"
                            action_desc = f"Phase 2 Safe ETF Swing: RSI oversold ({rsi:.1f}). Buy ETF shares."
                
                candidates.append({
                    "Ticker": ticker,
                    "Close": close_price,
                    "RSI_14": rsi,
                    "EMA_20": ema_20,
                    "Signal": signal,
                    "Action_Details": action_desc,
                    "Type": details.get('Type', 'Stock'),
                    "Thesis": details.get('Thesis', '')
                })
                
            except Exception as e:
                print(f"Error scanning {ticker}: {str(e)}")
                
        self.execute_trades(candidates)

    def execute_trades(self, candidates):
        print("\n" + "=" * 115)
        print(f"{'Ticker':<8} | {'Close':<8} | {'RSI':<6} | {'EMA_20':<8} | {'Signal':<15} | {'Trade Details'}")
        print("-" * 115)
        for c in candidates:
            print(f"{c['Ticker']:<8} | ${c['Close']:<7.2f} | {c['RSI_14']:<6.1f} | ${c['EMA_20']:<7.2f} | {c['Signal']:<15} | {c['Action_Details']}")
        print("=" * 115)
        
        phase = self.state["portfolio_phase"]
        cash = self.state["current_cash"]
        
        for c in candidates:
            ticker = c["Ticker"]
            close_price = c["Close"]
            
            if c["Signal"] == "BUY_SHARES" and cash >= 50.00:
                # Sizing allocation: 85% cash in P0/P1, 90% cash in P2
                allocation = 0.85 if phase < 2 else 0.90
                target_funds = cash * allocation
                qty = int(target_funds // close_price)
                
                if qty > 0:
                    cost = qty * close_price
                    commission = self.calculate_commission("shares", close_price, qty, ticker)

                    
                    # Commission Drag filter in Phase 2
                    if phase == 2 and (commission / cost) > 0.005:
                        print(f"TRADE BYPASSED: Commission drag too high for {ticker}")
                        continue
                        
                    print(f"\n>>> EXECUTE: Buy {qty} shares of {ticker} @ ${close_price:.2f} (Total: ${cost:.2f} + ${commission:.2f} fee)")
                    self.state["current_cash"] -= (cost + commission)
                    self.state["active_positions"][ticker] = {
                        "qty": qty,
                        "cost_basis": close_price,
                        "entry_date": datetime.today().strftime('%Y-%m-%d'),
                        "type": "shares",
                        "high_rsi": False
                    }
                    self.save_state()
                    break # Single trade focus
                    
            elif c["Signal"] == "BUY_CALL_OPTION" and cash >= 100.00:
                est_premium = close_price * 0.05
                contract_cost = est_premium * 100
                
                # Sizing constraints based on Phase
                if phase == 0:
                    qty = 1 # Strictly capped at exactly 1 contract max in Phase 0
                else:
                    target_funds = cash * 0.40
                    qty = int(target_funds // contract_cost)
                    if qty == 0:
                        qty = 1
                        
                total_cost = qty * contract_cost
                comm = self.calculate_commission("options", est_premium, qty, ticker)

                
                if cash >= (total_cost + comm):
                    print(f"\n>>> EXECUTE: Buy {qty} call contracts on {ticker} @ estimated premium ${est_premium:.2f} (Total: ${total_cost:.2f} + ${comm:.2f} fee)")
                    self.state["current_cash"] -= (total_cost + comm)
                    self.state["active_positions"][ticker] = {
                        "qty": qty,
                        "cost_basis": est_premium,
                        "entry_date": datetime.today().strftime('%Y-%m-%d'),
                        "type": "options",
                        "high_rsi": False
                    }
                    self.save_state()
                    break
                    
            elif c["Signal"] == "SELL_EXIT":
                pos = self.state["active_positions"][ticker]
                qty = pos["qty"]
                
                if pos["type"] == "shares":
                    revenue = qty * close_price
                    comm = self.calculate_commission("shares", close_price, qty, ticker)
                else:
                    # Estimate options close value
                    revenue = qty * 100 * (close_price * 0.05)
                    comm = self.calculate_commission("options", close_price * 0.05, qty, ticker)

                    
                print(f"\n>>> EXECUTE: Sell {qty} {pos['type']} of {ticker} @ ${close_price:.2f} (Est. Revenue: ${revenue:.2f} - ${comm:.2f} fee)")
                self.state["current_cash"] += (revenue - comm)
                del self.state["active_positions"][ticker]
                self.save_state()
                break

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="FPBV Model v3.2 Intelligent Trading Bot")
    parser.add_argument("--starting-cash", type=float, default=300.00, help="Initial cash for bot state if no state file exists (default: 300.00)")
    parser.add_argument("--reset-state", action="store_true", help="Reset/Overwrite state file with starting cash")
    args = parser.parse_args()
    
    if args.reset_state and os.path.exists(STATE_FILE):
        print(f"Resetting bot state. Deleting {STATE_FILE}...")
        try:
            os.remove(STATE_FILE)
        except Exception as e:
            print(f"Error deleting state file: {e}")
            
    bot = IntelligentFPBVBot(starting_cash=args.starting_cash)
    bot.evaluate_signals()
