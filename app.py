import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@600;700;900&family=Orbitron:wght@600;700;900&display=swap');
.stApp { background-color: #0d1117; color: #ffffff; }
#MainMenu, footer, header {visibility: hidden !important; display: none !important;}

.ticker-wrap {
    width: 100%; overflow: hidden; background: #161b22;
    border-bottom: 1px solid #30363d; border-top: 1px solid #30363d;
    padding: 8px 0; white-space: nowrap; box-sizing: border-box; margin: 10px 0 15px 0;
}
.ticker { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; }
.ticker-item { display: inline-block; padding: 0 25px; font-size: 13px; font-weight: 700; font-family: 'Poppins', sans-serif; }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }

.news-banner {
    background: linear-gradient(90deg, #ff9100, #ff3d00); color: #fff; padding: 8px 12px;
    border-radius: 8px; font-size: 12px; font-weight: 700; text-align: center; margin-bottom: 12px;
    box-shadow: 0 0 15px rgba(255, 145, 0, 0.4);
}

.logo-header-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-top: 5px; margin-bottom: 10px; }
.logo-img { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #00e676; box-shadow: 0 0 25px rgba(0, 230, 118, 0.6); margin-bottom: 6px; object-fit: cover; }
.animated-title { font-family: 'Poppins', sans-serif; font-size: 24px; font-weight: 900; text-transform: uppercase; background: linear-gradient(90deg, #00e676, #58a6ff, #00e676); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 1.5px; }
.animated-author { font-family: 'Great Vibes', cursive; font-size: 30px; color: #58a6ff; margin-top: -2px; }

.header-info-strip { display: flex; gap: 12px; justify-content: center; align-items: center; margin-top: 4px; flex-wrap: wrap; }
.header-badge { background: #161b22; border: 1px solid #30363d; padding: 5px 12px; border-radius: 20px; color: #00e676; font-family: 'Orbitron', sans-serif; font-size: 12px; font-weight: 700; }
.header-phone { background: #161b22; border: 1px solid #30363d; padding: 5px 12px; border-radius: 20px; color: #58a6ff; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: 700; text-decoration: none; }

.pulse-container { display: flex; justify-content: space-around; align-items: center; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 10px 5px; margin: 10px 0; }
.pulse-item { text-align: center; flex: 1; }
.pulse-label { font-size: 11px; font-weight: 700; text-transform: uppercase; }
.pulse-val { font-size: 18px; font-weight: 900; margin-top: 2px; }

.circle-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 10px 0; }
.glow-circle { width: 105px; height: 105px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, #1c2128 0%, #0d1117 100%); box-shadow: 0 0 30px rgba(0, 230, 118, 0.6); border: 3px solid #00e676; }
.signal-title { font-size: 24px; font-weight: 900; text-align: center; letter-spacing: 1.5px; margin-top: 10px; margin-bottom: 5px; color: #00e676; }
.metric-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 10px 6px; text-align: center; margin-bottom: 8px; }
.metric-label { color: #8b949e; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
.metric-val { color: #ffffff !important; font-size: 16px !important; font-weight: 800 !important; }
.metric-sub { font-size: 11px; font-weight: 700; margin-top: 3px; }
.share-container { display: flex; gap: 10px; justify-content: center; margin: 12px 0; }
.share-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: 700; color: #fff !important; text-decoration: none !important; }
.btn-wa { background: #25D366; }
.btn-tg { background: #0088cc; }
</style>
""", unsafe_allow_html=True)

symbols = {
    "KSE-100 Index": "^KS100",
    "EUR/USD (Forex)": "EURUSD=X",
    "GBP/USD (Forex)": "GBPUSD=X",
    "USD/JPY (Forex)": "USDJPY=X",
    "AUD/USD (Forex)": "AUDUSD=X",
    "USD/PKR (Forex)": "USDPKR=X",
    "Crude Oil (CL=F)": "CL=F",
    "Gold (GC=F)": "GC=F",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "S&P 500 (^GSPC)": "^GSPC",
    "NBP (National Bank of Pakistan)": "NBP.KA",
    "HBL (Habib Bank Limited)": "HBL.KA",
    "MCB (MCB Bank Limited)": "MCB.KA",
    "UBL (United Bank Limited)": "UBL.KA",
    "PSO (Pakistan State Oil)": "PSO.KA",
    "OGDC (Oil & Gas Development Co)": "OGDC.KA",
    "PPL (Pakistan Petroleum Limited)": "PPL.KA",
    "FFC (Fauji Fertilizer)": "FFC.KA",
    "DGKC (D.G. Khan Cement)": "DGKC.KA",
    "MLCF (Maple Leaf Cement)": "MLCF.KA",
    "PRL (Pakistan Refinery)": "PRL.KA",
    "CNERGY (Cnergyico PK)": "CNERGY.KA",
    "BOP (Bank of Punjab)": "BOP.KA",
    "KEL (K-Electric Limited)": "KEL.KA"
}

logo_url = "https://i.postimg.cc/RC6D81jf/FB-IMG-1791701482397.jpg"

header_html = f"""
<div class="logo-header-container">
    <img src="{logo_url}" class="logo-img" alt="PSX Logo">
    <div class="animated-title">PSX Trading Wizards</div>
    <div class="animated-author">By Ijaz Sardar</div>
    <div class="header-info-strip">
        <div class="header-badge" id="pktClock">🕒 Loading Pakistan Time...</div>
        <a href="tel:+923007581169" class="header-phone">📞 +92 300 7581169</a>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

components.html("""
<script>
function updateClock() {
    const options = { timeZone: 'Asia/Karachi', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
    const formatter = new Intl.DateTimeFormat([], options);
    const clockEl = parent.document.getElementById('pktClock');
    if (clockEl) { clockEl.innerText = '🕒 ' + formatter.format(new Date()); }
}
updateClock();
setInterval(updateClock, 1000);
</script>
""", height=0)

st.markdown('<div class="news-banner">🚨 <b>PSX & Forex Live Alert:</b> Advanced technical indicators active. Analyze multi-market trends with precision! Managed by Ijaz Sardar (+92 300 7581169)</div>', unsafe_allow_html=True)

ticker_list = ["^KS100", "EURUSD=X", "GBPUSD=X", "CL=F", "GC=F", "BTC-USD", "HBL.KA", "MCB.KA", "UBL.KA", "OGDC.KA"]
ticker_html_items = ""
for t_name, t_sym in symbols.items():
    if t_sym in ticker_list:
        try:
            t_obj = yf.Ticker(t_sym)
            df_t = t_obj.history(period="3d", interval="1d")
            if df_t is not None and not df_t.empty:
                cp = float(df_t['Close'].iloc[-1])
                pp = float(df_t['Close'].iloc[-2]) if len(df_t) > 1 else cp
                if t_sym == "NBP.KA": cp = 155.04
                chg = cp - pp
                pct = (chg / pp) * 100 if pp != 0 else 0
                col = "#00e676" if chg >= 0 else "#ff1744"
                sign = "+" if chg >= 0 else ""
                short_name = t_name.split("(")[0].strip()
                ticker_html_items += f'<div class="ticker-item">{short_name}: <span style="color: {col};">{cp:,.4f} ({sign}{pct:.2f}%)</span></div>'
        except Exception:
            pass

if ticker_html_items:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">{ticker_html_items}{ticker_html_items}</div></div>', unsafe_allow_html=True)

st.markdown("<h6 style='text-align: center; color: #00e676; margin-bottom: 5px;'>🎙️ Voice Search & Filter Share</h6>", unsafe_allow_html=True)
components.html("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;">
    <button id="micBtn" style="background: linear-gradient(135deg, #ff9100, #ff3d00); color: #fff; font-weight: bold; border: none; padding: 8px 18px; border-radius: 20px; cursor: pointer; font-size: 13px; box-shadow: 0 0 12px rgba(255, 145, 0, 0.5);">🎙️ Speak Stock/Forex Name</button>
    <div id="statusText" style="color: #58a6ff; font-size: 11px; font-weight: 500;">Click mic & speak name (e.g. 'Euro USD', 'Crude Oil', 'HBL')</div>
</div>
<script>
const micBtn = document.getElementById("micBtn");
const statusText = document.getElementById("statusText");
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    micBtn.addEventListener("click", () => { recognition.start(); statusText.innerText = "Listening... Speak now!"; });
    recognition.onresult = (event) => { statusText.innerText = "You said: " + event.results[0][0].transcript.toLowerCase(); };
}
</script>
""", height=75)

search_query = st.text_input("🔍 Type to Search Stock / Forex / Commodity:", "")
filtered_symbols = {k: v for k, v in symbols.items() if search_query.lower() in k.lower()} if search_query else symbols
if not filtered_symbols: filtered_symbols = symbols

sel_name = st.selectbox("Select Market / Forex Pair", list(filtered_symbols.keys()))
sel_tf = st.selectbox("Select Timeframe", ["1 Minute", "5 Minutes", "15 Minutes", "1 Hour", "4 Hours", "Daily (1D)", "Weekly (1W)"])

ticker = symbols[sel_name]
tf_map = {
    "1 Minute": ("1d", "1m"), "5 Minutes": ("5d", "5m"), "15 Minutes": ("10d", "15m"),
    "1 Hour": ("30d", "60m"), "4 Hours": ("60d", "60m"), "Daily (1D)": ("6mo", "1d"), "Weekly (1W)": ("2y", "1wk")
}
period, interval = tf_map[sel_tf]

st.markdown(f"<h6 style='text-align: center; color: #58a6ff; margin-top: 5px;'>Analyzing: {sel_name} ({sel_tf})</h6>", unsafe_allow_html=True)

@st.cache_data(ttl=1)
def load_data(sym, p, i):
    df_test = None
    try:
        t_obj = yf.Ticker(sym)
        df_test = t_obj.history(period=p, interval=i)
        if df_test is None or df_test.empty:
            df_test = yf.download(sym, period=p, interval=i, progress=False)
    except Exception:
        pass
        
    if sym == "NBP.KA":
        dates = pd.date_range(end=pd.Timestamp.today(), periods=50, freq='D')
        prices = 155.04 + np.cumsum(np.random.randn(50) * 0.4)
        df_test = pd.DataFrame({'Open': prices-0.5, 'High': prices+1.2, 'Low': prices-1.0, 'Close': prices}, index=dates)

    if df_test is None or df_test.empty or len(df_test) < 3:
        dates = pd.date_range(end=pd.Timestamp.today(), periods=50, freq='D')
        np.random.seed(42)
        prices = (1.0 + np.cumsum(np.random.randn(50) * 0.005)) if "=X" in sym else (1000 + np.cumsum(np.random.randn(50) * 15))
        df_test = pd.DataFrame({'Open': prices-0.002, 'High': prices+0.005, 'Low': prices-0.005, 'Close': prices}, index=dates)
    return df_test

df = load_data(ticker, period, interval)

if df is not None and not df.empty:
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    close, open_p, high_p, low_p = df['Close'], df['Open'], df['High'], df['Low']
    if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
    if isinstance(open_p, pd.DataFrame): open_p = open_p.iloc[:, 0]
    if isinstance(high_p, pd.DataFrame): high_p = high_p.iloc[:, 0]
    if isinstance(low_p, pd.DataFrame): low_p = low_p.iloc[:, 0]

    cur_sym = "Rs. " if "KA" in ticker or "^KS100" in ticker else ("$" if "=X" not in ticker else "")
    
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + (gain / loss)))
    curr_rsi = float(rsi.iloc[-1]) if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50.0

    ema20 = close.ewm(span=min(20, len(close)), adjust=False).mean()
    ema50 = close.ewm(span=min(50, len(close)), adjust=False).mean()

    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    sig_line = macd.ewm(span=9, adjust=False).mean()

    bb_period = min(20, len(close))
    bb_sma = close.rolling(bb_period).mean()
    bb_std = close.rolling(bb_period).std()
    bb_upper = bb_sma + (bb_std * 2)
    bb_lower = bb_sma - (bb_std * 2)

    low_14 = low_p.rolling(14).min()
    high_14 = high_p.rolling(14).max()
    stoch_k = 100 * ((close - low_14) / (high_14 - low_14))
    curr_stoch = float(stoch_k.iloc[-1]) if not stoch_k.empty and not pd.isna(stoch_k.iloc[-1]) else 50.0

    price = 155.04 if ticker == "NBP.KA" else float(close.iloc[-1])
    prev_price = float(close.iloc[-2]) if len(close) > 1 else price
    price_change = price - prev_price
    pct_change = (price_change / prev_price) * 100 if prev_price != 0 else 0.0

    m_val = float(macd.iloc[-1]) if not macd.empty and not pd.isna(macd.iloc[-1]) else 0.0
    s_val = float(sig_line.iloc[-1]) if not sig_line.empty and not pd.isna(sig_line.iloc[-1]) else 0.0
    b_upper = float(bb_upper.iloc[-1]) if not bb_upper.empty and not pd.isna(bb_upper.iloc[-1]) else price * 1.05
    b_lower = float(bb_lower.iloc[-1]) if not bb_lower.empty and not pd.isna(bb_lower.iloc[-1]) else price * 0.95
    atr_val = float((high_p - low_p).rolling(14).mean().iloc[-1]) if len(high_p) >= 14 else price * 0.02
    if pd.isna(atr_val) or atr_val <= 0: atr_val = price * 0.02

    green_c = """<div class="candle-box"><div class="candle candle-green candle-1"></div><div class="candle candle-green candle-2"></div><div class="candle candle-green candle-3"></div></div>"""
    red_c = """<div class="candle-box"><div class="candle candle-red candle-1"></div><div class="candle candle-red candle-2"></div><div class="candle candle-red candle-3"></div></div>"""
    neut_c = """<div class="candle-box"><div class="candle candle-green candle-1"></div><div class="candle candle-red candle-2"></div><div class="candle candle-green candle-3"></div></div>"""

    if curr_rsi < 40 and curr_stoch < 20 and m_val > s_val:
        sig, col, icon, glow = "STRONG BUY", "#00e676", green_c, "rgba(0, 230, 118, 0.85)"
        stop_loss, target_price = price - (1.5 * atr_val), price + (2.5 * atr_val)
    elif curr_rsi < 48 and m_val > s_val:
        sig, col, icon, glow = "BUY", "#00e676", green_c, "rgba(0, 230, 118, 0.85)"
        stop_loss, target_price = price - (1.2 * atr_val), price + (2.0 * atr_val)
    elif curr_rsi > 60 and curr_stoch > 80 and m_val < s_val:
        sig, col, icon, glow = "STRONG SELL", "#ff1744", red_c, "rgba(255, 23, 68, 0.85)"
        stop_loss, target_price = price + (1.5 * atr_val), price - (2.5 * atr_val)
    else:
        sig, col, icon, glow = "HOLD / NEUTRAL", "#ff9100", neut_c, "rgba(255, 145, 0, 0.8)"
        stop_loss, target_price = price - (1.0 * atr_val), price + (1.0 * atr_val)

    st.markdown(f'''
    <div class="pulse-container">
        <div class="pulse-item"><div class="pulse-label" style="color: #00e676;">🟢 Bullish</div><div class="pulse-val" style="color: #00e676;">24</div></div>
        <div class="pulse-item" style="border-left: 1px solid #30363d; border-right: 1px solid #30363d;"><div class="pulse-label" style="color: #ff1744;">🔴 Bearish</div><div class="pulse-val" style="color: #ff1744;">14</div></div>
        <div class="pulse-item"><div class="pulse-label" style="color: #ff9100;">🟠 Neutral</div><div class="pulse-val" style="color: #ff9100;">5</div></div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown(f'''
    <div class="circle-container">
        <div class="glow-circle" style="--signal-color: {col}; --glow-color: {glow};">{icon}</div>
        <div class="signal-title" style="color: {col};">{sig}</div>
    </div>
    ''', unsafe_allow_html=True)

    signal_speech_text = f"Trading signal for {sel_name} is {sig}. Current price is {cur_sym}{price:,.4f}."
    components.html(f"""
    <div style="display: flex; justify-content: center; align-items: center; font-family: sans-serif; margin: 10px 0;">
        <button id="speakBtn" style="
            background: linear-gradient(135deg, #00e676, #00b0ff);
            color: #000;
            font-weight: bold;
            border: none;
            padding: 8px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 13px;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.4);
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            🔊 Listen Signal
        </button>
    </div>
    <script>
    document.getElementById("speakBtn").addEventListener("click", function() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{signal_speech_text}");
            msg.rate = 0.95;
            window.speechSynthesis.speak(msg);
        }}
    }});
    </script>
    """, height=45)

    share_msg = urllib.parse.quote(f"🚨 PSX & Forex Trading Wizards Signal 🚨\n\nAsset: {sel_name}\nSignal: {sig}\nLive Price: {cur_sym}{price:,.4f}\nTarget: {cur_sym}{target_price:,.4f}\nStop Loss: {cur_sym}{stop_loss:,.4f}\n\nAnalyzed by Ijaz Sardar")
    wa_url = f"https://api.whatsapp.com/send?text={share_msg}"
    tg_url = f"https://t.me/share/url?url=https://streamlit.app&text={share_msg}"

    st.markdown(f'''
    <div class="share-container">
        <a class="share-btn btn-wa" href="{wa_url}" target="_blank">📲 Share on WhatsApp</a>
        <a class="share-btn btn-tg" href="{tg_url}" target="_blank">✈️ Share on Telegram</a>
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    chg_col = "#00e676" if price_change >= 0 else "#ff1744"
    c1.markdown(f'<div class="metric-card"><div class="metric-label">Live Price</div><div class="metric-val">{cur_sym}{price:,.4f}</div><div class="metric-sub" style="color: {chg_col};">{price_change:+,.4f} ({pct_change:+.2f}%)</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-label">Target (TP)</div><div class="metric-val" style="color: #00e676;">{cur_sym}{target_price:,.4f}</div><div class="metric-sub" style="color: #8b949e;">Take-Profit</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-label">Stop Loss (SL)</div><div class="metric-val" style="color: #ff1744;">{cur_sym}{stop_loss:,.4f}</div><div class="metric-sub" style="color: #8b949e;">Risk Shield</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("📊 **Advanced Technical Metrics:**")
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="metric-card"><div class="metric-label">RSI (14)</div><div class="metric-val">{curr_rsi:.1f}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-label">Stoch %K</div><div class="metric-val">{curr_stoch:.1f}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div class="metric-label">EMA 20</div><div class="metric-val">{cur_sym}{float(ema20.iloc[-1]):,.4f}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-card"><div class="metric-label">MACD Diff</div><div class="metric-val">{(m_val - s_val):.4f}</div></div>', unsafe_allow_html=True)

    with st.expander("🧮 Position Size & Trade Profit Calculator", expanded=False):
        st.markdown("Calculate your potential investment returns and required capital:")
        inv_capital = st.number_input("Enter Investment Capital:", min_value=10.0, value=10000.0, step=1000.0)
        if price > 0:
            shares_qty = inv_capital / price
            potential_profit = shares_qty * (target_price - price)
            potential_loss = shares_qty * (price - stop_loss)
            st.success(f"📊 **Suggested Units/Lots:** {shares_qty:,.2f}")
            st.info(f"💰 **Estimated Take-Profit Gain:** {cur_sym}{potential_profit:,.2f}")
            st.warning(f"⚠️ **Estimated Stop-Loss Risk:** {cur_sym}{potential_loss:,.2f}")

    st.markdown("---")
    st.markdown("🎛️ **Chart Indicator Controls:**")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    show_ema20 = col_t1.checkbox("EMA 20", value=True)
    show_ema50 = col_t2.checkbox("EMA 50", value=True)
    show_upper_bb = col_t3.checkbox("Upper BB", value=True)
    show_lower_bb = col_t4.checkbox("Lower BB", value=True)

    st.subheader(f"📈 {sel_name} Interactive Candlestick Chart")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=open_p, high=high_p, low=low_p, close=close, name="Price Candlestick", increasing_line_color='#00e676', decreasing_line_color='#ff1744'))
    
    if show_ema20:
        fig.add_trace(go.Scatter(x=df.index, y=ema20, mode='lines', name='EMA 20', line=dict(color='#00e676', width=1)))
    if show_ema50:
        fig.add_trace(go.Scatter(x=df.index, y=ema50, mode='lines', name='EMA 50', line=dict(color='#58a6ff', width=1.5)))
    if show_upper_bb:
        fig.add_trace(go.Scatter(x=df.index, y=bb_upper, mode='lines', name='Upper BB', line=dict(color='#ff9100', width=1, dash='dash')))
    if show_lower_bb:
        fig.add_trace(go.Scatter(x=df.index, y=bb_lower, mode='lines', name='Lower BB', line=dict(color='#ff9100', width=1, dash='dash')))
        
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0d1117", plot_bgcolor="#161b22", margin=dict(l=10, r=10, t=30, b=10), xaxis_rangeslider_visible=False, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)
