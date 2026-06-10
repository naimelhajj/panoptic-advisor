# February 2021 Active Portfolio Simulation ($300 to >$2,000 Target)

This document details an active portfolio simulation from **February 1, 2021, to June 1, 2021**, starting with **$300** capital. The protagonist dynamically combines the three investment paths—Catalyst Option Arbitrage (Path 1), Micro-Cap Moat Cycles (Path 2), and Leveraged ETF Swing Trading (Path 3)—governed by the **First-Principles Bottleneck & Valuation (FPBV)** rules.

---

## 1. Starting Setup (February 1, 2021)
The market in early February 2021 was characterized by extreme retail-driven hype (the GameStop short squeeze peak had just occurred in late January) and tech indices trading at multi-decade high multiples. 

*   **Path 3 (3x Leveraged ETFs):** Avoided. TQQQ and SOXL are at near-all-time highs (daily RSI > 75). Entering here would violate the *Expectations Treadmill* rule.
*   **Path 2 (Micro-Cap Hype/Moat):** MVIS (Microvision) is identified as a high-momentum retail volume bottleneck. It trades at **$7.37** with a moderate daily RSI of **61.11**.
*   **Initial Allocation (Feb 1, 2021):**
    *   **Action:** Buy **30 shares of MVIS** at **$7.37** ($221.10 cost + $1.00 commission).
    *   **Cash Remaining:** **$77.90**
    *   **Total Portfolio Value:** **$299.00**

---

## 2. Step-by-Step Simulation Timeline

### **Step 1: The MVIS Momentum Harvest (Feb 1 – Feb 16, 2021)**
*   **Catalyst:** Retail momentum drives MVIS into a parabolic curve.
*   **Technical Trigger:** On **February 16, 2021**, MVIS closes at **$23.72**. The daily RSI hits **90.18** (extreme technical exhaustion).
*   **Action:** Sell all **30 shares of MVIS** at **$23.72** to capture the run before a correction.
    *   *Revenue:* $711.60 - $1.00 commission = **$710.60**.
    *   *New Cash Balance:* $77.90 + $710.60 = **$788.50**.
    *   *Return:* **+162.8%** in 11 trading days.

### **Step 2: The GME Capitulation Option Play (Feb 16 – Feb 25, 2021)**
*   **Catalyst:** After collapsing from its peak, GameStop (GME) undergoes severe consolidation. By **February 22, 2021**, GME settles at **$11.50** (split-adjusted, unadjusted ~$46.00). Daily RSI has cooled, and volume is extremely thin, suggesting seller exhaustion. This is a classic *Capitulation Buy* setup.
*   **Action (Path 1):** Buy **1 contract** of the GME March 12 $15 Call Option (unadjusted $60 Call) for **$1.00** split-adjusted ($100 contract premium + $1.00 commission).
    *   *Cost:* $101.00.
    *   *Cash Remaining:* **$687.50**.
*   **The Gamma Squeeze:** On February 24, GME surges over 100% in the final hour. On **February 25, 2021**, the stock closes at **$27.18**. The March 12 $15 Call is deep in-the-money (intrinsic value = $12.18), and implied volatility has spiked to historic levels, ballooning the option premium.
*   **Action:** Exit the option at the close of **February 25, 2021** at a premium of **$14.50** ($1,450.00 contract value - $1.00 commission).
    *   *Revenue:* **$1,449.00**.
    *   *New Cash Balance:* $687.50 + $1,449.00 = **$2,136.50**.
    *   *Target Achieved:* The account passes the $2,000 threshold within the first month.

### **Step 3: The Tech Correction 3x ETF swing (Feb 25 – Apr 16, 2021)**
*   **Catalyst:** High inflation fears trigger a deep Nasdaq tech correction. By **March 8, 2021**, indices bottom. 
    *   *SOXL Close:* **$26.69** (Daily RSI = 37.38).
    *   *TQQQ Close:* **$18.29** (Daily RSI = 33.19).
*   **Action (Path 3):** Re-allocate cash into diversified 3x Leveraged ETFs at the trough.
    *   *Buy 37 shares of SOXL:* Cost $987.47 + $1.00 commission.
    *   *Buy 27 shares of TQQQ:* Cost $493.85 + $1.00 commission.
    *   *Cash Remaining:* **$653.18**.
*   **The Rebound:** Indices recover. On **April 16, 2021**, tech reaches a short-term top.
    *   *SOXL Close:* **$41.48** (RSI = 55.74).
    *   *TQQQ Close:* **$26.70** (RSI = 66.86).
*   **Action:** Sell all ETF shares to avoid daily rebalancing volatility decay.
    *   *SOXL Revenue:* 37 * $41.48 - $1.00 commission = **$1,533.61**.
    *   *TQQQ Revenue:* 27 * $26.70 - $1.00 commission = **$719.85**.
    *   *New Cash Balance:* $653.18 + $1,533.61 + $719.85 = **$2,906.65**.

---

## 3. Final Portfolio Value (June 1, 2021)

*   **Holdings:** 100% Cash.
*   **Broker Deductions:** **$12.00** in Young Trader inactivity fees ($3.00/month for Feb, Mar, Apr, May).
*   **Net Portfolio Value (June 1, 2021):** **$2,894.65**
*   **Total Return on Capital:** **+864.88%** (a 9.6x increase in 4 months).

---

## 4. Black Box Autopsy: Critical Findings

1.  **Asymmetric Option Exploitation (Path 1):** 
    *   Buying OTM options *during* high-volatility hype cycles is a negative expected-value gamble due to over-priced implied volatility (IV crush). 
    *   *The Pivot:* Buying call options *after* a major collapse when volume dries up and volatility is suppressed (Capitulation/Consolidation) offers highly asymmetric leverage. A sudden volatility spike (Vega) and stock move (Delta) multiply the option value exponentially.
2.  **ETF Swing Discipline (Path 3):**
    *   Leveraged ETFs (SOXL, TQQQ) must never be held as long-term compounders in high-volatility sideways markets due to mathematical decay. They are strictly short-term tools to be entered when sector RSI is oversold (<35) and harvested when RSI approaches overbought (~65-70).
3.  **Active Sizing Constraints:**
    *   The protagonist correctly avoided putting 100% of the account into options. Keeping a cash buffer ($77.90 initially, and $687.50 during the GME play) ensured that if GME options had expired to $0, the core capital would have survived to fight another day.
