import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime

WATCHLIST_PATH = 'watchlist.json'
CATALYSTS_PATH = 'upcoming_catalysts.json'
HISTORY_PATH = 'advisor_history.json'
OUTPUT_HTML = 'advisor_dashboard.html'

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

def generate_html(cards_html, history_html, today_str):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panoptic Quants - Daily Advisor</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        :root {{
            --bg-dark: #09090b; --glass-bg: rgba(24, 24, 27, 0.65); --glass-border: rgba(255, 255, 255, 0.08);
            --text-main: #fafafa; --text-muted: #a1a1aa;
            --color-buy: #10b981; --color-buy-glow: rgba(16, 185, 129, 0.2);
            --color-call: #3b82f6; --color-call-glow: rgba(59, 130, 246, 0.2);
            --color-put: #f43f5e; --color-put-glow: rgba(244, 63, 94, 0.2);
            --color-wait: #f59e0b; --color-wait-glow: rgba(245, 158, 11, 0.2);
            --color-panic: #8b5cf6; --color-panic-glow: rgba(139, 92, 246, 0.2);
            --color-sell: #ec4899; --color-sell-glow: rgba(236, 72, 153, 0.2);
            --color-star: #fbbf24;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Outfit', sans-serif; background-color: var(--bg-dark); color: var(--text-main); min-height: 100vh; padding: 3rem 1rem; }}
        body::before {{
            content: ''; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1;
            background: radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.15), transparent 25%),
                        radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.15), transparent 25%);
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 2rem; }}
        h1 {{ font-size: 3.5rem; font-weight: 800; background: linear-gradient(to right, #60a5fa, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }}
        .subtitle {{ font-size: 1.2rem; color: var(--text-muted); font-weight: 300; }}
        .date-badge {{ display: inline-block; margin-top: 1.5rem; padding: 0.5rem 1.5rem; background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 50px; font-weight: 600; }}
        
        .portfolio-input-container {{ text-align: center; margin-bottom: 3rem; animation: fadeInUp 0.8s ease-out; }}
        .portfolio-input-container label {{ color: var(--text-muted); font-size: 1.1rem; font-weight: 600; }}
        .portfolio-input-container input {{ 
            background: var(--glass-bg); color: var(--text-main); border: 1px solid #60a5fa; 
            padding: 0.6rem 1rem; border-radius: 8px; font-size: 1.2rem; width: 150px; 
            outline: none; margin-left: 0.5rem; font-family: 'Outfit', sans-serif; font-weight: 800;
            box-shadow: 0 0 15px rgba(96, 165, 250, 0.2); text-align: center;
        }}
        .portfolio-input-container input:focus {{ border-color: #c084fc; box-shadow: 0 0 20px rgba(192, 132, 252, 0.4); }}
        
        .tabs {{ display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; border-bottom: 1px solid var(--glass-border); padding-bottom: 1rem; flex-wrap: wrap; }}
        .tab-btn {{ background: transparent; border: none; color: var(--text-muted); font-size: 1.1rem; font-weight: 600; cursor: pointer; padding: 0.8rem 1.5rem; border-radius: 12px; transition: all 0.3s ease; font-family: 'Outfit', sans-serif; }}
        .tab-btn:hover {{ color: var(--text-main); background: rgba(255,255,255,0.05); }}
        .tab-btn.active {{ color: var(--text-main); background: rgba(255,255,255,0.1); box-shadow: 0 4px 15px rgba(0,0,0,0.2); border-bottom: 2px solid #60a5fa; border-bottom-left-radius: 0; border-bottom-right-radius: 0; }}
        .tab-content {{ display: none; animation: fadeInUp 0.4s ease-out; }}
        .tab-content.active {{ display: block; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2rem; }}
        .card {{ background: var(--glass-bg); backdrop-filter: blur(16px); border: 1px solid var(--glass-border); border-radius: 24px; padding: 2rem; position: relative; overflow: hidden; transition: transform 0.3s ease, box-shadow 0.3s ease; }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.4); }}
        .card::before {{ content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; }}
        .card.action-buy::before {{ background: var(--color-buy); }}
        .card.action-call::before {{ background: var(--color-call); }}
        .card.action-put::before {{ background: var(--color-put); }}
        .card.action-wait::before {{ background: var(--color-wait); }}
        .card.action-panic::before {{ background: var(--color-panic); }}
        .card.action-sell::before {{ background: var(--color-sell); }}
        .ticker-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }}
        .ticker-symbol {{ font-size: 1.8rem; font-weight: 800; display: flex; align-items: center; gap: 0.5rem; }}
        .star-icon {{ color: var(--color-star); font-size: 1.4rem; text-shadow: 0 0 10px rgba(251,191,36,0.5); }}
        .ticker-name {{ font-size: 0.9rem; color: var(--text-muted); display: block; }}
        .action-badge {{ padding: 0.5rem 1rem; border-radius: 12px; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; text-align: right; }}
        .action-buy .action-badge {{ background: var(--color-buy-glow); color: var(--color-buy); }}
        .action-call .action-badge {{ background: var(--color-call-glow); color: var(--color-call); }}
        .action-put .action-badge {{ background: var(--color-put-glow); color: var(--color-put); }}
        .action-wait .action-badge {{ background: var(--color-wait-glow); color: var(--color-wait); }}
        .action-panic .action-badge {{ background: var(--color-panic-glow); color: var(--color-panic); }}
        .action-sell .action-badge {{ background: var(--color-sell-glow); color: var(--color-sell); }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--glass-border); }}
        .stat-item {{ display: flex; flex-direction: column; }}
        .stat-label {{ font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; }}
        .stat-value {{ font-size: 1.2rem; font-weight: 600; }}
        .explanation {{ font-size: 0.95rem; color: #d4d4d8; margin-bottom: 1rem; }}
        .explanation strong {{ color: var(--text-main); }}
        .risk-box {{ background: rgba(0,0,0,0.3); border-radius: 8px; padding: 1rem; border-left: 3px solid #60a5fa; font-size: 0.9rem; color: #cbd5e1; }}
        .risk-box strong {{ color: #60a5fa; }}
        .history-container {{ background: var(--glass-bg); backdrop-filter: blur(16px); border: 1px solid var(--glass-border); border-radius: 24px; padding: 2rem; overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{ padding: 1rem; color: var(--text-muted); border-bottom: 1px solid var(--glass-border); }}
        td {{ padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        tr:last-child td {{ border-bottom: none; }}
        .empty-state {{ text-align: center; padding: 4rem 2rem; color: var(--text-muted); font-size: 1.2rem; display: none; }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(15px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Panoptic Quants</h1>
            <div class="subtitle">Daily Algorithmic Trading Advisor</div>
            <div class="date-badge">Data for {today_str}</div>
        </header>

        <div class="portfolio-input-container">
            <label for="portfolio-size">Your Portfolio Size: $</label>
            <input type="number" id="portfolio-size" value="5000" onchange="updateRisk()" onkeyup="updateRisk()">
        </div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="filterCards('actionable', this)">🎯 Actionable Signals (<span id="action-count">0</span>)</button>
            <button class="tab-btn" onclick="filterCards('starred', this)">⭐ Bot Top Picks (<span id="star-count">0</span>)</button>
            <button class="tab-btn" onclick="filterCards('all', this)">📋 Full Watchlist</button>
            <button class="tab-btn" onclick="openHistory(this)">📖 Historical Ledger</button>
        </div>

        <div id="cards-view" class="tab-content active">
            <div class="grid" id="main-grid">
                {cards_html}
            </div>
            <div id="empty-actionable" class="empty-state">
                No signals found for this filter. The market is quiet—stay patient! ☕
            </div>
        </div>

        <div id="history-view" class="tab-content">
            <div class="history-container">
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Ticker</th>
                            <th>Action</th>
                            <th>Entry Price</th>
                            <th>Status</th>
                            <th>Exit Info</th>
                        </tr>
                    </thead>
                    <tbody>{history_html}</tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        function updateRisk() {{
            const val = document.getElementById('portfolio-size').value;
            const size = parseFloat(val) || 0;
            
            document.querySelectorAll('.card').forEach(card => {{
                const type = card.dataset.type;
                const pct = parseFloat(card.dataset.pct);
                const price = parseFloat(card.dataset.price);
                const riskBox = card.querySelector('.risk-box');
                
                if (!riskBox || !pct || size === 0) return;
                
                const maxDollars = size * pct;
                
                if (type === 'CALLS' || type === 'PUTS') {{
                    const maxPremium = maxDollars / 100.0;
                    riskBox.innerHTML = `<strong>Dynamic Risk Translation:</strong><br>You can risk exactly <strong>$${{maxDollars.toFixed(2)}}</strong> here. Since 1 contract = 100 shares, your absolute limit is <strong>$${{maxPremium.toFixed(2)}} per share</strong>.`;
                }} else if (type === 'SHARES') {{
                    const sharesQty = Math.floor(maxDollars / price);
                    riskBox.innerHTML = `<strong>Dynamic Risk Translation:</strong><br>You can risk exactly <strong>$${{maxDollars.toFixed(2)}}</strong> here. At current prices, you can buy exactly <strong>${{sharesQty}} shares</strong>.`;
                }}
            }});
        }}

        function filterCards(filter, btn) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('history-view').classList.remove('active');
            document.getElementById('cards-view').classList.add('active');
            
            const cards = document.querySelectorAll('.card');
            let visibleCount = 0;
            
            cards.forEach(card => {{
                let show = false;
                if (filter === 'actionable') {{
                    show = !card.classList.contains('action-wait');
                }} else if (filter === 'starred') {{
                    show = card.dataset.starred === 'true';
                }} else {{
                    show = true;
                }}
                
                card.style.display = show ? 'block' : 'none';
                if (show) visibleCount++;
            }});
            
            const emptyState = document.getElementById('empty-actionable');
            emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
        }}
        
        function openHistory(btn) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('cards-view').classList.remove('active');
            document.getElementById('history-view').classList.add('active');
        }}

        window.onload = () => {{
            let actionableCount = 0;
            let starCount = 0;
            document.querySelectorAll('.card').forEach(card => {{
                if (!card.classList.contains('action-wait')) actionableCount++;
                if (card.dataset.starred === 'true') starCount++;
            }});
            document.getElementById('action-count').innerText = actionableCount;
            document.getElementById('star-count').innerText = starCount;
            
            filterCards('actionable', document.querySelector('.tab-btn.active'));
            updateRisk(); // Run once on load to populate
        }}
    </script>
</body>
</html>"""
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Successfully generated HTML at: {OUTPUT_HTML}")


def run():
    # Base Python calculations are done at a baseline of 5000 to filter contracts, 
    # but the frontend is now fully dynamic.
    BASE_PYTHON_PORTFOLIO = 5000.00
    
    watchlist = load_json(WATCHLIST_PATH)
    catalysts = load_json(CATALYSTS_PATH)
    history_data = load_json(HISTORY_PATH)
    if not isinstance(history_data, list):
        history_data = []

    today_str = datetime.now().strftime('%Y-%m-%d')
    today_date = datetime.strptime(today_str, "%Y-%m-%d")
    signals = []

    for ticker, info in watchlist.items():
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="1y")
            if df.empty or len(df) < 200:
                continue
                
            df['RSI'] = calculate_rsi(df['Close'])
            df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
            
            latest = df.iloc[-1]
            close_price = float(latest['Close'])
            rsi = float(latest['RSI'])
            ema_200 = float(latest['EMA_200'])
            
            is_bear_market = close_price < ema_200
            is_etf = info.get("Type", "Stock").upper() == "ETF"
            name = info.get("Name", ticker)
            
            signal = {
                "ticker": ticker,
                "name": name,
                "close_price": close_price,
                "rsi": rsi,
                "ema_200": ema_200,
                "is_etf": is_etf,
                "is_bear_market": is_bear_market,
                "action_class": "action-wait",
                "action_badge": "HOLD",
                "explanation": "The stock is floating in the middle right now. Wait patiently.",
                "is_actionable": False,
                "type_category": "HOLD",
                "days_until_cat": 999,
                "pct": 0.0
            }
            
            # --- CHECK OPEN POSITIONS FOR SELL SIGNALS ---
            open_positions = [h for h in history_data if h['ticker'] == ticker and h.get('status', 'OPEN') == 'OPEN']
            has_sell_signal = False
            
            for pos in open_positions:
                days_held = (today_date - datetime.strptime(pos['date'], "%Y-%m-%d")).days
                sell_reason = None
                
                if "SHARES" in pos['action']:
                    if rsi > 70.0 and close_price >= pos['price']:
                        sell_reason = f"Profit target reached! RSI is extremely overbought (>70) and price is above your entry (${pos['price']:.2f}). Sell to lock in profits."
                elif "CALLS" in pos['action'] or "PUTS" in pos['action']:
                    if days_held >= 5:
                        sell_reason = f"Time to close the options. You've held for {days_held} days, and options lose value quickly to time decay. Cash out your position."

                if sell_reason:
                    has_sell_signal = True
                    signal["action_class"] = "action-sell"
                    signal["action_badge"] = "SELL TO CLOSE"
                    signal["explanation"] = f"<strong>EXIT SIGNAL:</strong> {sell_reason}"
                    signal["type_category"] = "SELL"
                    signal["is_actionable"] = True
                    pos['status'] = 'CLOSED'
                    pos['exit_date'] = today_str
                    pos['exit_price'] = round(close_price, 2)
            
            if has_sell_signal:
                signals.append(signal)
                continue

            # --- CHECK FOR NEW ENTRY SIGNALS ---
            if is_etf and rsi < 20.0:
                signal["action_class"] = "action-panic"
                signal["action_badge"] = "WAIT / DON't SELL"
                signal["explanation"] = "<strong>EXTREME PANIC DETECTED.</strong> RSI under 20. Do NOT sell. Hold for 30 days."
                signal["is_actionable"] = True
                signal["type_category"] = "PANIC"
            elif is_etf and rsi < 35.0 and not is_bear_market:
                signal["action_class"] = "action-buy"
                signal["action_badge"] = "BUY SHARES (15%)"
                signal["explanation"] = "<strong>OVERSOLD BOUNCE.</strong> Buy shares with 15% of your cash to catch the bounce."
                signal["is_actionable"] = True
                signal["type_category"] = "SHARES"
                signal["pct"] = 0.15
            elif is_etf and is_bear_market and rsi > 70.0:
                signal["action_class"] = "action-put"
                signal["action_badge"] = "BUY PUTS (2%)"
                signal["type_category"] = "PUTS"
                signal["pct"] = 0.02
                
                is_affordable = False
                contract_info = ""
                try:
                    exp_dates = stock.options
                    if exp_dates:
                        target_dt = datetime.now().date() + pd.Timedelta(days=7)
                        target_date = exp_dates[0]
                        for d in exp_dates:
                            if datetime.strptime(d, "%Y-%m-%d").date() >= target_dt:
                                target_date = d
                                break
                        
                        chain = stock.option_chain(target_date)
                        opts = chain.puts
                        otm_opts = opts[opts['strike'] <= close_price].sort_values(by='strike', ascending=False)
                        if not otm_opts.empty:
                            max_premium = (BASE_PYTHON_PORTFOLIO * 0.02) / 100.0
                            affordable_opts = otm_opts[otm_opts['lastPrice'] <= max_premium]
                            if not affordable_opts.empty:
                                best_opt = affordable_opts.iloc[0]
                                is_affordable = True
                                contract_info = f"<br><strong>Live Option Found:</strong> Contract <strong>{best_opt['contractSymbol']}</strong> (Strike: ${best_opt['strike']}) expiring {target_date} costs exactly <strong>${best_opt['lastPrice']:.2f} premium</strong> per share."
                except Exception as e:
                    pass
                
                if is_affordable:
                    signal["explanation"] = f"<strong>BEAR MARKET TRAP.</strong> Buy Put Options with 2% of cash to profit when it falls.{contract_info}"
                    signal["is_actionable"] = True
                else:
                    signal["action_class"] = "action-wait"
                    signal["action_badge"] = "SKIPPED (TOO EXPENSIVE)"
                    signal["explanation"] = f"<strong>PUT SKIPPED.</strong> {ticker} is overbought in a bear market, but all Put Option contracts exceed our safe $100 limit. Do not trade."
                    signal["is_actionable"] = False
                    signal["type_category"] = "HOLD"

            elif not is_etf and ticker in catalysts:
                cat = catalysts[ticker]
                days = cat.get('days_until', 0)
                if 0 <= days <= 14:
                    signal["action_class"] = "action-call"
                    signal["action_badge"] = "BUY CALLS (3%)"
                    signal["type_category"] = "CALLS"
                    signal["days_until_cat"] = days
                    signal["pct"] = 0.03
                    
                    is_affordable = False
                    contract_info = ""
                    try:
                        exp_dates = stock.options
                        if exp_dates:
                            target_dt = datetime.now().date() + pd.Timedelta(days=days)
                            target_date = exp_dates[0]
                            for d in exp_dates:
                                if datetime.strptime(d, "%Y-%m-%d").date() >= target_dt:
                                    target_date = d
                                    break
                            
                            chain = stock.option_chain(target_date)
                            opts = chain.calls
                            otm_opts = opts[opts['strike'] >= close_price].sort_values(by='strike')
                            if not otm_opts.empty:
                                max_premium = (BASE_PYTHON_PORTFOLIO * 0.03) / 100.0
                                affordable_opts = otm_opts[otm_opts['lastPrice'] <= max_premium]
                                if not affordable_opts.empty:
                                    best_opt = affordable_opts.iloc[0]
                                    is_affordable = True
                                    contract_info = f"<br><strong>Live Option Found:</strong> Contract <strong>{best_opt['contractSymbol']}</strong> (Strike: ${best_opt['strike']}) expiring {target_date} costs exactly <strong>${best_opt['lastPrice']:.2f} premium</strong> per share."
                    except Exception as e:
                        pass
                    
                    if is_affordable:
                        signal["explanation"] = f"<strong>MASSIVE CATALYST in {days} days.</strong> Buy Call Options with 3% of cash.{contract_info}"
                        signal["is_actionable"] = True
                    else:
                        signal["action_class"] = "action-wait"
                        signal["action_badge"] = "SKIPPED (TOO EXPENSIVE)"
                        signal["explanation"] = f"<strong>CATALYST SKIPPED.</strong> {ticker} has an event in {days} days, but all Call Option contracts exceed our safe $150 limit. Do not trade."
                        signal["is_actionable"] = False
                        signal["type_category"] = "HOLD"
            
            signals.append(signal)

        except Exception as e:
            pass

    # Phase 2: Selection Logic
    calls = [s for s in signals if s["type_category"] == "CALLS"]
    puts = [s for s in signals if s["type_category"] == "PUTS"]
    shares = [s for s in signals if s["type_category"] == "SHARES"]
    
    calls.sort(key=lambda x: x["days_until_cat"])
    puts.sort(key=lambda x: x["rsi"], reverse=True)
    shares.sort(key=lambda x: x["rsi"])
    
    selected_tickers = set()
    for s in calls[:2]: selected_tickers.add(s['ticker'])
    for s in puts[:1]: selected_tickers.add(s['ticker'])
    for s in shares[:1]: selected_tickers.add(s['ticker'])
    for s in signals:
        if s["type_category"] in ["PANIC", "SELL"]:
            selected_tickers.add(s['ticker'])

    for s in signals:
        s["starred"] = s['ticker'] in selected_tickers

    # Phase 3: Render HTML
    cards_html = ""
    todays_alerts = []

    for s in signals:
        star_html = '<span class="star-icon">⭐</span>' if s["starred"] else ''
        is_starred_str = 'true' if s["starred"] else 'false'
        
        risk_html = ""
        if s["is_actionable"] and s["type_category"] not in ["PANIC", "SELL"]:
            risk_html = '<div class="risk-box">Loading dynamic risk...</div>'

        card = f"""
        <div class="card {s['action_class']}" data-starred="{is_starred_str}" data-pct="{s['pct']}" data-price="{s['close_price']}" data-type="{s['type_category']}">
            <div class="ticker-header">
                <div>
                    <div class="ticker-symbol">{s['ticker']} {star_html}</div>
                    <div class="ticker-name">{s['name']}</div>
                </div>
                <div class="action-badge">{s['action_badge']}</div>
            </div>
            <div class="stats-grid">
                <div class="stat-item"><span class="stat-label">Price</span><span class="stat-value">${s['close_price']:.2f}</span></div>
                <div class="stat-item"><span class="stat-label">RSI</span><span class="stat-value">{s['rsi']:.1f}</span></div>
                <div class="stat-item"><span class="stat-label">200 EMA</span><span class="stat-value">${s['ema_200']:.2f}</span></div>
            </div>
            <div class="explanation">{s['explanation']}</div>
            {risk_html}
        </div>
        """
        cards_html += card

        if s["is_actionable"] and s["type_category"] != "SELL" and s["starred"]:
            if not any(h['date'] == today_str and h['ticker'] == s['ticker'] for h in history_data):
                todays_alerts.append({
                    "date": today_str,
                    "ticker": s['ticker'],
                    "action": s['action_badge'],
                    "action_class": s['action_class'],
                    "price": round(s['close_price'], 2),
                    "rsi": round(s['rsi'], 1),
                    "status": "OPEN",
                    "starred": s["starred"]
                })

    # Phase 4: History updates
    if todays_alerts or any(h.get('status') == 'CLOSED' and h.get('exit_date') == today_str for h in history_data):
        history_data.extend(todays_alerts)
        save_json(HISTORY_PATH, history_data)

    history_html = ""
    sorted_history = sorted(history_data, key=lambda x: x['date'], reverse=True)
    if not sorted_history:
        history_html = "<tr><td colspan='6' style='text-align:center;'>No history yet.</td></tr>"
    else:
        for item in sorted_history:
            bg = "rgba(255,255,255,0.1)"
            if "buy" in item.get('action_class', ''): bg = "var(--color-buy-glow)"
            elif "call" in item.get('action_class', ''): bg = "var(--color-call-glow)"
            elif "put" in item.get('action_class', ''): bg = "var(--color-put-glow)"
            
            status = item.get('status', 'OPEN')
            status_color = "#10b981" if status == "OPEN" else "#94a3b8"
            
            exit_info = "-"
            if status == "CLOSED":
                exit_pr = item.get('exit_price', 0)
                diff = exit_pr - item['price']
                sign = "+" if diff >= 0 else ""
                exit_info = f"Closed on {item.get('exit_date', 'Unknown')} at ${exit_pr} ({sign}{diff:.2f})"
                
            hist_star = "⭐ " if item.get("starred", False) else ""
                
            history_html += f"""
            <tr>
                <td>{item['date']}</td>
                <td style="font-weight: 600;">{hist_star}{item['ticker']}</td>
                <td><span style="background: {bg}; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.8rem; font-weight: bold;">{item['action']}</span></td>
                <td>${item['price']:.2f}</td>
                <td style="color: {status_color}; font-weight: bold;">{status}</td>
                <td style="color: #a1a1aa; font-size: 0.85rem;">{exit_info}</td>
            </tr>
            """

    generate_html(cards_html, history_html, today_str)

if __name__ == "__main__":
    run()
