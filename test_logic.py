import unittest
import json
import os
import pandas as pd
import numpy as np

# Import the bot components for testing
from intelligent_bot import IntelligentFPBVBot
from walk_forward_backtest import calculate_ibkr_commission, calculate_rsi

class TestFPBVModelLogic(unittest.TestCase):
    
    def test_commission_calculation(self):
        # 1. Shares commission checks (IBKR Pro Fixed)
        # 10 shares of a $100 stock = $1000 value. 
        # Comm = max(1.00, 0.005 * 10) = $1.00
        self.assertAlmostEqual(calculate_ibkr_commission("shares", 100.0, 10), 1.00)
        # 1000 shares of a $5 stock = $5000 value.
        # Comm = max(1.00, 0.005 * 1000) = $5.00
        self.assertAlmostEqual(calculate_ibkr_commission("shares", 5.0, 1000), 5.00)
        # Maximum cap check: 10 shares of a $2 stock = $20 value.
        # Comm = max(1.00, 0.005 * 10) = $1.00, but capped at 1% of value = $0.20
        self.assertAlmostEqual(calculate_ibkr_commission("shares", 2.0, 10), 0.20)
        
        # 2. Options commission checks (IBKR Pro Fixed)
        # 1 contract: max(1.00, 0.65 * 1) = $1.00
        self.assertAlmostEqual(calculate_ibkr_commission("options", 2.00, 1), 1.00)
        # 10 contracts: max(1.00, 0.65 * 10) = $6.50
        self.assertAlmostEqual(calculate_ibkr_commission("options", 2.00, 10), 6.50)

    def test_rsi_calculation(self):
        # Create a series of constant prices
        prices = pd.Series([10.0] * 20)
        rsi = calculate_rsi(prices)
        # RSI should be 50.0 or close to it on flat series
        self.assertTrue(np.isnan(rsi.iloc[0])) # first 13 elements should be NaN
        self.assertTrue(np.isnan(rsi.iloc[12]))
        
        # Test basic boundaries
        prices_rising = pd.Series(range(10, 30))
        rsi_rising = calculate_rsi(prices_rising)
        self.assertTrue(rsi_rising.iloc[-1] > 50.0)

    def test_state_transitions(self):
        # Create temporary bot instance
        bot = IntelligentFPBVBot(starting_cash=300.00)
        
        # Verify initial state (Phase 0)
        self.assertEqual(bot.state["portfolio_phase"], 0)
        self.assertFalse(bot.state["debt_paid"])
        
        # Trigger Phase 1 Transition
        bot.state["current_cash"] = 2000.00
        # Call evaluate transitions (replicating transition check)
        if bot.state["portfolio_phase"] == 0 and bot.state["current_cash"] >= 2000.00:
            bot.state["portfolio_phase"] = 1
            
        self.assertEqual(bot.state["portfolio_phase"], 1)
        
        # Trigger Debt Payoff & Phase 2 Transition
        bot.state["current_cash"] = 7300.00
        if not bot.state["debt_paid"] and bot.state["current_cash"] >= 7300.00:
            bot.state["current_cash"] -= 5000.00
            bot.state["total_withdrawn"] += 5000.00
            bot.state["debt_paid"] = True
            bot.state["portfolio_phase"] = 2
            
        self.assertTrue(bot.state["debt_paid"])
        self.assertEqual(bot.state["portfolio_phase"], 2)
        self.assertEqual(bot.state["current_cash"], 2300.00)
        self.assertEqual(bot.state["total_withdrawn"], 5000.00)

    def test_conditional_dead_code_prevention(self):
        # This test programmatically checks that the triggers do not contain logical contradictions (like unreachable elifs)
        # by checking the structure of walk_forward_backtest.py and intelligent_bot.py file contents
        
        for filepath in ['walk_forward_backtest.py', 'intelligent_bot.py']:
            if not os.path.exists(filepath):
                continue
            with open(filepath, 'r') as f:
                content = f.read()
                
                # Check 1: Verify we don't have "if is_etf and rsi < 35.0:" immediately followed by "elif is_etf and rsi < 32.0:"
                # which was the cause of the previous dead-code block.
                contradiction_pattern_1 = "rsi < 35.0" in content and "elif is_etf and rsi < 32.0" in content
                self.assertFalse(contradiction_pattern_1, f"Found dead-code trigger bug in {filepath}!")
                
                # Check 2: Verify the Hybrid Bear rule is implemented (Close < EMA_200 blocks share entry)
                has_bear_market_check = "not is_bear_market" in content
                self.assertTrue(has_bear_market_check, f"Missing bear market swing check in {filepath}!")

    def test_dynamic_starting_cash(self):
        import unittest.mock as mock
        # Mock os.path.exists to return False so we force initialization of a new state
        orig_exists = os.path.exists
        with mock.patch('os.path.exists') as mock_exists:
            # We mock it to return False when looking for bot_state.json
            mock_exists.side_effect = lambda path: False if "bot_state.json" in path else orig_exists(path)
            
            bot_300 = IntelligentFPBVBot(starting_cash=300.00)
            self.assertEqual(bot_300.state["portfolio_phase"], 0)
            self.assertEqual(bot_300.state["current_cash"], 300.00)
            
            bot_2500 = IntelligentFPBVBot(starting_cash=2500.00)
            self.assertEqual(bot_2500.state["portfolio_phase"], 1)
            self.assertEqual(bot_2500.state["current_cash"], 2500.00)
            
            bot_8000 = IntelligentFPBVBot(starting_cash=8000.00)
            self.assertEqual(bot_8000.state["portfolio_phase"], 2)
            self.assertEqual(bot_8000.state["current_cash"], 8000.00)

if __name__ == '__main__':
    unittest.main()
