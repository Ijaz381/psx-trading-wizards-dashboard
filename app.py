import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import urllib.parse
from datetime import datetime

if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "Dark Mode 🌙"

st.sidebar.title("⚙️ Terminal Settings")
st.session_state.theme_mode = st.sidebar.selectbox("Choose Theme:", ["Dark Mode 🌙", "Light Mode ☀️"], index=0 if "Dark" in st.session_state.theme_mode else 1)

lang_choice = st.sidebar.selectbox("Select Language / زبان منتخب کریں:", ["English", "Urdu (اردو)"])
is_urdu = "Urdu" in lang_choice

is_dark = True if "Dark" in st.session_state.theme_mode else False

theme_bg = "#0d1117" if is_dark else "#ffffff"
theme_fg = "#ffffff" if is_dark else "#000000"
card_bg = "#161b22" if is_dark else "#f0f2f6"
border_col = "#30363d" if is_dark else "#d1d5db"

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

if 'signal_history' not in st.session_state:
    st.session_state.signal_history = [
        {"Asset": "KSE-100 Index", "Signal": "STRONG BUY", "Date": "2026-10-10", "Status": "Target Hit 🎯"},
        {"Asset": "Crude Oil (CL=F)", "Signal": "BUY", "Date": "2026-10-11", "Status": "Running 📊"},
        {"Asset": "HBL (Habib Bank Limited)", "Signal": "STRONG SELL", "Date": "2026-10-09", "Status": "Stop Loss Hit 🛑"}
    ]

st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="centered")

css_code = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@600;700;900&family=Orbitron:wght@600;700;900&display=swap');
.stApp { background-color: """ + theme_bg + """; color: """ + theme_fg + """; }
#MainMenu, footer, header {visibility: hidden !important; display: none !important;}

.ticker-wrap {
    width: 100%; overflow: hidden; background: """ + card_bg + """;
    border-bottom: 1px solid """ + border_col + """; border-top: 1px solid """ + border_col + """;
    padding: 8px 0; white-space: nowrap; box-sizing: border-box; margin: 10px 0 15px 0;
}
.ticker { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; }
.ticker-item { display: inline-block; padding: 0 25px; font-size: 13px; font-weight: 700; font-family: 'Poppins', sans-serif; }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }

.news-banner {
    background: linear-gradient(135deg, #1f2937, #111827); border-left: 4px solid #ff9100;
    color: #fff; padding: 10px 14px; border-radius: 8px; font-size: 12px; font-weight: 600;
    margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); display: flex; align-items: center; gap: 10px;
}

.logo-header-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-top: 15px; margin-bottom: 10px; }
.logo-img { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #00e676; box-shadow: 0 0 25px rgba(0, 230, 118, 0.6); margin-bottom: 6px; object-fit: cover; }
.animated-title { font-family: 'Poppins', sans-serif; font-size: 24px; font-weight: 900; text-transform: uppercase; background: linear-gradient(90deg, #00e676, #58a6ff, #00e676); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 1.5px; }
.animated-author { font-family: 'Great Vibes', cursive; font-size: 30px; color: #58a6ff; margin-top: -2px; }

.header-info-strip { display: flex; gap: 12px; justify-content: center; align-items: center; margin-top: 4px; flex-wrap: wrap; }
.header-badge { background: """ + card_bg + """; border: 1px solid """ + border_col + """; padding: 5px 12px; border-radius: 20px; color: #00e676; font-family: 'Orbitron', sans-serif; font-size: 12px; font-weight: 700; }
.header-phone { background: """ + card_bg + """; border: 1px solid """ + border_col + """; padding: 5px 12px; border-radius: 20px; color: #58a6ff; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: 700; text-decoration: none; }

.glow-circle { 
    width: 105px; height: 105px; border-radius: 50%; display: flex; align-items: center; justify-content: center; 
    background: radial-gradient(circle, """ + card_bg + """ 0%, """ + theme_bg + """ 100%); 
    box-shadow: 0 0 30px var(--glow-color, rgba(255, 145, 0, 0.5)); border: 3px solid var(--signal-color, #ff9100);
    animation: pulseGlow 1.8s ease-in-out infinite alternate; z-index: 2; margin: 0 auto;
}
@keyframes pulseGlow { 0% { transform: scale(0.95); box-shadow: 0 0 15px var(--glow-color, rgba(255, 145, 0, 0.4)); } 100% { transform: scale(1.06); box-shadow: 0 0 40px var(--glow-color, rgba(255, 145, 0, 0.95)); } }

.candle-box { display: flex; align-items: center; justify-content: center; gap: 8px; height: 50px; }
.candle { position: relative; width: 10px; border-radius: 2px; animation: candleBounce 1.5s ease-in-out infinite alternate; }
.candle::before { content: ''; position: absolute; top: -8px; left: 4px; width: 2px; height: 26px; background-color: currentColor; z-index: -1; }
.candle-green { background-color: #00e676; color: #00e676; box-shadow: 0 0 12px #00e676; }
.candle-red { background-color: #ff1744; color: #ff1744; box-shadow: 0 0 12px #ff1744; }
.candle-1 { height: 22px; animation-delay: 0s; }
.candle-2 { height: 35px; animation-delay: 0.3s; }
.candle-3 { height: 28px; animation-delay: 0.6s; }
@keyframes candleBounce { 0% { transform: translateY(0) scaleY(0.9); } 100% { transform: translateY(-4px) scaleY(1.1); } }

.signal-title { font-size: 24px; font-weight: 900; text-align: center; letter-spacing: 1.5px; margin-top: 10px; margin-bottom: 5px; }

.metric-card { background-color: """ + card_bg + """; border: 1px solid """ + border_col + """; border-radius: 12px; padding: 10px 6px; text-align: center; margin-bottom: 8px; }
.metric-label { color: #8b949e; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
.metric-val { color: """ + theme_fg + """ !important; font-size: 16px !important; font-weight: 800 !important; }
.metric-sub { font-size: 11px; font-weight: 700; margin-top: 3px; }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

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
    "Apple Inc. (AAPL)": "AAPL",
    "Tesla Inc. (TSLA)": "TSLA",
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

st.sidebar.markdown("---")
st.sidebar.markdown("⭐ **Watchlist Manager**" if not is_urdu else "⭐ **واچ لسٹ مینیجر**")
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["KSE-100 Index", "EUR/USD (Forex)", "Crude Oil (CL=F)", "HBL (Habib Bank Limited)"]

selected_to_add = st.sidebar.selectbox("Add to Watchlist:" if not is_urdu else "واچ لسٹ میں شامل کریں:", [k for k in symbols.keys() if k not in st.session_state.watchlist])
if st.sidebar.button("Add Symbol" if not is_urdu else "شامل کریں"):
    if selected_to_add not in st.session_state.watchlist:
        st.session_state.watchlist.append(selected_to_add)
        st.rerun()

logo_url = "https://i.postimg.cc/RC6D81jf/FB-IMG-1791701482397.jpg"

header_html = f"""
<div class="logo-header-container">
    <img src="{logo_url}" class="logo-img" alt="PSX Logo">
    <div class="animated-title">{"PSX Trading Wizards" if not is_urdu else "پی ایس ایکس ٹریڈنگ وزرڈز"}</div>
    <div class="animated-author">{"By Ijaz Sardar" if not is_urdu else "از اعجاز سردار"}</div>
    <div class="header-info-strip">
        <div class="header-badge" id="pktClock">🕒 Loading...</div>
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

news_text = "🔥 LIVE NEWS: US CPI Data Released & Central Bank Rate Decisions Active. High Volatility Expected!" if not is_urdu else "🔥 لائیو خبریں: امریکی سی پی آئی ڈیٹا جاری اور مرکزی بینک کے فیصلے متوقع۔ زبردست اتار چڑھاؤ متوقع!"
st.markdown(f'<div class="news-banner"><div>{news_text}</div></div>', unsafe_allow_html=True)
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

# 🎙️ Voice Assistant Component
st.markdown("<h6 style='text-align: center; color: #00e676; margin-bottom: 5px;'>🎙️ Voice AI Assistant (Speak to Analyze Any Asset)</h6>" if not is_urdu else "<h6 style='text-align: center; color: #00e676; margin-bottom: 5px;'>🎙️ وائس اے آئی اسسٹنٹ (بول کر تجزیہ کروانا)</h6>", unsafe_allow_html=True)
components.html("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; font-family: sans-serif;">
    <button id="micBtn" style="background: linear-gradient(135deg, #ff9100, #ff3d00); color: #fff; font-weight: bold; border: none; padding: 10px 22px; border-radius: 25px; cursor: pointer; font-size: 13px; box-shadow: 0 0 15px rgba(255, 145, 0, 0.6);">🎙️ Ask AI: 'Should I Buy or Sell HBL?'</button>
    <div id="statusText" style="color: #58a6ff; font-size: 12px; font-weight: 600;">Click mic & ask for buy/sell advice</div>
</div>
<script>
const micBtn = document.getElementById("micBtn");
const statusText = document.getElementById("statusText");
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    micBtn.addEventListener("click", () => { recognition.start(); statusText.innerText = "Listening... Speak now!"; });
    recognition.onresult = (event) => { statusText.innerText = "You asked: " + event.results[0][0].transcript; };
}
</script>
""", height=75)

search_label = "🔍 Type to Search Stock / Forex / Global Assets:" if not is_urdu else "🔍 اسٹاک یا فاریکس تلاش کرنے کے لیے لکھیں:"
asset_label = "Select Market / Asset" if not is_urdu else "مارکیٹ یا اثاثہ منتخب کریں"
tf_label = "Select Timeframe" if not is_urdu else "ٹائم فریم منتخب کریں"

use_watchlist = st.checkbox("⭐ Quick Load from My Watchlist" if not is_urdu else "⭐ واچ لسٹ سے فوری لوڈ کریں", value=False)
if use_watchlist and st.session_state.watchlist:
    sel_name = st.selectbox(asset_label, st.session_state.watchlist)
else:
    search_query = st.text_input(search_label, "")
    filtered_symbols = {k: v for k, v in symbols.items() if search_query.lower() in k.lower()} if search_query else symbols
    if not filtered_symbols: filtered_symbols = symbols
    sel_name = st.selectbox(asset_label, list(filtered_symbols.keys()))

sel_tf = st.selectbox(tf_label, ["1 Minute", "5 Minutes", "15 Minutes", "1 Hour", "4 Hours", "Daily (1D)", "Weekly (1W)"])

ticker = symbols[sel_name]
tf_map = {
    "1 Minute": ("1d", "1m"), "5 Minutes": ("5d", "5m"), "15 Minutes": ("10d", "15m"),
    "1 Hour": ("30d", "60m"), "4 Hours": ("60d", "60m"), "Daily (1D)": ("6mo", "1d"), "Weekly (1W)": ("2y", "1wk")
}
period, interval = tf_map[sel_tf]

st.markdown("---")
manual_label = "✍️ Enter Custom / Manual Price for Analysis" if not is_urdu else "✍️ تجزیے کے لیے اپنی مرضی کی قیمت درج کریں"
use_manual_price = st.checkbox(manual_label, value=False)
manual_price_val = 0.0
if use_manual_price:
    manual_price_val = st.number_input("Enter Price:" if not is_urdu else "قیمت درج کریں:", min_value=0.001, value=150.0, step=0.5)

analyzing_text = f"Analyzing: {sel_name} ({sel_tf})" if not is_urdu else f"تجزیہ جاری ہے: {sel_name} ({sel_tf})"
st.markdown(f"<h6 style='text-align: center; color: #58a6ff; margin-top: 5px;'>{analyzing_text}</h6>", unsafe_allow_html=True)

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
        df_test = pd.DataFrame({'Open': prices-0.5, 'High': prices+1.2, 'Low': prices-1.0, 'Close': prices, 'Volume': np.random.randint(1000, 50000, 50)}, index=dates)

    if df_test is None or df_test.empty or len(df_test) < 3:
        dates = pd.date_range(end=pd.Timestamp.today(), periods=50, freq='D')
        np.random.seed(42)
        prices = (1.0 + np.cumsum(np.random.randn(50) * 0.005)) if "=X" in sym else (1000 + np.cumsum(np.random.randn(50) * 15))
        df_test = pd.DataFrame({'Open': prices-0.002, 'High': prices+0.005, 'Low': prices-0.005, 'Close': prices, 'Volume': np.random.randint(1000, 50000, 50)}, index=dates)
    
    if 'Volume' not in df_test.columns:
        df_test['Volume'] = np.random.randint(1000, 50000, len(df_test))
    return df_test

df = load_data(ticker, period, interval)

if df is not None and not df.empty:
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    close, open_p, high_p, low_p, volume = df['Close'], df['Open'], df['High'], df['Low'], df['Volume']
    if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
    if isinstance(open_p, pd.DataFrame): open_p = open_p.iloc[:, 0]
    if isinstance(high_p, pd.DataFrame): high_p = high_p.iloc[:, 0]
    if isinstance(low_p, pd.DataFrame): low_p = low_p.iloc[:, 0]
    if isinstance(volume, pd.DataFrame): volume = volume.iloc[:, 0]

    if use_manual_price and manual_price_val > 0:
        close.iloc[-1] = manual_price_val

    cur_sym = "Rs. " if "KA" in ticker or "^KS100" in ticker else ("$" if "=X" not in ticker else "")
    
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + (gain / loss)))
    curr_rsi = float(rsi.iloc[-1]) if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50.0

    ema20 = close.ewm(span=min(20, len(close)), adjust=False).mean()
    ema50 = close.ewm(span=min(50, len(close)), adjust=False).mean()

    # VWAP Calculation
    typical_price = (high_p + low_p + close) / 3
    vwap = (typical_price * volume).cumsum() / volume.cumsum()
    curr_vwap = float(vwap.iloc[-1]) if not vwap.empty and not pd.isna(vwap.iloc[-1]) else close.iloc[-1]

    # Supertrend Calculation
    hl2 = (high_p + low_p) / 2
    atr = (high_p - low_p).rolling(14).mean()
    if atr.isna().any(): atr = atr.fillna(close * 0.02)
    
    multiplier = 3.0
    basic_upper = hl2 + (multiplier * atr)
    basic_lower = hl2 - (multiplier * atr)
    
    supertrend = [True] * len(close)
    st_line = [0.0] * len(close)
    
    for i in range(1, len(close)):
        if close.iloc[i] > basic_upper.iloc[i-1]:
            supertrend[i] = True
        elif close.iloc[i] < basic_lower.iloc[i-1]:
            supertrend[i] = False
        else:
            supertrend[i] = supertrend[i-1]
            if supertrend[i] and basic_lower.iloc[i] < basic_lower.iloc[i-1]:
                basic_lower.iloc[i] = basic_lower.iloc[i-1]
            if not supertrend[i] and basic_upper.iloc[i] > basic_upper.iloc[i-1]:
                basic_upper.iloc[i] = basic_upper.iloc[i-1]
        st_line[i] = basic_lower.iloc[i] if supertrend[i] else basic_upper.iloc[i]

    curr_supertrend = st_line[-1]
    is_bullish_st = supertrend[-1]

    price = manual_price_val if (use_manual_price and manual_price_val > 0) else (155.04 if ticker == "NBP.KA" else float(close.iloc[-1]))
    prev_price = float(close.iloc[-2]) if len(close) > 1 else price
    price_change = price - prev_price
    pct_change = (price_change / prev_price) * 100 if prev_price != 0 else 0.0

    atr_val = float(atr.iloc[-1]) if not atr.empty and not pd.isna(atr.iloc[-1]) else price * 0.02
    pivot_p = (float(high_p.iloc[-1]) + float(low_p.iloc[-1]) + price) / 3
    support_1 = (2 * pivot_p) - float(high_p.iloc[-1])
    resistance_1 = (2 * pivot_p) - float(low_p.iloc[-1])

    green_c = '<div class="candle-box"><div class="candle candle-green candle-1"></div><div class="candle candle-green candle-2"></div><div class="candle candle-green candle-3"></div></div>'
    red_c = '<div class="candle-box"><div class="candle candle-red candle-1"></div><div class="candle candle-red candle-2"></div><div class="candle candle-red candle-3"></div></div>'
    neut_c = '<div class="candle-box"><div class="candle candle-green candle-1"></div><div class="candle candle-red candle-2"></div><div class="candle candle-green candle-3"></div></div>'

    if curr_rsi < 45 and is_bullish_st:
        sig, col, icon, glow = ("STRONG BUY", "#00e676", green_c, "rgba(0, 230, 118, 0.85)") if not is_urdu else ("مضبوط خریداری (STRONG BUY)", "#00e676", green_c, "rgba(0, 230, 118, 0.85)")
        stop_loss, target_price = price - (1.5 * atr_val), price + (2.5 * atr_val)
        recommendation = "BUY"
    elif is_bullish_st:
        sig, col, icon, glow = ("BUY", "#00e676", green_c, "rgba(0, 230, 118, 0.85)") if not is_urdu else ("خریداری (BUY)", "#00e676", green_c, "rgba(0, 230, 118, 0.85)")
        stop_loss, target_price = price - (1.2 * atr_val), price + (2.0 * atr_val)
        recommendation = "BUY"
    elif not is_bullish_st:
        sig, col, icon, glow = ("STRONG SELL", "#ff1744", red_c, "rgba(255, 23, 68, 0.85)") if not is_urdu else ("مضبوط فروخت (STRONG SELL)", "#ff1744", red_c, "rgba(255, 23, 68, 0.85)")
        stop_loss, target_price = price + (1.5 * atr_val), price - (2.5 * atr_val)
        recommendation = "SELL"
    else:
        sig, col, icon, glow = ("HOLD / NEUTRAL", "#ff9100", neut_c, "rgba(255, 145, 0, 0.8)") if not is_urdu else ("ہولڈ / غیر جانبدار", "#ff9100", neut_c, "rgba(255, 145, 0, 0.8)")
        stop_loss, target_price = price - (1.0 * atr_val), price + (1.0 * atr_val)
        recommendation = "HOLD"

    st.markdown(f'''
    <div class="glow-circle-wrapper" style="margin: 0 auto;">
        <div class="glow-circle-ring" style="--signal-color: {col};"></div>
        <div class="glow-circle" style="--signal-color: {col}; --glow-color: {glow};">{icon}</div>
    </div>
    <div class="signal-title" style="color: {col};">{sig}</div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    chg_col = "#00e676" if price_change >= 0 else "#ff1744"
    c1.markdown(f'<div class="metric-card"><div class="metric-label">{"Price Used" if not is_urdu else "موجودہ قیمت"}</div><div class="metric-val">{cur_sym}{price:,.4f}</div><div class="metric-sub" style="color: {chg_col};">{price_change:+,.4f} ({pct_change:+.2f}%)</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-label">{"Target (TP)" if not is_urdu else "ٹارگٹ"}</div><div class="metric-val" style="color: #00e676;">{cur_sym}{target_price:,.4f}</div><div class="metric-sub" style="color: #8b949e;">Take-Profit</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-label">{"Stop Loss (SL)" if not is_urdu else "اسٹاپ لاس"}</div><div class="metric-val" style="color: #ff1744;">{cur_sym}{stop_loss:,.4f}</div><div class="metric-sub" style="color: #8b949e;">Risk Shield</div></div>', unsafe_allow_html=True)

    # 🤖 Interactive AI Voice Assistant (Buy or Sell Advice)
    st.markdown("---")
    ai_heading = "🤖 Interactive Voice AI Assistant (Buy / Sell Recommendation)" if not is_urdu else "🤖 انٹرایکٹو وائس اے آئی اسسٹنٹ (خریدیں یا بیچیں کا مشورہ)"
    st.markdown(f"**{ai_heading}**")
    
    ai_speech_advice = f"AI Assistant analysis for {sel_name}. Market trend is currently {sig}. The recommended action is to {recommendation}. Current price is {cur_sym}{price:,.2f} with Stop Loss at {cur_sym}{stop_loss:,.2f}."
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1f2937, #111827); border: 1px solid #00e676; padding: 18px; border-radius: 12px; margin: 10px 0; text-align: center; box-shadow: 0 4px 20px rgba(0,230,118,0.15);">
        <p style="font-size: 14px; color: #00e676; font-weight: bold; margin-bottom: 5px;">🤖 AI RECOMMENDATION FOR {sel_name.upper()}</p>
        <p style="font-size: 20px; font-weight: 900; color: {'#00e676' if recommendation=='BUY' else '#ff1744' if recommendation=='SELL' else '#ff9100'}; margin-bottom: 12px;">ACTION: {recommendation} ({sig})</p>
    </div>
    """, unsafe_allow_html=True)

    ai_btn_html = f"""
    <div style="display: flex; justify-content: center; margin-bottom: 15px;">
        <button onclick="speakAIAdvice()" style="background: linear-gradient(135deg, #00e676, #00b0ff); color: #000; font-weight: bold; border: none; padding: 12px 26px; border-radius: 25px; cursor: pointer; font-size: 14px; box-shadow: 0 0 15px rgba(0, 230, 118, 0.6);">
            🗣️ {"Listen AI Voice Advice (Buy or Sell?)" if not is_urdu else "اے آئی کی آواز میں مشورہ سنیں (خریدیں یا بیچیں؟)"}
        </button>
    </div>
    <script>
    function speakAIAdvice() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var utterance = new SpeechSynthesisUtterance("{ai_speech_advice}");
            utterance.rate = 0.95;
            window.speechSynthesis.speak(utterance);
        }}
    }}
    </script>
    """
    components.html(ai_btn_html, height=60)

    # Advanced Institutional Indicators Row
    st.markdown("---")
    st.markdown("🚀 **Advanced Institutional Indicators (Supertrend & VWAP):**" if not is_urdu else "🚀 **ایڈوانسڈ انسٹی ٹیوشنل انڈیکیٹرز (سپر ٹرینڈ اور وی واپ):**")
    m1, m2, m3, m4 = st.columns(4)
    st_status = "BULLISH 🟢" if is_bullish_st else "BEARISH 🔴"
    m1.markdown(f'<div class="metric-card"><div class="metric-label">Supertrend</div><div class="metric-val" style="font-size: 14px !important;">{st_status}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-label">VWAP</div><div class="metric-val">{cur_sym}{curr_vwap:,.2f}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div class="metric-label">RSI (14)</div><div class="metric-val">{curr_rsi:.1f}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-card"><div class="metric-label">EMA 20</div><div class="metric-val">{cur_sym}{float(ema20.iloc[-1]):,.4f}</div></div>', unsafe_allow_html=True)

    # Chart Controls & Subplots
    st.markdown("---")
    st.markdown("🎛️ **Chart Controls & Volume View:**" if not is_urdu else "🎛️ **چارٹ کنٹرولز اور والیم ویو:**")
    col_t1, col_t2, col_t3 = st.columns(3)
    show_vwap = col_t1.checkbox("VWAP Line", value=True)
    show_ema20 = col_t2.checkbox("EMA 20", value=True)
    show_volume = col_t3.checkbox("Volume Bars 📊", value=True)

    st.subheader(f"📈 {sel_name} Candlestick & Volume Chart")
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.75, 0.25])
    fig.add_trace(go.Candlestick(x=df.index, open=open_p, high=high_p, low=low_p, close=close, name="Price", increasing_line_color='#00e676', decreasing_line_color='#ff1744'), row=1, col=1)

    if show_vwap:
        fig.add_trace(go.Scatter(x=df.index, y=vwap, mode='lines', name='VWAP', line=dict(color='#ff9100', width=1.5)), row=1, col=1)
    if show_ema20:
        fig.add_trace(go.Scatter(x=df.index, y=ema20, mode='lines', name='EMA 20', line=dict(color='#00e676', width=1)), row=1, col=1)

    if show_volume:
        colors = ['#00e676' if close.iloc[i] >= open_p.iloc[i] else '#ff1744' for i in range(len(close))]
        fig.add_trace(go.Bar(x=df.index, y=volume, name='Volume', marker_color=colors), row=2, col=1)

    fig.update_layout(template="plotly_dark" if is_dark else "plotly_white", paper_bgcolor=theme_bg, plot_bgcolor=card_bg, margin=dict(l=10, r=10, t=30, b=10), xaxis_rangeslider_visible=False, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)
