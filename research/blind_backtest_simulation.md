# Blind Backtest Simulation (June 2024 - June 2025)

This document analyzes the results of a blind investment simulation using a pool of 100 diverse stocks that existed in June 2024. Using our first-principles framework, we selected 11 target picks in June 2024 (without hindsight) and compared them against their actual performance in June 2025.

---

## 1. The Full Pool & Actual Returns (June 2024 - June 2025)

Out of the 100 stocks, only **4 stocks** achieved raw returns of **>100%**:
1.  **RHM.DE (Rheinmetall):** +241.72%
2.  **GEV (GE Vernova):** +185.20%
3.  **RYCEY (Rolls-Royce):** +106.60%
4.  **HWM (Howmet Aerospace):** +104.62%

*Notable near-doublers:* **KOG.OL** (+98.87%), **TSLA** (+94.39%), **SAAB-B.ST** (+90.90%), **AVGO** (+90.45%), **VST** (+81.09%).

---

## 2. Our Blind Selections vs. Realized Performance

Here is how the 11 selections we chose using the first-principles framework (as of June 2024) actually performed by June 2025:

| Ticker | June 2024 Price | June 2025 Price | Actual Return | Hit >100%? | First-Principles Review |
| --- | --- | --- | --- | --- | --- |
| **RHM.DE** | €527.04 | €1,801.00 | **+241.72%** | **YES** | **Success:** Ammunition depletion was a physical bottleneck that sovereign states had to fund immediately. |
| **RYCEY** | $5.74 | $11.87 | **+106.60%** | **YES** | **Success:** Engine service hours returned faster than expected, compounding high-margin cash flow. |
| **KOG.OL** | NOK 176.93 | NOK 351.86 | **+98.87%** | *Almost* | **Success:** Missed the 100% threshold by just 1.13%. Air defense backlog conversion was highly lucrative. |
| **SAAB-B.ST**| SEK 254.06 | SEK 485.01 | **+90.90%** | *Close* | **Success:** Strong re-rating driven by Northern Europe re-armament. |
| **AVGO** | $129.54 | $246.71 | **+90.45%** | *Close* | **Success:** Custom ASICs and networking dominated the hardware build-out. |
| **VST** | $92.01 | $166.62 | **+81.09%** | *Close* | **Success:** Baseload electricity was a major winner, though it fell just short of a double. |
| **NVDA** | $114.94 | $137.35 | **+19.50%** | No | *Underperformed:* See "The Hype Giants" analysis below. |
| **VRT** | $95.87 | $109.10 | **+13.80%** | No | *Underperformed:* Liquid cooling demand grew, but valuation multiples contracted. |
| **POWL** | $56.66 | $57.40 | **+1.30%** | No | *Underperformed:* Grid hardware backlogs remained high, but execution timelines delayed revenue. |
| **LLY** | $819.81 | $741.87 | **-9.51%** | No | *Underperformed:* Extreme starting multiple compressed despite strong drug sales. |
| **NVO** | $126.84 | $69.47 | **-45.23%** | No | *Underperformed:* Supply expansion delays and competitive pricing compressed margins. |

---

## 3. Black-Box Analysis: Why the Hype Giants Underperformed
*Why did NVDA (+19.5%), VRT (+13.8%), LLY (-9.5%), and NVO (-45.2%) underperform, despite having massive moats?*

### The Expectations Treadmill & Multiple Contraction
In June 2024, these stocks represented the peak of market consensus. 
*   **The Valuation Blocker:** When a company's price-to-earnings (P/E) or price-to-sales multiple is stretched to historical extremes (e.g., Lilly trading at >80x forward earnings), the market has already priced in 5–10 years of perfect, uninterrupted growth.
*   **The Reality Check:** Even if the underlying business grows by 50% (which Nvidia and Lilly did), if the market's enthusiasm cools and the P/E multiple contracts from 80x to 40x, the stock price will go sideways or fall.
*   **Lesson:** A great company is not always a great stock. First principles must calculate **starting valuation** as a risk factor.

---

## 4. The Winners We Missed: First-Principles Autopsy
*Why did GE Vernova (+185.2%) and Howmet Aerospace (+104.6%) double, and why did we miss them?*

### GE Vernova (GEV) — Return: +185.20%
*   **The Story:** Spun off from General Electric in April 2024. GEV controls a massive portion of the world's gas turbines and wind power infrastructure.
*   **Why It Doubled:** The market initially treated it as a legacy, low-margin utility manufacturer. However, as data center electricity constraints worsened, utilities rushed to buy gas turbines (GEV's specialty) to add capacity quickly. 
*   **Detection Gap:** We focused on the high-profile electricity providers (Vistra/Constellation) and grid equipment (Eaton/Powell), but missed the turbine manufacturer itself, which was severely underpriced due to its recent spin-off status.

### Howmet Aerospace (HWM) — Return: +104.62%
*   **The Story:** HWM makes specialized engine castings, titanium components, and aerospace fasteners.
*   **Why It Doubled:** Every commercial aircraft engine (Rolls-Royce, Safran, GE) and airframe (Airbus, Boeing) requires Howmet's components. They are a pure **monopoly bottleneck** for aerospace. As aviation flight hours surged, engine manufacturers had to buy spare parts at high prices.
*   **Detection Gap:** We focused on the main engine manufacturers (Rolls-Royce, Safran) but missed the sub-component supplier (Howmet) which possessed even higher pricing power and lower structural execution risk.

---

## 5. Key Takeaways for our Stock Screener

To build a high-probability stock finder, we must integrate these refined rules:
1.  **Incorporate Valuation Caps:** Filter out stocks trading at extreme historically high multiples (e.g., PEG ratio > 3 or Price/Sales > 20) to avoid the "expectations treadmill."
2.  **Scan for Spin-offs / Re-ratings:** Look for recent spin-offs in bottleneck sectors where the market has not yet recalculated the standalone company's pricing power.
3.  **Trace the Sub-Component Chain:** Look deeper into the supply chain. If an oligopoly (like engine manufacturing) is hot, look for the *single-source supplier* of their critical components (like Howmet).
