import json
import os
import sys
import time
from datetime import datetime
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
        """Overrides the local cash balance with the actual IBKR NetLiquidation value"""
        account_summary = self.ib.accountSummary()
        net_liq = self.state.get("current_cash", 300.0) # default fallback
        
        for item in account_summary:
            if item.tag == 'NetLiquidation':
                net_liq = float(item.value)
                break
                
        print(f"[IBKR Sync] Live Account Net Liquidation: ${net_liq:.2f}")
        self.state["current_cash"] = net_liq
        
        # In a full implementation, we would also sync self.state["active_positions"]
        # with self.ib.positions() to ensure accuracy.
        self.save_state()

    def get_last_price(self, contract):
        self.ib.qualifyContracts(contract)
        [ticker_data] = self.ib.reqTickers(contract)
        # Fallback if live data isn't subscribed
        if ticker_data.last != ticker_data.last: # Check for NaN
             return ticker_data.close
        return ticker_data.last or ticker_data.close

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
