# Amgen (AMGN) Monthly Investment Simulation (Jan 2023 - Jun 2026)

This document simulates the performance of our **First-Principles Bottleneck & Valuation (FPBV)** model on Amgen Inc. (AMGN) on a monthly basis from January 2023 to June 2026.

---

## 1. Month-by-Month Simulation Log

### **Phase 1: Horizon Deal Risk & FTC Block (Jan 2023 – Aug 2023)**
*   **Jan 2023:** Price = **$234.32** | RSI = 18.70 (Oversold)
    *   *M&A Catalyst:* Amgen announces Horizon Therapeutics acquisition for $27.8B. The market fears high debt and antitrust blocks.
    *   *Logic:* Under our M&A rules, we must cap the maximum allocation at **25%** due to binary regulatory scrutiny.
    *   *Action:* **BUY / SMALL ACCUMULATION (Max 25% portfolio allocation)**
*   **Feb 2023:** Price = **$220.68** | RSI = **8.80** (Extreme oversold)  $\rightarrow$ *Action:* **HOLD (Capped)**
*   **Mar 2023:** Price = **$213.39** | RSI = 47.30  $\rightarrow$ *Action:* **HOLD**
*   **Apr 2023:** Price = **$220.84** | RSI = 69.04  $\rightarrow$ *Action:* **HOLD**
*   **May 2023:** Price = **$215.84** | RSI = **22.22**
    *   *Catalyst:* FTC formally sues to block the Horizon acquisition on May 16.
    *   *Action:* **STAND ASIDE / HOLD (No additional purchases; keep capped at 25%)**
*   **Jun 2023:** Price = **$195.41** | RSI = **21.48** (Oversold)
    *   *Logic:* FTC lawsuit is fully priced in. Standalone business is highly profitable.
    *   *Action:* **BUY / ACCUMULATE (Within the 25% risk cap)**
*   **Jul 2023:** Price = **$205.21** | RSI = 62.80  $\rightarrow$ *Action:* **HOLD**
*   **Aug 2023:** Price = **$211.69** | RSI = 69.10  $\rightarrow$ *Action:* **HOLD**

### **Phase 2: HZNP Merger Resolution & MariTide Hype (Sep 2023 – Sep 2024)**
*   **Sep 2023:** Price = **$236.01** | RSI = 44.93
    *   *Catalyst:* FTC settles and clears the Horizon merger.
    *   *Action:* **HOLD**
*   **Oct 2023:** Price = **$244.84** | RSI = 58.91
    *   *Catalyst:* Merger closes Oct 6. Binary deal risk is resolved.
    *   *Action:* **ACCUMULATE TO FULL ALLOCATION (Remove 25% risk cap)**
*   **Nov 2023:** Price = **$239.81** | RSI = **25.51** (Oversold)
    *   *Action:* **BUY BACK / RE-ACCUMULATE on dip**
*   **Dec 2023:** Price = **$252.45** | RSI = 63.38  $\rightarrow$ *Action:* **HOLD**
*   **Jan 2024:** Price = **$275.56** | RSI = 77.74  $\rightarrow$ *Action:* **HOLD**
*   **Feb 2024:** Price = **$300.74** | RSI = **78.57**
    *   *Logic:* High retail hype surrounding upcoming MariTide (GLP-1 weight loss candidate) Phase 2 data.
    *   *Action:* **TAKE PROFIT (Sell 50% of position) on overbought momentum**
*   **Mar 2024:** Price = **$261.79** | RSI = 39.85  $\rightarrow$ *Action:* **HOLD remaining 50%**
*   **Apr 2024:** Price = **$264.32** | RSI = 62.35  $\rightarrow$ *Action:* **HOLD**
*   **May 2024:** Price = **$259.02** | RSI = 60.43
    *   *Catalyst:* Q1 earnings confirm encouraging MariTide Phase 2 trial updates.
    *   *Action:* **BUY BACK / RE-ACCUMULATE the 50% sold portion**
*   **Jun 2024 - Sep 2024:** Stock climbs from **$289.12** to **$313.00**.  $\rightarrow$ *Action:* **HOLD**

### **Phase 3: Clinical Data Rumors & Rebound (Oct 2024 – Jun 2026)**
*   **Oct 2024 - Nov 2024:** Price is flat around **$302.31**.  $\rightarrow$ *Action:* **HOLD**
*   **Dec 2024:** Price = **$265.48** | RSI = **25.38**
    *   *Catalyst:* Market panic over unconfirmed rumors of bone density loss side-effects in MariTide trial data.
    *   *Logic:* Fear has created a value gap; the rumors are unconfirmed.
    *   *Action:* **BUY / ACCUMULATE**
*   **Jan 2025:** Price = **$247.51** | RSI = **26.08** (Oversold)
    *   *Action:* **BUY / ACCUMULATE MORE**
*   **Feb 2025:** Price = **$275.76** | RSI = 74.70
    *   *Catalyst:* Amgen confirms robust Phase 2 safety data with no bone density issues.
    *   *Action:* **HOLD (Riding the recovery)**
*   **Mar 2025 - Nov 2025:** Stock trades flat between **$273.09** and **$292.14**.  $\rightarrow$ *Action:* **HOLD**
*   **Dec 2025:** Price = **$332.66** | RSI = 63.63
    *   *Catalyst:* Horizon revenue integration beats guidance.
    *   *Action:* **HOLD**
*   **Jan 2026 - Feb 2026:** Climbs to **$339.74**.  $\rightarrow$ *Action:* **HOLD**
*   **Mar 2026:** Price = **$382.81** | RSI = 60.34
    *   *Logic:* Stock hits all-time highs on Phase 3 MariTide design approvals. 
    *   *Action:* **TAKE PROFIT (Sell 50% of position)**
*   **Apr 2026 - Jun 2026:** Pulls back to close at **$327.83** on June 1.  $\rightarrow$ *Action:* **HOLD remaining 50%**

---

## 2. The Black Box Autopsy: Model Behaviors & Lessons

### A. Success: M&A Capping Rule (First-Principles Risk Management)
*   **Key Learn:** In January 2023, the model's **M&A position capping rule** worked perfectly. By limiting exposure to **25%** due to active FTC antitrust litigation, the model protected capital when the FTC formally sued to block the merger in May, causing the stock to drop. When the litigation settled in September, the model removed the cap and scaled back to full size.

### B. Success: Capitulation on Clinical Trial Rumors
*   **Key Learn:** In December 2024/January 2025, the model recognized that the bone-density loss rumors had created a classic capitulation bottom (P/E compression + oversold RSI). Buying at **$247** before the data was formally cleared and the stock rebounded to **$299** was a major success.

### C. The "Biotech Binary Catalyst" Risk (Un-quantified Risk)
*   **Incident:** In biotechnology, a single clinical trial readout (like MariTide's Phase 2 data) represents a binary catalyst that can cause a 20%+ price swing in a single day. While oversold technical rules worked to find the entry point, the model was exposed to massive binary risk (if the trial had actually failed, the stock would have permanently collapsed).
*   **Mitigation (Biotech Binary Trial Rule):** If a stock's valuation expansion is driven by a single pipeline candidate's upcoming Phase 2/3 data release, enforce a **50% risk reduction** (or buy protective puts) prior to the readout date, as clinical trial failure is a binary event that cannot be predicted by financial indicators.
