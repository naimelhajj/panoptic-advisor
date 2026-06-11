import json
import os
import sys
import time
from datetime import datetime
import pandas as pd
import yfinance as yf
from ib_insync import IB, Stock, Option, MarketOrder, LimitOrder, util

# Import the existing Intelligent Bot logic
sys.path.append('C:/development/stocks-finder')
from intelligent_bot import IntelligentFPBVBot

class IBKRPaperTrader(IntelligentFPBVBot):
    def __init__(self, port=7497, client_id=1):
        self.port = port
        self.client_id = client_id
        self.ib = IB()
        
        print("Connecting to IBKR...")
        try:
            self.ib.connect('127.0.0.1', self.port, clientId=self.client_id, timeout=10)
            print(f"Successfully connected to IBKR on port {self.port}!")
        except Exception as e:
            print(f"Failed to connect to IBKR: {e}")
            print("Please ensure TWS or IB Gateway is running, API is enabled, and the port is correct.")
            sys.exit(1)
            
        super().__init__()
        self.sync_state_with_broker()
        
    def sync_state_with_broker(self):
        """No longer overriding local cash with IBKR NetLiquidation. Bot will strictly follow its internal $300 virtual balance logic."""
        pass

    def get_last_price(self, contract):
        self.ib.qualifyContracts(contract)
        [ticker_data] = self.ib.reqTickers(contract)
        # Fallback if live data isn't subscribed
        if ticker_data.last != ticker_data.last: # Check for NaN
             return ticker_data.close
        return ticker_data.last or ticker_data.close

    def get_yfinance_call_option(self, ticker, close_price, max_premium, target_days_out=7):
        try:
            stock = yf.Ticker(ticker)
            exp_dates = stock.options
            if not exp_dates: return None
            
            target_dt = datetime.now().date() + pd.Timedelta(days=target_days_out)
            target_date = exp_dates[0]
            for d in exp_dates:
                if datetime.strptime(d, "%Y-%m-%d").date() >= target_dt:
                    target_date = d
                    break
                    
            chain = stock.option_chain(target_date)
            opts = chain.calls
            otm_opts = opts[opts['strike'] >= close_price].sort_values(by='strike')
            if otm_opts.empty: return None
            
            affordable_opts = otm_opts[otm_opts['lastPrice'] <= max_premium]
            if affordable_opts.empty: return None
            
            best_opt = affordable_opts.iloc[0]
            return {
                "strike": float(best_opt['strike']),
                "expiration": target_date.replace("-", ""), # format: YYYYMMDD
                "premium": float(best_opt['lastPrice'])
            }
        except Exception as e:
            print(f"Error fetching options for {ticker}: {e}")
            return None

    def execute_trades(self, candidates):
        """Overrides the local execution to send real orders to IBKR"""
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
                allocation = 0.85 if phase < 2 else 0.90
                target_funds = cash * allocation
                qty = int(target_funds // close_price)
                
                if qty > 0:
                    cost = qty * close_price
                    commission = self.calculate_commission("shares", close_price, qty, ticker)
                    
                    if phase == 2 and (commission / cost) > 0.005:
                        print(f"TRADE BYPASSED: Commission drag too high for {ticker}")
                        continue
                        
                    print(f"\n>>> LIVE EXECUTE: Buy {qty} shares of {ticker} Limit Order")
                    contract = Stock(ticker, 'SMART', 'USD')
                    self.ib.qualifyContracts(contract)
                    
                    # Using a safe limit order slightly above close to prevent slippage
                    limit_price = round(close_price * 1.005, 2) 
                    order = LimitOrder('BUY', qty, limit_price)
                    
                    trade = self.ib.placeOrder(contract, order)
                    print(f"Order Placed: {trade}")
                    
                    self.state["current_cash"] -= (cost + commission)
                    self.state["active_positions"][ticker] = {
                        "qty": qty,
                        "cost_basis": close_price,
                        "entry_date": datetime.today().strftime('%Y-%m-%d'),
                        "type": "shares",
                        "high_rsi": False
                    }
                    self.save_state()
                    break 

            elif c["Signal"] == "BUY_CALL_OPTION" and cash >= 100.00:
                if phase == 0:
                    max_premium = (cash * 0.95) / 100.0 # Phase 0 allows betting most of the cash on 1 contract
                else:
                    max_premium = (cash * 0.40) / 100.0
                
                opt_data = self.get_yfinance_call_option(ticker, close_price, max_premium)
                if not opt_data:
                    print(f"TRADE BYPASSED: Could not find affordable Call Option for {ticker} under ${max_premium:.2f} premium.")
                    continue
                
                est_premium = opt_data["premium"]
                contract_cost = est_premium * 100
                
                if phase == 0:
                    qty = 1
                else:
                    target_funds = cash * 0.40
                    qty = int(target_funds // contract_cost)
                    if qty == 0:
                        qty = 1
                        
                total_cost = qty * contract_cost
                comm = self.calculate_commission("options", est_premium, qty, ticker)
                
                if cash >= (total_cost + comm):
                    print(f"\n>>> LIVE EXECUTE: Buy {qty} Call contracts on {ticker} Limit Order (Strike: ${opt_data['strike']}, Exp: {opt_data['expiration']})")
                    
                    contract = Option(ticker, opt_data["expiration"], 'C', opt_data["strike"], 'SMART', 'USD')
                    self.ib.qualifyContracts(contract)
                    
                    limit_price = round(est_premium * 1.05, 2)
                    order = LimitOrder('BUY', qty, limit_price)
                    
                    trade = self.ib.placeOrder(contract, order)
                    print(f"Order Placed: {trade}")
                    
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
                    print(f"\n>>> LIVE EXECUTE: Sell {qty} shares of {ticker} Limit Order")
                    contract = Stock(ticker, 'SMART', 'USD')
                    self.ib.qualifyContracts(contract)
                    
                    limit_price = round(close_price * 0.995, 2) 
                    order = LimitOrder('SELL', qty, limit_price)
                    trade = self.ib.placeOrder(contract, order)
                    print(f"Order Placed: {trade}")
                    
                    revenue = qty * close_price
                    comm = self.calculate_commission("shares", close_price, qty, ticker)
                    self.state["current_cash"] += (revenue - comm)
                    del self.state["active_positions"][ticker]
                    self.save_state()
                    break

        print("\nPaper trading execution sweep complete.")

if __name__ == '__main__':
    bot = IBKRPaperTrader()
    bot.evaluate_signals()
