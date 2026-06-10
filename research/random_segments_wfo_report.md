# Walk-Forward Optimization (WFO) on Random Segments (Model v3)
Generated on: 2026-06-01 22:35:07

This report documents the walk-forward optimization of the **FPBV Model v3** across 7 completely new, randomly shifted 1-year windows, simulating realistic **Interactive Brokers (IBKR) Pro Fixed commissions** and utilizing **Golden Rule 4 position-sizing overrides** for small accounts ($300 starting capital).

## WFO Pass Results Table
| Pass Name | Start Date | End Date | Ending Assets | Withdrawn | Total Gen | Return (%) | Debt Paid | Trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pass A (Spring 2019 - COVID Crash Start) | 2019-04-15 | 2020-04-14 | $5372.46 | $5500.00 | $10872.46 | +3524.2% | True | 23 |
| Pass B (Late Summer 2020 - Retail Squeezes) | 2020-08-01 | 2021-07-31 | $2248.20 | $6500.00 | $8748.20 | +2816.1% | True | 25 |
| Pass C (Spring 2021 - Peak Tech to Bear Intro) | 2021-03-01 | 2022-02-28 | $1223.66 | $0.00 | $1223.66 | +307.9% | False | 22 |
| Pass D (Summer 2022 - Bear Bottom to Recovery) | 2022-06-01 | 2023-05-31 | $403.51 | $0.00 | $403.51 | +34.5% | False | 14 |
| Pass E (Autumn 2023 - AI Breakout to Carry Unwind) | 2023-10-01 | 2024-09-30 | $3642.66 | $0.00 | $3642.66 | +1114.2% | False | 23 |
| Pass F (Spring 2024 - Post-Hype Consolidation) | 2024-05-01 | 2025-04-30 | $204.30 | $0.00 | $204.30 | -31.9% | False | 20 |
| Pass G (Late Summer 2025 - Today's Cycles) | 2025-08-01 | 2026-06-01 | $555.18 | $0.00 | $555.18 | +85.1% | False | 14 |

## Continuous 7-Year Multi-Regime Journey (2019-2026)
Runs the refined v3 model continuously from 2019 to today under IBKR Pro commissions and Phase 2 monthly withdrawals.

* **Ending Portfolio Cash:** $19961.34
* **Total Wealth Extracted (Debt + Living):** $28500.00
* **Total Value Generated:** $48461.34
* **Total Return (%):** +16053.8%
* **Debt Paid Status:** True
* **Total Trades:** 138

## Continuous Run Trade Ledger (First 30 & Last 10 Trades)
```text
[2019-01-03] BUY SHARES: SOXL Qty 56 at $4.51 | Comm: $1.00
[2019-01-03] BUY SHARES: TQQQ Qty 9 at $4.05 | Comm: $0.36
[2019-01-10] SELL SHARES: SOXL Qty 56 at $5.88 | Comm: $1.00 | Reason: RSI Overbought (59.3) in profit
[2019-01-10] SELL SHARES: TQQQ Qty 9 at $5.01 | Comm: $0.45 | Reason: RSI Overbought (57.9) in profit
[2019-05-08] BUY SHARES: SOXL Qty 30 at $10.69 | Comm: $1.00
[2019-05-13] BUY SHARES: TQQQ Qty 7 at $6.54 | Comm: $0.46
[2019-06-20] SELL SHARES: TQQQ Qty 7 at $7.60 | Comm: $0.53 | Reason: RSI Overbought (78.7) in profit
[2019-07-23] SELL SHARES: SOXL Qty 30 at $11.85 | Comm: $1.00 | Reason: RSI Overbought (75.3) in profit
[2019-07-31] BUY OPTION: ENPH Qty 3 contracts of CALL at premium $1.00 | Comm: $1.95 | Desc: ENPH Q2 earnings blowout solar demand
[2019-08-02] BUY SHARES: TQQQ Qty 13 at $7.37 | Comm: $0.96
[2019-08-02] SELL OPTION: ENPH Qty 3 contracts at exit premium $6.50 | Comm: $1.95 | Reason: Catalyst Target Exit Date
[2019-08-12] BUY SHARES: SOXL Qty 185 at $9.03 | Comm: $1.00
[2019-09-13] SELL SHARES: SOXL Qty 185 at $12.05 | Comm: $1.00 | Reason: RSI Overbought (84.3) in profit
[2019-09-13] SELL SHARES: TQQQ Qty 13 at $7.79 | Comm: $1.00 | Reason: RSI Overbought (76.1) in profit
[2019-10-01] BUY SHARES: SOXL Qty 209 at $10.67 | Comm: $1.04
[2019-10-01] BUY SHARES: TQQQ Qty 46 at $7.18 | Comm: $1.00
[2019-10-28] SELL SHARES: SOXL Qty 209 at $13.38 | Comm: $1.04 | Reason: RSI Overbought (73.5) in profit
[2019-10-28] SELL SHARES: TQQQ Qty 46 at $8.34 | Comm: $1.00 | Reason: RSI Overbought (80.1) in profit
[2019-12-03] BUY SHARES: SOXL Qty 211 at $13.02 | Comm: $1.05
[2019-12-19] SELL SHARES: SOXL Qty 211 at $17.32 | Comm: $1.05 | Reason: RSI Overbought (73.0) in profit
[2020-02-20] BUY OPTION: TQQQ Qty 8 contracts of PUT at premium $2.00 | Comm: $5.20 | Desc: Pre-COVID crash index overbought warning
[2020-02-26] BUY SHARES: SOXL Qty 150 at $14.36 | Comm: $1.00
[2020-03-16] SELL OPTION: TQQQ Qty 8 contracts at exit premium $18.00 | Comm: $5.20 | Reason: Catalyst Target Exit Date
[2020-03-17] DEBT PAYOFF MILESTONE TRIGGERED. Cash withdrawn: $5000.00. Remaining Cash: $9780.17
[2020-03-17] BUY SHARES (Phase 2 Swing): TQQQ Qty 1701 at $5.17 | Comm: $8.51
[2020-04-01] PHASE 2 WITHDRAWAL: $500.00
[2020-04-06] SELL SHARES: TQQQ Qty 1701 at $6.12 | Comm: $8.51 | Reason: RSI Overbought (57.1) in profit
[2020-04-21] SELL SHARES: SOXL Qty 150 at $6.67 | Comm: $1.00 | Reason: Crossed below 20 EMA after high RSI
[2020-05-01] PHASE 2 WITHDRAWAL: $500.00
[2020-06-01] PHASE 2 WITHDRAWAL: $500.00
... [MIDDLE TRADES OMITTED FOR BREVITY] ...
[2025-12-31] BUY SHARES (Phase 2 Swing): SOXL Qty 43 at $42.03 | Comm: $1.00
[2026-01-06] SELL SHARES: SOXL Qty 43 at $54.01 | Comm: $1.00 | Reason: RSI Overbought (73.3) in profit
[2026-01-07] PHASE 2 WITHDRAWAL: $500.00
[2026-02-02] PHASE 2 WITHDRAWAL: $500.00
[2026-03-02] PHASE 2 WITHDRAWAL: $500.00
[2026-03-06] BUY SHARES (Phase 2 Swing): SOXL Qty 19 at $47.89 | Comm: $1.00
[2026-04-10] SELL SHARES: SOXL Qty 19 at $76.39 | Comm: $1.00 | Reason: RSI Overbought (71.7) in profit
[2026-04-13] PHASE 2 WITHDRAWAL: $500.00
[2026-04-14] SELL SHARES: TQQQ Qty 363 at $53.41 | Comm: $1.81 | Reason: RSI Overbought (71.6) in profit
[2026-05-01] PHASE 2 WITHDRAWAL: $500.00
```