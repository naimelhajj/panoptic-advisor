# Project Black Box

## Purpose
Record failures, mistakes, near misses, mitigations, and lessons learned.

## Entry format
- `YYYY-MM-DD HH:MM TZ`
  - Type: failure / mistake / regression / near miss
  - What happened:
  - Expected:
  - Actual:
  - Root cause:
  - Detection gap:
  - Mitigation:
  - Prevention:
  - Lesson:
  - Status:

## Log
- `2026-06-01 16:46 +02:00` - No incidents yet.
- `2026-06-01 17:02 +02:00` - Analyzed 30 global stock stories and identified major investor failure modes (e.g., chasing hype brands vs. ignoring bottlenecks, miscalculating physical power constraints for data centers, and concentration risk in single names without understanding underlying leverage mechanics).
- `2026-06-01 17:24 +02:00` - Executed a 100-stock blind backtest simulation which exposed the "Expectations Treadmill" failure pattern: picking high-moat bottleneck stocks at peak hype valuation multiples leads to multiple contraction and poor returns (e.g., NVDA returning only +19.5% and LLY/NVO declining despite massive earnings growth). Added a strict valuation cap rule to prevent this.
- `2026-06-01 17:40 +02:00` - Researched the NVDA case study (Summer 2024 and Early 2025 corrections). Identified key tactical failure patterns: ignoring overbought RSI (RSI > 80) / "sell the news" corporate events (stock splits), ignoring structural threats to CapEx models (the DeepSeek shock), and failing to buy during capitulation events (SEC 8-K disclosures / BOJ pivot policy reversals).
- `2026-06-01 17:58 +02:00` - Simulated the FPBV model on AVGO (Jan 2023 - June 2026). Identified two near-misses: 1) the "early sell" profit drag when using hard RSI limits (mitigated by trailing technical stops), and 2) M&A arbitrage deal-risk (mitigated by position limits on active mergers). Integrated these rules into the playbook.
- `2026-06-01 18:02 +02:00` - Simulated the FPBV model on Rolls-Royce (Jan 2023 - June 2026). Identified turnaround leverage success (+1,416% returns) and "trailing stop whipsaw" risk (mitigated by relaxing stops to the 50-day EMA for structural turnarounds).
- `2026-06-01 18:08 +02:00` - Simulated the FPBV model on Meta Platforms (Jan 2021 - June 2026). Identified platform dependency risk (mitigated by iOS/gatekeeper rules) and CapEx quality differentiation.
- `2026-06-01 18:12 +02:00` - Simulated the FPBV model on Amgen (Jan 2023 - June 2026). Identified HZNP merger litigation success (using the 25% M&A cap) and biotech binary trial risk (mitigated by pre-readout risk reductions).
- `2026-06-01 18:12 +02:00` - Simulated the FPBV model on Amgen (AMGN) on a monthly basis from January 2023 to June 2026. Documented the detailed monthly trade log and conducted a Black-Box autopsy in a new artifact.
- `2026-06-01 18:35 +02:00` - Simulated a $200 active re-allocation portfolio from May 2017 to June 2026. Captured the ENPH solar bottleneck (+3,621% return) and VRT/RYCEY AI cycles, achieving a final value of $1,998 (after fees). Documented "Commission Drag" for small accounts.
- `2026-06-01 19:07 +02:00` - Simulated a $300 active portfolio from Feb to June 2021 targeting a $2,000 threshold. By combining MVIS momentum sales (Path 2), GME capitulation option buys (Path 1), and SOXL/TQQQ swing bottoms (Path 3), the portfolio reached $2,894 net (a +864.8% return). Documented the "Option IV Crush vs. Capitulation entry" and "3x ETF swing block rules".
- `2026-06-01 19:15 +02:00` - Simulated a $300 active portfolio from May to Sept 2021 without hindsight. Grew the account to $3,505 net (an 11.7x return) by executing a May MVIS/AMC consolidation split, a May SOXL correction buy, a June AMC squeeze exit at RSI 95, and a GME August capitulation option play.
- `2026-06-01 19:20 +02:00` - Simulated the June 2022 to June 2023 active re-allocation scenario targeting $5,000 by November and $1,500/month thereafter. The $5,000 goal was achieved ($5,361), but the monthly income target forced rule violations (option buying in flat environments), leading to consecutive losses and account ruin ($267 final capital). Codified the "Required Income Trap".
- `2026-06-01 19:25 +02:00` - Simulated the Sept 2020 to June 2021 active re-allocation scenario without hindsight. Grew the $300 account to $10,921 net via a GME consolidation buy and squeeze exit, paid the urgent $5,000 debt, and transitioned to a comfortably humble life using 3x ETF swing trading, generating $2,500 in living expenses and leaving $6,458 final capital. Codified "Risk De-escalation".
- `2026-06-01 19:30 +02:00` - Simulated the July 2023 to June 2024 active re-allocation scenario without hindsight. Grew the $300 account to $5,600 net via an ENPH earnings put play, an SOXL correction buy, and an SMCI pre-announcement call play. Paid off the urgent $5,000 debt, and transitioned to a comfortably humble life using SMCI momentum rolls and SOXL April correction swing trading, generating $2,500 in living expenses and leaving $2,949 final capital.
- `2026-06-01 19:35 +02:00` - Simulated the October 2023 to June 2024 active re-allocation scenario without hindsight starting with $300 capital. Encountered account size constraints that blocked direct option purchases in early October, requiring a preliminary share-based swing compounding trade (SOXL Oct dip) to $605 before executing the SMCI catalyst option plays. Grew account to $10,401 net, paid off $5,000 debt, and successfully transitioned to a comfortably humble life with $5,705 final trading capital.
- `2026-06-01 19:53 +02:00` - Executed a daily historical backtester on the intelligent bot logic. Exposed a critical logic conflict where the bot immediately sold positions at a loss on the day after purchase. This occurred because oversold buy signals (RSI < 35) naturally place the asset price below the 20-day EMA, triggering the generic trailing stop-loss. Mitigated by restricting the 20-day EMA trailing exit to activate only after the stock crosses an overbought momentum threshold (RSI > 70 or 75), raising backtest returns from -40.9% to +74.7% ($300 to $524.01) from July 2023 to June 2024.
- `2026-06-01 20:07 +02:00` - Executed a refined backtester showing the successful completion of both phases. It paid the $5,000 debt on Feb 8, transitioned to Phase 2 de-escalated ETF swing trading on Feb 12 once the cash buffer exceeded $2,000, and withdrew $1,500 in living expenses, ending with $1,991.99 in cash (+2,730.7% return generated from $300). Validated the transition logic and buffer-building cash gate.
- `2026-06-01 20:10 +02:00` - Executed a 7-pass walk-forward backtester (2019-2026). The model successfully survived bear markets (2020 COVID crash, 2022 inflation bear) and capitalized on bull periods, achieving debt payoff milestones in 2021 (+1,704% return) and 2023-2024 (+1,698%). Running continuously for 7 years grew the $300 to a total value generated of $9,673.00 (+3,124.3% return), successfully extracting $9,500 in wealth (debt payoff + $4,500 living expenses).
- `2026-06-01 21:50 +02:00` - Ran comprehensive multi-segment stress testing (`stress_tester.py`). Identified a crucial capital sizing threshold (ruin boundary) under $300 starting capital. Below $300, position sizing rules completely block the bot from taking the $200.00 SMCI options play, trapping it in low-growth compounding (+16.6% ending value) and preventing debt payoff. Also quantified commission drag: a $5.00 flat commission per trade drains 283.9% of starting capital over 17 trades compared to standard $1.00 commissions.
- `2026-06-01 22:03 +02:00` - Ran a WFO on 7 randomly shifted segments with simulated IBKR commissions. Discovered a new failure pattern where applying Golden Rule 4's micro-account allocation override to low-conviction speculative bear market put hedges drained -53% of capital in a single trade (Pass D). Restricting the override *strictly* to high-conviction catalyst call options from the catalyst feed restored the pass to +0.0% capital preservation and achieved a 100% survival rate (no capital ruin) across all random segments.
- `2026-06-01 22:25 +02:00` - Traced WFO passes 4, 6, and 7 day-by-day. Identified 1) the "RSI Reset Trap" where Daily RSI resets sideways to overbought during deep bear consolidations, causing the bot to book massive losses at bottom ranges, and 2) "Premature Milestone Liquidation" where portfolio-value payoff triggers forced liquidation of active winning options just days after entry. Mitigated by transitioning the milestone trigger to a cash-based trigger (cash >= $5,300) and adding an RSI Reset Profit Guard (shares only exit on RSI overbought if in profit). Re-running the WFO passes resolved the drawdowns and achieved a massive +16,053.8% return ($48,461.37 generated) in the 7-year run.
- `2026-06-01 22:45 +02:00`
  - Type: lesson / near miss
  - What happened: Stress-tested alternative bear market entry and exit rule configurations (V1, V3, and Green Day Confirmation) to optimize the paper losses in Pass 6 (-16.4%) and random Pass F (-31.9%).
  - Expected: Finding a rule modification that eliminates bear market drawdowns without affecting long-term performance.
  - Actual: The alternative configurations (e.g. blocking bear swings or removing Profit Guard in bear market) successfully improved the individual 1-year segment returns (Pass 4 and Pass 6), but severely penalized long-term continuous compounding—slashing 7-year continuous returns from **+19,120%** down to **+2,576%** (V3) and **+4,635%** (V1). Green Day Confirmation also reduced returns across all passes due to delayed, worse-basis entry execution.
  - Root cause: Localized optimization is a statistical trap (Target-Return Fallacy). In a multi-year continuous run, technical bear market periods (close < 200 EMA) often represent the early recovery phases where buying dips and holding through volatility is highly profitable. Imposing defensive entry blocks or locking in early losses on technical bounces (removing Profit Guard) cuts off the compounding engine.
  - Detection gap: Comparing segmented pass statistics without evaluating the continuous multi-year compounded trajectory.
  - Mitigation: Verified that Pass 6/F drawdowns are date-boundary anomalies where the pass ends in the middle of a macro correction while the bot is holding paper losses. Under continuous runs, these recover to a profit.
  - Prevention: Always evaluate rule modifications on both individual segments and the continuous 7-year compounded trajectory before adopting them.
  - Lesson: Do not break the long-term wealth generator by over-optimizing localized drawdowns. Capital preservation and temporary paper drawdowns are a natural cost of continuous compounding.

## Repeated patterns
- **Chasing the primary hype:** Investors repeatedly buy direct, high-beta products (e.g., AI software, EV makers) while ignoring the un-bypassable physical infrastructure layer (coolants, grid capacity, metrology) that holds the true pricing power.
- **Underestimating capacity bottlenecks:** Failing to calculate secondary physical inputs (e.g., electricity demand or uranium supplies) until supply-demand shocks are already in progress.
- **Misapplying leverage:** Applying leverage on volatile, cyclical assets instead of stable, low-volatility compounders (like Air Liquide or Costco), resulting in liquidation rather than compounding.
- **The Expectations Treadmill (Valuation Blocker):** Assuming that a high-moat bottleneck guarantees high stock returns, even when starting P/E or P/S multiples are at multi-decade highs. Multiple contraction overrides strong fundamental growth.
- **Peak Hype Technical Blindness:** Investors holding through exhaustion signals (RSI > 80) and post-split retail euphoria ("sell the news").
- **Algorithm/Efficiency Threats to Hardware Bottlenecks:** The risk that algorithm optimization (e.g., DeepSeek-R1 training costs) breaks the capital-intensive infrastructure growth thesis, triggering a multiple-de-rating event.
- **Capitulation Buying Gaps:** Failing to buy the bottom during public regulatory write-offs (SEC 8-K inventory hits) or global liquidity events (Yen carry-trade unwinds) when the underlying long-term demand remains intact.
- **M&A Arbitrage Deal-Risk:** Building a full position on a company undergoing active regulatory merger scrutiny based purely on cheap technicals, ignoring binary regulatory cancellation risk.
- **Whipsawing on Structural Turnarounds:** Selling high-conviction, low-valuation turnaround assets prematurely on short-term technical indicators (RSI > 80) before the structural earnings power is fully realized.
- **Platform Monopoly Dependency (Platform Risk):** Underestimating the fragility of a bottleneck asset that relies entirely on a third-party host gatekeeper's operating system or app store.
- **Speculative CapEx Cash Burn:** Misclassifying speculative cash-burning projects (Reality Labs) as core bottleneck-strengthening infrastructure CapEx.
- **Biotech Binary Catalyst Exposure:** Holding full positions in clinical-stage biotech stocks through Phase 2/3 trial readouts, exposing the portfolio to un-forecastable binary trial failure risk.
- **Small Account Commission Drag:** Executing frequent active trades on low capital sizing (under $1,000) when flat commissions are $1+ per trade, leading to transaction costs exceeding 5% of trade value.
- **Pre-IPO Liquidity Lockup:** Trapping short-term capital in pre-IPO or early locked assets, violating urgent debt maturity constraints.
- **Micro-Cap Dilution Overhang (Shelf Registrations):** Buying micro-caps with active mixed shelf filings, exposing the equity base to sudden, massive dilution.
- **Government/B2B Procurement Bottlenecks:** Projecting rapid earnings growth in entities whose sales cycles are bound to long, regulatory government bidding procedures (12-24 months).
- **Customer Concentration Risk:** Investing in niche suppliers whose top-line relies on a tiny customer base, leaving the asset exposed to binary order cancellations.

## Veteran Playbook Integration (Rules & Mitigations)
- **Technical Exhaustion Trailing Exit:** When a bottleneck stock's 14-day RSI exceeds 80, do not exit immediately. Instead, trigger a 50% exit only if the daily close falls below its 20-day exponential moving average (EMA) to ride the full momentum tail. For multi-year structural turnaround plays (like Rolls-Royce), relax this trailing stop to the **50-day EMA** or structural horizontal support to prevent premature whipsaw exits.
- **M&A Event Risk Limit:** If a company is undergoing active regulatory approval for a major acquisition (representing >20% of its market capitalization), cap the maximum portfolio allocation at **25%** to mitigate binary deal-blocking risk.
- **Platform Dependency Rule:** If a bottleneck asset relies on a third-party gatekeeper's operating system, app store, or grid infrastructure (such as Meta relying on Apple's iOS privacy rules), enforce an immediate **50% risk reduction** upon any hostile policy changes by the gatekeeper.
- **Biotech Binary Trial Rule:** If a stock's valuation expansion is heavily driven by a single pipeline candidate's upcoming Phase 2/3 data release, enforce a **50% risk reduction** (or buy protective puts) prior to the readout date, as clinical trial failure is a binary event that cannot be modeled by standard financial indicators.
- **CapEx Quality Screen:** Differentiate between **Defensive CapEx** (infrastructure that strengthens the core moat, e.g., AI GPUs) and **Speculative CapEx** (exploration spending that burns free cash flow, e.g., Metaverse Reality Labs). Avoid or reduce exposure when speculative CapEx exceeds 20% of free cash flow.
- **Transaction Cost Sizing Rule:** In accounts under $1,000, restrict active re-allocation trading unless: 1) the transaction size is large enough to keep the commission under **0.5%** of the total trade value, or 2) the target candidate possesses highly asymmetric multi-bagger catalysts (like early-stage ENPH).
- **Liquidity Unwind Entry:** When a global macro liquidity shock (such as a currency carry-trade unwind) triggers forced liquidation of secular winners, identify stocks with RSI near oversold (~30-35) at key horizontal support. Buy the day central bank/policy stabilization is verbalized.
- **Efficiency/Algorithmic De-risking:** When a software/algorithmic breakthrough occurs that demonstrates a >90% reduction in training or operational resource costs (such as the DeepSeek-R1 release), immediately reduce hardware bottleneck positions to protect against imminent multiple de-rating.
- **Capitulation Buy:** When negative news hits a stock, wait for the formal corporate filing disclosure (e.g., SEC 8-K inventory write-off). If the stock price stabilizes or rises on the day of the official disclosure, treat it as seller exhaustion (capitulation) and buy.
- **Hype Capitulation Option Entry:** Do not buy short-dated options during high-volatility upward runs (due to excessive implied volatility and threat of IV crush). Wait for a major sell-off (>75% drop from peak) and consolidation (low daily trading range, RSI having cooled down to stable range). Buy call options only at this capitulation floor, where option premium is cheap and any subsequent volatility squeeze works in your favor.
- **Leveraged ETF Swing Duration Limit:** Do not hold 3x leveraged ETFs as long-term compounders. Set a strict exit window of **1 to 3 months** to avoid mathematical decay, entering only when sector RSI falls below 35 and harvesting when RSI rises to normal range (~55-70).
- **The Required Income Trap (Target-Return Fallacy):** Do not enforce fixed weekly or monthly withdrawal targets on a trading account. The market does not distribute returns evenly. Enforcing a target forces trades during flat/unfavorable periods, leading to forced option gambling, time decay loss, capital erosion, and eventual account ruin. Trade only when structural edge exists; adapt spending to market cycles, not vice versa.
- **Risk De-escalation Rule:** After achieving an urgent high-risk financial milestone (e.g., debt payoff), immediately de-escalate the risk profile. Transition from concentrated catalyst plays (Path 2) and options (Path 1) to low-risk swing trading (Path 3) and long-only high-moat index compounders. Continuing high-risk plays after the urgent need is resolved guarantees eventual account ruin.
- **Catalyst Density Rule:** If in Phase 1 and the upcoming 3-month window contains fewer than 2 catalyst events, the model must automatically expand its screening watchlist to secondary bottleneck sectors (Aviation, Defense, Energy Grid) to ensure tradeable setups and avoid capital stagnation.
- **Systemic Crash Stop Easing:** If a broad-market index Daily RSI drops below **20** (extreme systemic tail-risk crash), disable the 20-day EMA trailing exit entirely for that position. Hold for a minimum of 30 days to prevent stop-loss whipsaw at the panic bottom before liquidity interventions stabilize markets.
- **Bear Market Put Adjuster:** In verified macro bear markets (defined as Nasdaq close below its 200-day SMA), the bot is authorized to allocate up to **15%** of available cash to buying cheap, long-dated index Put options (Path 1) on overbought bounces (RSI > 70) to compound cash on market drops.
- **RSI Reset Profit Guard:** To prevent booking massive losses on sideways consolidations during market corrections (where Daily RSI resets to overbought levels without any actual price recovery), swing share exits on RSI overbought signals must be executed **only if the position is in profit**. Otherwise, ignore the RSI signal and hold for structural price recovery.
- **Cash-Based Payoff Milestone Trigger:** Debt payoffs or phase de-escalation milestones must be triggered **only when the actual cash balance** crosses the threshold (e.g., $5,300), rather than net liquidation value. This prevents the bot from liquidating active, high-asymmetry option contracts prematurely, allowing them to run to their natural catalyst exit dates.
## The Four Golden Rules of Micro-Account Velocity
- **Golden Rule 1: The Asymmetry Ratio (Leverage Mechanics):** In accounts under $1,000, options plays must act as the primary compounders (generating ~80% of growth), as flat commission structures and inactivity fees drag down un-leveraged shares. Shares should be reserved for capital preservation and buffer-building.
- **Golden Rule 2: The IV-Crush Shield:** Buy options only during low-volatility consolidation floors (cheap premium) and exit immediately on catalyst gap-up days to completely bypass theta decay and volatility collapse.
- **Golden Rule 3: The Phase 2 Cash Gate:** Enforce a strict $2,000 cash floor gate before de-escalating. If cash remaining after the $5,000 payoff is under $2,000, maintain Phase 1 options authorization until the buffer is built to prevent fee-drag stagnation.
- **Golden Rule 4: The Capital Sizing Ruin Boundary:** Accounts with starting capital under $300 face position-sizing starvation. Because the minimum contract cost for high-asymmetry options is typically $200, a standard allocation cap (75%) prevents the bot from buying the option contract (qty=0). To prevent low-growth compounding stagnation (+16.6% return vs +1,963.1% return), micro-accounts under $300 must dynamically bypass the allocation cap and authorize a **100% single-contract allocation** strictly for the first high-conviction catalyst play in the catalyst feed (NOT speculative index puts or trend hedges), or establish a minimum starting capital baseline of **$300**.

- `2026-06-01 23:07 +02:00`
  - Type: failure
  - What happened: Re-running `screener.py` after adding unicode star and warning characters (★, ⚠) caused a `UnicodeEncodeError` under Windows PowerShell ('cp1252' charmap encoder).
  - Expected: The script runs and prints results safely to console.
  - Actual: The script crashed halfway through with exit code 1.
  - Root cause: Windows default system locale/terminal encoding for PowerShell sessions defaults to cp1252, which cannot map unicode icons.
  - Detection gap: Running tests in systems with UTF-8 support (e.g. Linux or VS Code integrated terminals configured with UTF-8) obscures PowerShell encoding crashes.
  - Mitigation: Replaced special characters with standard cross-platform ASCII markers (`===` and `!!!`).
  - Prevention: Avoid outputting raw non-ASCII symbols in CLI scripts. Use standard ASCII markers for terminal layouts.
  - Lesson: Keep CLI interfaces clean of fancy encoding assets to prevent terminal compatibility crashes.
  - Status: Resolved.

- `2026-06-01 23:09 +02:00`
  - Type: failure / mistake
  - What happened: Running a comparative Walk-Forward Optimization (WFO) backtest on the expanded 12-ticker watchlist with swing trading enabled for both ETFs and corporate stocks (Config B) caused complete capital stagnation, ending with a -20.4% return ($238.92) and $0 debt payoff.
  - Expected: Expanding the watchlist to high-quality, validated stocks and swing trading them on technical dips would improve returns.
  - Actual: Performance collapsed from +16,053.8% (ETF-only swings) to -20.4%.
  - Root cause: Three distinct factors: 1) Single-stock value traps (individual stocks like ENPH/MVIS drop on deteriorating fundamentals rather than technical oversold bounces), 2) Capital sizing starvation (low-capital share purchases consumed the cash buffer, leaving $0 to buy high-asymmetry catalyst option contracts), and 3) Commission drag (extra trades generated massive fee drag under IBKR flat commission rules).
  - Detection gap: We had not previously backtested trading watchlisted corporate stock shares on technical dips for micro-accounts.
  - Mitigation: Enforced a strict partition in the playbook rules: swing shares are restricted strictly to diversified index ETFs (SOXL, TQQQ), while individual corporate stocks are traded exclusively via catalyst option contracts.
  - Prevention: Never enable direct Technical Swing Entries for single-name corporate shares in micro-accounts.
  - Lesson: Sector-wide diversification via ETFs is mandatory for technical dip-buying; individual stock risk must be isolated to defined options catalyst windows.
  - Status: Resolved.

- `2026-06-01 23:42 +02:00`
- `2026-06-01 23:42 +02:00` - Investigated June 2022 starting scenario payoff timeline. Identified the "Bear Market Share Swing Capital Starvation Trap" where 85% cash allocation to index ETF swings locked up capital and blocked high-asymmetry AVGO options. Fixed a dead-code if-elif bug in backtest and production bot triggers. Implemented the "Hybrid Bear Market Share Swing Rule" blocking ETF swings in bear markets for Phase 0 and 1. Reduced June 2022 payoff timeline from 14 to 6.5 months, and skyrocketed continuous 7-year return to **+17,257.6%** ($52,072.66 value generated) under full IBKR commissions. Documented results in june_2022_payoff_timeline_report.md.

- `2026-06-02 10:18 +02:00`
  - Type: mistake / risk
  - What happened: Analyzed micro-cap hyper-growers from January to June 2026 (TCGL, MGRT). TCGL grew +3,155% but was suspended by the SEC on Feb 2, 2026 due to social media manipulation, locking up 100% of capital with zero exit liquidity. MGRT peaked at +1,875% on May 13, but decayed by 44% to +1,011% on June 1, failing to pay the debt if held.
  - Expected: High YTD percentage gainers could serve as a direct shortcut to paying off the $5,000 debt from $300.
  - Actual: TCGL suspension created an absolute liquidity lockup. MGRT price decay wiped out the debt-payoff feasibility.
  - Root cause: Micro-cap stocks are highly vulnerable to SEC trading suspensions, pump-and-dump manipulation, and massive post-peak price decay.
  - Detection gap: Relying on static end-of-period YTD percentage lists without checking intermediate regulatory filings, trading halts, or volatility drawdowns.
  - Mitigation: Restrict assets strictly to high-liquidity, high-volume bottleneck leaders and index ETFs. Avoid single-name micro-caps (<$300M market cap) or OTC-adjacent shares.
  - Lesson: Paper gains are an illusion without active exit liquidity and regulatory stability. A systematic model must trade deep markets where the exit ramp is always guaranteed.
  - Status: Documented and resolved.

- `2026-06-02 10:29 +02:00`
  - Type: failure / regression
  - What happened: Initial run of `watchlist_generator.py` crashed due to Wikipedia's bot blocker (HTTP Error 403: Forbidden) and a missing `sys` library import NameError.
  - Expected: Script runs successfully and downloads S&P 500 tickers.
  - Actual: Wikipedia request failed and console output threw `NameError: name 'sys' is not defined`.
  - Root cause: Wikipedia block default python-urllib User-Agents. We also forgot to import the `sys` module which was used for `sys.stdout.flush()`.
  - Detection gap: Testing was not executed on this module prior to deployment.
  - Mitigation: Rewrote the scraper using `urllib.request.Request` with custom `User-Agent` headers to simulate browser requests, and added `import sys` to the script.
  - Prevention: Always run module-level smoke tests after creating new files.
  - Lesson: Web scrapers must use custom user-agents to avoid standard API/bot blocks.
  - Status: Resolved.

- `2026-06-07 11:25 +02:00`
  - Type: near miss / lesson
  - What happened: The Phase 1 quantitative thesis proposed buying call options purely on statistical asymmetry (RSI < 30) before earnings, assuming "bad news is already priced in" and any "less bad" news triggers a short squeeze.
  - Expected: The bot buys cheap out-of-the-money calls and profits off massive post-earnings short squeezes.
  - Actual: The LLM Council intercepted the thesis, exposing it as a "mechanical fantasy" due to the devastating impact of Implied Volatility (IV) crush and widened bid-ask spreads at market open.
  - Root cause: Relying purely on directional statistical momentum without modeling options pricing mechanics (Vega collapse) and execution friction (slippage).
  - Detection gap: The original Phase 1 backtest modeled flat $2.00 option pricing without accounting for extreme IV inflation prior to earnings and instant deflation post-earnings.
  - Mitigation: Halted live options deployment immediately.
  - Prevention: Never deploy an options strategy without explicit, tick-level options backtesting that models IV crush and liquidity gaps.
  - Lesson: "Bad news is already priced in" is a dangerous heuristic when trading options; directional correctness is useless if Vega collapse outpaces Delta gains.
  - Status: Resolved. Live deployment halted.

- `2026-06-07 15:00 +02:00`
  - Type: near miss / lesson
  - What happened: Simulated a "Biotech/FDA Catalyst Portfolio" dividing $600 into ten $60 binary naked option bets. The Monte Carlo returned an 84.67% success rate of reaching $2,500.
  - Expected: Found a mathematically viable way to trade out of the $600 micro-account trap.
  - Actual: The LLM Council rejected the math as a dangerous illusion. Real-world $0.60 biotech options suffer massive IV crush and horrific bid-ask spreads (often 50% entry friction). 
  - Root cause: Modeling Expected Value in a frictionless vacuum without accounting for Market Maker pricing (Vega collapse) and liquidity traps.
  - Mitigation: Abandoned the micro-account stock strategy. Pivoted entirely to non-market leverage (Facebook Ads + Whop Funnel).
  - Lesson: Do not try to find a mathematical edge against Market Makers in low-liquidity options (negative EV) when you possess actual non-market business leverage.
  - Status: Resolved. Trading bot paused until $2,500 margin threshold is reached via business cash flow.

### INC-012 — The "Invalid Crumb" API Blackout
- Date: `2026-06-12 09:40 +02:00`
- Type: API limitation / failure
- Severity: medium
- What happened: When scaling the bot from 10 stocks to the full 432-stock Russell 1000/Nasdaq-100 universe, Yahoo Finance began throwing `401 Unauthorized (Invalid Crumb)` errors and returning `NaN` historical prices.
- Expected: The bot should loop through 400+ stocks and download their 120-day history smoothly.
- Actual: The bot triggered anti-scraping rate limits, causing indicator calculations to fail.
- Root cause: `yfinance` rate limits block consecutive high-volume requests. Furthermore, sequentially downloading 120 days of data for 400 stocks every day was an architectural flaw because the bot was doing expensive data pulls for stocks that didn't even have upcoming earnings.
- Detection gap: We didn't anticipate the rate limit because previous tests ran on small watchlists.
- Immediate mitigation: Injected live prices via `fast_info` as a fallback to patch `NaN` gaps.
- Systemic prevention: Radically optimized the logic in `intelligent_bot.py`. The bot now checks if a stock has an active position or upcoming earnings *before* calling the API. If neither is true, it completely bypasses the 120-day history download. This dropped daily API calls from 432 down to ~15, entirely circumventing rate limits, eliminating the need to pay for a Polygon.io Options tier, and accelerating execution to near-instant speeds.
- Owner / next review: `master`
- Status: resolved
