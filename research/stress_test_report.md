# Stateful Portfolio Bot Stress Test Report
Generated on: 2026-06-01 21:49:51

This report documents the performance of the **Stateful Portfolio Journey Bot** under various stressed macro environments, asset universes, capital levels, and commission friction rates.

## Test Suite 1: Extreme Macro Regimes
Tests bot resilience across historical bear markets, panic events, bubbles, and carry-trade liquidations. (Starting Cash: $300, Commission: $1.00, Universe: Full)

| Macro Regime | Start Date | End Date | Ending Value | Return (%) | Debt Paid | Trades |
| --- | --- | --- | --- | --- | --- | --- |
| COVID Panic Crash | 2020-02-15 | 2020-04-30 | $1619.77 | +439.9% | False | 8 |
| 2022 Bear Bottom Capitulation | 2022-08-15 | 2022-10-31 | $203.27 | -32.2% | False | 4 |
| 2022 Year-Long Inflation Bear | 2022-01-01 | 2022-12-31 | $3770.68 | +1156.9% | False | 22 |
| 2021 Meme Stock Mania Squeeze | 2020-12-01 | 2021-06-30 | $4553.25 | +1417.8% | False | 12 |
| AI Parabolic Blowoff | 2024-01-01 | 2024-03-31 | $16517.36 | +5405.8% | False | 5 |
| Carry-Trade Unwind Shock | 2024-07-10 | 2024-08-31 | $266.52 | -11.2% | False | 4 |
| 2025 AI Peak & Multiple De-Rating | 2025-06-01 | 2025-10-31 | $396.70 | +32.2% | False | 4 |
| 2019 Quiet Growth Era | 2019-01-01 | 2019-12-31 | $2812.42 | +837.5% | False | 20 |

## Test Suite 2: Ticker Watchlist Segments
Tests the effect of restricting the bot's asset universe to specific styles. (Timeframe: July 2023 - June 2024, Starting Cash: $300, Commission: $1.00)

| Watchlist Segment | Tickers included | Ending Value | Return (%) | Debt Paid | Trades |
| --- | --- | --- | --- | --- | --- |
| Full Universe | `SOXL, TQQQ, SMCI, NVDA, AVGO, ENPH, RYCEY, GME, MVIS` | $6189.40 | +1963.1% | True | 17 |
| Index ETFs Only | `SOXL, TQQQ` | $347.72 | +15.9% | False | 12 |
| AI/Semi Moat Leaders Only | `SMCI, NVDA, AVGO` | $3846.00 | +1182.0% | False | 4 |
| Value & Turnarounds (Non-Tech) | `ENPH, RYCEY` | $1148.00 | +282.7% | False | 2 |
| Speculative Squeezes Only | `GME, MVIS` | $300.00 | +0.0% | False | 0 |

## Test Suite 3: Account Capital Sizing & Ruin Boundaries
Finds the minimum viable budget where flat transaction commissions don't lead to fee-drag ruin. (Timeframe: July 2023 - June 2024, Commission: $1.00, Universe: Full)

| Starting Capital | Ending Value | Net Return | Return (%) | Debt Paid | Trades | Status / Ruin Risk |
| --- | --- | --- | --- | --- | --- | --- |
| $30.00 | $28.37 | -1.63 | -5.4% | False | 2 | Ruin / Commission Stagnation |
| $50.00 | $52.23 | +2.23 | +4.5% | False | 8 | Ruin / Commission Stagnation |
| $75.00 | $84.97 | +9.97 | +13.3% | False | 10 | Ruin / Commission Stagnation |
| $100.00 | $116.61 | +16.61 | +16.6% | False | 8 | Low Growth compounding |
| $200.00 | $226.10 | +26.10 | +13.1% | False | 12 | Ruin / Commission Stagnation |
| $300.00 | $6189.40 | +5889.40 | +1963.1% | True | 17 | Success (Debt Paid) |
| $500.00 | $5536.15 | +5036.15 | +1007.2% | True | 17 | Success (Debt Paid) |
| $1000.00 | $8362.76 | +7362.76 | +736.3% | True | 15 | Success (Debt Paid) |

## Test Suite 4: Broker Friction & Commission Rates
Tests the sensitivity of the bot to flat commissions. (Timeframe: July 2023 - June 2024, Starting Cash: $300, Universe: Full)

| Commission / Side | Ending Value | Return (%) | Debt Paid | Trades | Performance Impact |
| --- | --- | --- | --- | --- | --- |
| $0.00 | $6212.43 | +1970.8% | True | 17 | Baseline (0% Drag) |
| $0.50 | $6203.43 | +1967.8% | True | 17 | -$9.00 drag (3.0% of starting capital) |
| $1.00 | $6189.40 | +1963.1% | True | 17 | -$23.04 drag (7.7% of starting capital) |
| $2.00 | $6170.96 | +1957.0% | True | 17 | -$41.48 drag (13.8% of starting capital) |
| $5.00 | $5360.64 | +1686.9% | True | 17 | -$851.79 drag (283.9% of starting capital) |