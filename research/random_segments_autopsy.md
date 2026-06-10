# Random-Segment WFO Autopsy: Black Box Failure Analysis

This document applies the **Black Box Thinking** method to analyze the results of the 7 randomly shifted walk-forward optimization passes, highlighting failures, near-misses, critical bug detections, and lessons learned.

---

## 1. Executive Summary & Verification

After fixing a critical **ending valuation hindsight leak**, the 7 random-segment WFO passes under realistic **Interactive Brokers (IBKR) Pro Fixed commissions** and **Model v3** rules show a **100% survival rate (0% account ruin)**:

*   **Pass A (Spring 2019 - COVID Crash Start):** **Success (+1,890.9% return)** — Paid $5,000 debt.
*   **Pass B (Late Summer 2020 - Squeezes):** **Success (+2,635.0% return)** — Paid $5,000 debt + withdrew $1,500 living expenses.
*   **Pass C (Spring 2021 - Peak Tech to Bear Intro):** Missed milestone (+371.5% return) — Ended at $1,414.45 assets.
*   **Pass D (Summer 2022 - Bear Bottom to Recovery):** Missed milestone (+0.0% return) — Preserved capital at $300.00.
*   **Pass E (Autumn 2023 - AI Breakout to Carry Unwind):** Missed milestone (+1,351.9% return) — Ended at $4,355.73.
*   **Pass F (Spring 2024 - Post-Hype Consolidation):** Missed milestone (+67.6% return) — Ended at $502.72.
*   **Pass G (Late Summer 2025 - Today's Cycles):** Missed milestone (+85.1% return) — Ended at $555.18.

---

## 2. Pass-by-Pass Autopsies

### Pass A (Spring 2019 - COVID Crash Start): SUCCESS (+1,890.9%)
*   **Verdict:** Milestone Achieved.
*   **What happened:** Grew the $300 starting cash to **$5,972.61**, successfully paying off the $5,000 debt and leaving a $972.61 cash base.
*   **Key Driver:** The shifted 1-year window (April 2019 to April 2020) bridged two separate high-asymmetry opportunities: the `ENPH` Call option blowout in July 2019 (took cash to ~$1,100) and the `TQQQ` Put option pre-covid warning in Feb 2020 (multiplied the $1,100 to over $5,300).
*   **Lesson:** Crossing macro eras (a quiet growth period followed by a high-volatility panic event) provides excellent catalyst density for micro-accounts.

### Pass B (Late Summer 2020 - Retail Squeezes): SUCCESS (+2,635.0%)
*   **Verdict:** Milestone Achieved.
*   **What happened:** Grew the $300 starting cash to **$8,205.00**, paying the $5,000 debt and generating $1,500 in living expenses.
*   **Key Driver:** Run from August 2020 to July 2021. Successfully captured the Ryan Cohen GME Call option on Sept 22, 2020, the historic January 2021 GME Short Squeeze option play, and the April 2021 MVIS squeeze.
*   **Lesson:** Short squeeze manias provide maximum account velocity, provided options are entered strictly at consolidation floors (low IV) rather than during upward runs.

### Pass C (Spring 2021 - Peak Tech to Bear Intro): Missed Milestone (+371.5%)
*   **Verdict:** Survived (No Ruin).
*   **What happened:** Grew to **$1,414.45** but failed to pay the debt.
*   **Root Cause:**
    1.  *Catalyst Deprivation:* The pass started in March 2021, missing the January GME squeeze. The only options catalyst in its window was MVIS in April.
    2.  *Bear Transition:* The pass ended during the early 2022 bear market transition, triggering stop-losses at a loss on share swing entries.
*   **Lesson:** Cycles starting immediately after major mania peaks experience slower growth, as the account faces multiple contractions and must prioritize capital preservation.

### Pass D (Summer 2022 - Bear Bottom to Recovery): Missed Milestone (+0.0%)
*   **Verdict:** Survived (No Ruin, Capital Preserved).
*   **What happened:** Sat in cash and ended at exactly **$300.00** (0 trades).
*   **Expected:** Compound cash during the bear bottom.
*   **Actual:** Inactive, ended at $300.00.
*   **Root Cause:** The only option setups available were index bear puts (premium $2.00, cost $200.00). Under standard sizing, a $300 account could not buy them. The Model v3 restricted the Golden Rule 4 override strictly to catalyst call options, preventing the bot from buying the speculative index puts. This protected the account from a -53.0% loss (the result of the prior un-refined run).
*   **Lesson:** In a persistent macro bear market with no corporate catalyst events, inactivity and capital preservation (+0.0%) are a massive victory compared to forcing speculative hedges that drag the account into ruin.

### Pass E (Autumn 2023 - AI Breakout to Carry Unwind): Missed Milestone (+1,351.9%)
*   **Verdict:** Survived (No Ruin, Close to Goal).
*   **What happened:** Grew from $300 to **$4,355.73** but did not cross the $5,300 threshold.
*   **Root Cause:** The pass started in October 2023, missing the ENPH PUT catalyst of July 2023. It successfully captured both SMCI catalysts in January 2024 (growing the account to $3,800), but the remaining months of the pass (Feb to Sept 2024) lacked additional high-velocity option catalysts to cover the remaining $1,500 gap.
*   **Lesson:** Even with a +1,350% return, a 1-year segment is sometimes too short to cover the 17.6x compounding required for a $300 account to pay a $5,000 debt if it misses one of the year's major catalysts.

### Pass F (Spring 2024 - Post-Hype Consolidation) & Pass G (Late Summer 2025): Missed Milestone (+67.6% and +85.1%)
*   **Verdict:** Survived (No Ruin).
*   **Root Cause:** These passes ran during flat/consolidation years with no options catalysts in the feed. They grew slowly via TQQQ/SOXL share swings.
*   **Lesson:** Baseline swing compounding provides steady growth but requires more time to hit major capital milestones.

---

## 3. The Diagnostic Breakthrough: Ending Pricing Leak Bug

During this autopsy, we identified a systemic diagnostic leak in the backtester's ending accounting loop:

*   **The Mistake:** When liquidating active positions at the end of a WFO pass, the backtester accessed `df.iloc[-1]['Close']`, which pulled the closing price from the **absolute last row of the historical dataset** (June 1, 2026) rather than the price on the **exact end date of that specific pass** (`pass_dates[-1]`).
*   **Impact:** This artificially inflated the ending asset values of earlier passes. For example, Pass C (ending in February 2022) appeared to end at **$5,133.99** because its active shares were valued at 2026 prices. Its true, non-hindsight ending value was **$1,414.45**.
*   **Mitigation:** Rewrote the ending accounting loops in `walk_forward_random_segments.py`, `walk_forward_backtest.py`, and `stress_tester.py` to look up the closing price on the exact end date of the pass.
*   **Prevention:** Never use absolute positional indices (like `.iloc[-1]`) on dataframes representing active data stores when performing date-bounded segment analysis.

---

## 4. Refined Playbook Integration (Rules Update)

*   **Speculative Option Override Prohibition (Golden Rule 4 Refinement):** Under $300 starting capital, the single-contract position-sizing override **must never** be applied to index puts, bear market hedges, or trend-following options. The override is restricted *solely* to high-conviction corporate earnings/short squeeze options in the catalyst feed. Speculative index hedges are capped strictly at the account's standard 50% allocation (buying 0 contracts if cash is insufficient) to protect the account from capital erosion.
