# Interactive Brokers May 2017 Investment Simulation ($200 Capital)

This document simulates an investment of **$200** on Interactive Brokers (IBKR) starting in **May 2017**, evaluating structural broker constraints, stock affordability (no fractional shares), and actual historical returns by May 2018 (1-year) and May 2021 (4-year).

---

## 1. IBKR Structural Constraints (As of May 2017)

Before selecting any stocks, a veteran trader must navigate three severe structural constraints on IBKR in May 2017:

1.  **No Fractional Shares:** IBKR did not launch fractional share trading until **November 2019**. The investor can only buy whole shares of stocks. This immediately excludes companies trading above $200 (such as Amazon at ~$950, Alphabet at ~$930, or Tesla at ~$320).
2.  **Inactivity Fees:** In 2017, IBKR charged a **$10/month inactivity fee** for accounts with balances under $10,000. For a $200 account, this fee would consume $120/year (60% of capital), destroying any passive return. 
    *   *The Pivot:* To survive, the investor must qualify for a **Young Trader / Student Account** (under 26 years old), which reduced the inactivity fee to **$3/month** ($36/year).
3.  **Minimum Initial Deposit:** While IBKR historically required a $10,000 minimum deposit, young trader accounts were approved with a $3,000 minimum. We assume a cash account waiver is granted for this $200 simulation.
4.  **Commissions:** IBKR charged a minimum of **$1.00 per trade** in commissions.

---

## 2. Selection & Nominal Prices (May 1, 2017)

Applying our **First-Principles Bottleneck & Valuation (FPBV)** model, we screen for affordable, high-moat bottleneck assets:

| Ticker | Split-Adjusted Close (2017) | Split Factor (2017-2024) | **Nominal (Unadjusted) Close** | First-Principles Moat (May 2017) |
| --- | --- | --- | --- | --- |
| **NVDA** | $2.63 | 40x (4-for-1, 10-for-1) | **$105.18** | GPU supply bottleneck driven by the Ethereum mining boom and early deep learning AI. |
| **SHOP** | $7.73 | 10x (10-for-1) | **$77.26** | E-commerce merchant storefront bottleneck. Growth >70% YoY. |
| **AMD** | $13.62 | 1x | **$13.62** | Just launched Zen "Ryzen" CPU architecture, challenging Intel's CPU monopoly. |
| **MU** | $27.59 | 1x | **$27.59** | Oligopolistic DRAM memory cycle in structural upswing. |

### **The May 2017 Portfolio Allocation**
To fully allocate the $200 in whole shares, the optimal combination of bottleneck assets is:
*   **1 Share of NVIDIA (NVDA):** Cost = **$105.18**
*   **1 Share of Shopify (SHOP):** Cost = **$77.26**
*   **1 Share of AMD:** Cost = **$13.62**
*   **Total Capital Invested:** **$196.06**
*   **Remaining Cash (for commissions):** **$3.94** (Covers $3.00 for the 3 buy trades).

---

## 3. Realized Returns: What Happened Next?

### **1-Year Performance (May 2017 - May 2018)**
By May 1, 2018, the stock prices evolved as follows:
*   **NVIDIA (NVDA):** Rose from $105.18 to **$224.80** (+113.69% | +$119.62 gain).
*   **Shopify (SHOP):** Rose from $77.26 to **$127.70** (+65.26% | +$50.44 gain).
*   **AMD:** Fell from $13.62 to **$11.13** (-18.28% | -$2.49 loss).
*   **Total Portfolio Value (May 2018):** **$363.63** (Gross return: **+85.47%**).
*   **Net Account Size (after $36 Young Trader inactivity fees):** **$327.63** (Net return: **+63.81%**).

### **4-Year Performance (May 2017 - May 2021)**
By May 2021, the structural compounding of the bottlenecks became apparent:
*   **NVIDIA (NVDA):** Rose to **$592.00** (+$486.82 gain).
*   **Shopify (SHOP):** Rose to **$1,122.00** (+$1,044.74 gain).
*   **AMD:** Rose to **$78.55** (+$64.93 gain).
*   **Total Portfolio Value (May 2021):** **$1,792.55** (Gross return: **+814.29%**).
*   **Net Account Size (after $144 Young Trader inactivity fees):** **$1,648.55** (Net return: **+724.27%**).

---

## 4. Black Box Lessons: The Small Account Paradox
1.  **The Drag of Fixed Fees:** In a small account ($200), structural fixed broker fees (commissions and inactivity fees) act as a massive drag on returns. A standard account paying $10/month would have lost 60% of its capital in fees in Year 1. Minimizing structural fees is as important as picking the right stocks.
2.  **Whole Share Concentration:** When fractional shares are unavailable, position sizing is dictated by nominal share price rather than portfolio theory. Concentration in a single high-conviction unit (like NVDA at $105) is the only path to meaningful capital growth.
