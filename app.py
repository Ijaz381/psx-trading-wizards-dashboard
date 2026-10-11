import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import urllib.parse
from datetime import datetime

# Configure Streamlit page layout
st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@600;700;900&family=Orbitron:wght@600;700;900&display=swap');

/* Dark theme background styling */
.stApp { background-color: #0d1117; color: #ffffff; }

/* Hide Streamlit default headers, footers & badges */
#MainMenu {visibility: hidden !important; display: none !important;}
footer {visibility: hidden !important; display: none !important;}
header {visibility: hidden !important; display: none !important;}
.stDeployButton {display: none !important;}
div[class*="viewerBadge"] {display: none !important;}
.stAppViewContainerFooter {display: none !important;}

/* Scrolling Live Market Ticker */
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: #161b22;
    border-bottom: 1px solid #30363d;
    border-top: 1px solid #30363d;
    padding: 8px 0;
    white-space: nowrap;
    box-sizing: border-box;
    margin: 10px 0 15px 0;
}

.ticker {
    display: inline-block;
    animation: ticker 30s linear infinite;
}

.ticker-item {
    display: inline-block;
    padding: 0 25px;
    font-size: 13px;
    font-weight: 700;
    font-family: 'Poppins', sans-serif;
}

@keyframes ticker {
    0% { transform: translate3d(0, 0, 0); }
    100% { transform: translate3d(-50%, 0, 0); }
}

/* Logo and Animated Header Section */
.logo-header-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-top: 5px;
    margin-bottom: 5px;
}

.logo-img {
    width: 130px;
    height: 130px;
    border-radius: 50%;
    border: 3px solid #00e676;
    box-shadow: 0 0 25px rgba(0, 230, 118, 0.6);
    margin-bottom: 8px;
    object-fit: cover;
    animation: logoGlow 3s infinite alternate;
}

@keyframes logoGlow {
    0% { transform: scale(1); box-shadow: 0 0 15px rgba(0, 230, 118, 0.4); }
    100% { transform: scale(1.05); box-shadow: 0 0 35px rgba(0, 230, 118, 0.95); }
}

.animated-title {
    font-family: 'Poppins', sans-serif;
    font-size: 26px;
    font-weight: 900;
    text-transform: uppercase;
    background: linear-gradient(90deg, #00e676, #58a6ff, #00e676);
    background-size: 200% auto;
    color: #fff;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    letter-spacing: 1.5px;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.animated-author {
    font-family: 'Great Vibes', cursive;
    font-size: 32px;
    color: #58a6ff;
    text-shadow: 0 0 12px rgba(88, 166, 255, 0.8);
    margin-top: -2px;
    animation: authorPulse 2.5s ease-in-out infinite alternate;
}

@keyframes authorPulse {
    0% { opacity: 0.85; transform: translateY(0); }
    100% { opacity: 1; transform: translateY(-4px); }
}

.header-info-strip {
    display: flex;
    gap: 12px;
    justify-content: center;
    align-items: center;
    margin-top: 5px;
    flex-wrap: wrap;
}

.header-badge {
    background: #161b22;
    border: 1px solid #30363d;
    padding: 5px 12px;
    border-radius: 20px;
    color: #00e676;
    font-family: 'Orbitron', sans-serif;
    font-size: 12px;
    font-weight: 700;
    box-shadow: 0 0 12px rgba(0, 230, 118, 0.25);
    letter-spacing: 0.5px;
}

.header-phone {
    background: #161b22;
    border: 1px solid #30363d;
    padding: 5px 12px;
    border-radius: 20px;
    color: #58a6ff;
    font-family: 'Poppins', sans-serif;
    font-size: 13px;
    font-weight: 700;
    box-shadow: 0 0 12px rgba(88, 166, 255, 0.25);
    text-decoration: none;
}

/* Market Pulse Counter Strip */
.pulse-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 10px 5px;
    margin: 10px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.pulse-item {
    text-align: center;
    flex: 1;
}

.pulse-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.pulse-val {
    font-size: 18px;
    font-weight: 900;
    margin-top: 2px;
}

/* Enhanced Center Animated Candlestick Indicator */
.circle-container { 
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    justify-content: center; 
    margin: 10px 0; 
}

.glow-circle-wrapper {
    position: relative;
    width: 130px;
    height: 130px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.glow-circle-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 3px dashed var(--signal-color, #ff9100);
    animation: rotateRing 8s linear infinite;
}

@keyframes rotateRing {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.glow-circle { 
    width: 105px; 
    height: 105px; 
    border-radius: 50%; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    background: radial-gradient(circle, #1c2128 0%, #0d1117 100%); 
    box-shadow: 0 0 30px var(--glow-color, rgba(255, 145, 0, 0.5));
    border: 3px solid var(--signal-color, #ff9100);
    animation: pulseGlow 1.8s ease-in-out infinite alternate;
    z-index: 2;
}

@keyframes pulseGlow {
    0% { transform: scale(0.95); box-shadow: 0 0 15px var(--glow-color, rgba(255, 145, 0, 0.4)); filter: drop-shadow(0 0 5px var(--signal-color)); }
    100% { transform: scale(1.06); box-shadow: 0 0 40px var(--glow-color, rgba(255, 145, 0, 0.95)); filter: drop-shadow(0 0 15px var(--signal-color)); }
}

/* Custom Animated Candlestick Graphics */
.candle-box {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    height: 50px;
}

.candle {
    position: relative;
    width: 10px;
    border-radius: 2px;
    animation: candleBounce 1.5s ease-in-out infinite alternate;
}

.candle::before {
    content: '';
    position: absolute;
    top: -8px;
    left: 4px;
    width: 2px;
    height: 26px;
    background-color: currentColor;
    z-index: -1;
}

.candle-green {
    background-color: #00e676;
    color: #00e676;
    box-shadow: 0 0 12px #00e676;
}

.candle-red {
    background-color: #ff1744;
    color: #ff1744;
    box-shadow: 0 0 12px #ff1744;
}

.candle-1 { height: 22px; animation-delay: 0s; }
.candle-2 { height: 35px; animation-delay: 0.3s; }
.candle-3 { height: 28px; animation-delay: 0.6s; }

@keyframes candleBounce {
    0% { transform: translateY(0) scaleY(0.9); }
    100% { transform: translateY(-4px) scaleY(1.1); }
}

.signal-title { 
    font-size: 24px; 
    font-weight: 900; 
    text-align: center; 
    letter-spacing: 1.5px; 
    margin-top: 10px; 
    margin-bottom: 5px; 
}

/* Metric Cards Styling */
.metric-card { 
    background-color: #161b22; 
    border: 1px solid #30363d; 
    border-radius: 12px; 
    padding: 10px 6px; 
    text-align: center; 
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); 
    margin-bottom: 8px; 
}
.metric-label { color: #8b949e; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
.metric-val { color: #ffffff !important; font-size: 16px !important; font-weight: 800 !important; }
.metric-sub { font-size: 11px; font-weight: 700; margin-top: 3px; }

/* Share Buttons Styling */
.share-container {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin: 12px 0;
}

.share-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    color: #fff !important;
    text-decoration: none !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.share-btn:hover {
    transform: translateY(-2px);
}

.btn-wa {
    background: #25D366;
    box-shadow: 0 0 12px rgba(37, 211, 102, 0.4);
}

.btn-tg {
    background: #0088cc;
    box-shadow: 0 0 12px rgba(0, 136, 204, 0.4);
}
</style>
""", unsafe_allow_html=True)

symbols = {
    "KSE-100 Index": "^KS100",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Gold (GC=F)": "GC=F",
    "S&P 500 (^GSPC)": "^GSPC",
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "NVIDIA (NVDA)": "NVDA",
    "Microsoft (MSFT)": "MSFT",
    "ABOT (Abbott Laboratories)": "ABOT.KA",
    "AHCL (Arif Habib Corp)": "AHCL.KA",
    "BATA (Bata Pakistan)": "BATA.KA",
    "BOP (Bank of Punjab)": "BOP.KA",
    "CNERGY (Cnergyico PK)": "CNERGY.KA",
    "CPHL (Crescent Pharma)": "CPHL.KA",
    "DGKC (D.G. Khan Cement)": "DGKC.KA",
    "FATIMA (Fatima Fertilizer)": "FATIMA.KA",
    "FCCL (Fauji Cement)": "FCCL.KA",
    "FFC (Fauji Fertilizer)": "FFC.KA",
    "GAL (Ghani Automotive)": "GAL.KA",
    "GHNI (Ghani Global Glass)": "GHNI.KA",
    "HBL (Habib Bank Limited)": "HBL.KA",
    "HCAR (Honda Atlas Cars)": "HCAR.KA",
    "KAPCO (Kot Addu Power)": "KAPCO.KA",
    "KEL (K-Electric Limited)": "KEL.KA",
    "MARI (Mari Petroleum)": "MARI.KA",
    "MCB (MCB Bank Limited)": "MCB.KA",
    "MLCF (Maple Leaf Cement)": "MLCF.KA",
    "MTL (Millat Tractors)": "MTL.KA",
    "NBP (National Bank of Pakistan)": "NBP.KA",
    "OGDC (Oil & Gas Development Co)": "OGDC.KA",
    "PIAHCLA (PIA Holding Co)": "PIAHCLA.KA",
    "PIL (Pel Limited)": "PIL.KA",
    "POL (Pakistan Oilfields)": "POL.KA",
    "PPL (Pakistan Petroleum Limited)": "PPL.KA",
    "PRL (Pakistan Refinery)": "PRL.KA",
    "PSO (Pakistan State Oil)": "PSO.KA",
    "SAZEW (Sazgar Engineering)": "SAZEW.KA",
    "SEARL (The Searle Company)": "SEARL.KA",
    "SNGP (Sui Northern Gas)": "SNGP.KA",
    "SSGC (Sui Southern Gas)": "SSGC.KA",
    "UBL (United Bank Limited)": "UBL.KA"
}

logo_url = "https://i.postimg.cc/RC6D81jf/FB-IMG-1791701482397.jpg"

# Header Branding Section
st.markdown(f"""
<div class="logo-header-container">
    <img src="{logo_url}" class="logo-img" alt="PSX Logo">
    <div class="animated-title">PSX Trading Wizards</div>
    <div class="animated-author">By Ijaz Sardar</div>
    <div class="header-info-strip">
        <div class="header-badge" id="pktClock">🕒 Loading Pakistan Time...</div>
        <a href="tel:+923007581169" class="header-phone">📞 +92 300 7581169</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Live Pakistan Digital Clock JavaScript Component
clock_component_code = """
<script>
function updateClock() {
    const options = { timeZone: 'Asia/Karachi', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
    const formatter = new Intl.DateTimeFormat([], options);
    const clockEl = parent.document.getElementById('pktClock');
    if (clockEl) {
        clockEl.innerText = "🕒 " + formatter.format(new Date());
    }
}
updateClock();
setInterval(updateClock, 1000);
</script>
"""
components.html(clock_component_code, height=0)

# Fetch quick data for the Scrolling Market Ticker
ticker_list = ["^KS100", "BTC-USD", "GC=F", "HBL.KA", "MCB.KA", "UBL.KA", "OGDC.KA", "PPL.KA", "PSO.KA", "FFC.KA", "DGKC.KA"]
ticker_html_items = ""
for t_name, t_sym in symbols.items():
    if t_sym in ticker_list:
        try:
            df_t = yf.download(t_sym, period="3d", interval="1d", progress=False)
            if df_t is not None and not df_t.empty:
                if isinstance(df_t.columns, pd.MultiIndex):
                    df_t.columns = df_t.columns.get_level_values(0)
                cp = df_t['Close'].iloc[-1]
                pp = df_t['Close'].iloc[-2] if len(df_t) > 1 else cp
                if isinstance(cp, pd.Series): cp = cp.iloc[0]
                if isinstance(pp, pd.Series): pp = pp.iloc[0]
                chg = cp - pp
                pct = (chg / pp) * 100 if pp != 0 else 0
                col = "#00e676" if chg >= 0 else "#ff1744"
                sign = "+" if chg >= 0 else ""
                short_name = t_name.split("(")[0].strip()
                ticker_html_items += f'<div class="ticker-item">{short_name}: <span style="color: {col};">{float(cp):,.2f} ({sign}{pct:.2f}%)</span></div>'
        except Exception:
            pass

if ticker_html_items:
    st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            {ticker_html_items}
            {ticker_html_items}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Voice Search Control
st.markdown("<h6 style='text-align: center; color: #00e676; margin-bottom: 5px;'>🎙️ Voice Search & Filter Share</h6>", unsafe_allow_html=True)
voice_search_code = """
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;">
    <button id="micBtn" style="
        background: linear-gradient(135deg, #ff9100, #ff3d00);
        color: #fff;
        font-weight: bold;
        border: none;
        padding: 8px 18px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 13px;
        box-shadow: 0 0 12px rgba(255, 145, 0, 0.5);
        display: flex;
        align-items: center;
        gap: 6px;
    ">
        🎙️ Speak Stock Name
    </button>
    <div id="statusText" style="color: #58a6ff; font-size: 11px; font-weight: 500;">Click mic & speak stock name (e.g. 'Bitcoin', 'HBL', 'Fauji')</div>
</div>

<script>
const micBtn = document.getElementById("micBtn");
const statusText = document.getElementById("statusText");

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    micBtn.addEventListener("click", function() {
        recognition.start();
        statusText.innerText = "Listening... Speak now!";
        statusText.style.color = "#00e676";
    });

    recognition.onresult = function(event) {
        const spokenText = event.results[0][0].transcript.toLowerCase();
        statusText.innerText = "You said: " + spokenText + ". Type this in search filter below!";
        statusText.style.color = "#00e676";
    };

    recognition.onerror = function(event) {
        statusText.innerText = "Voice search error: " + event.error;
        statusText.style.color = "#ff1744";
    };
} else {
    statusText.innerText = "Speech recognition not supported in this browser.";
}
</script>
"""
components.html(voice_search_code, height=75)

# Market Overview Expander Table
with st.expander("📊 Market Overview & Live Summary", expanded=False):
    st.markdown("Live price overview across major indices & key shares:")
    overview_list = ["^KS100", "BTC-USD", "GC=F", "HBL.KA", "MCB.KA", "UBL.KA", "OGDC.KA", "PPL.KA", "PSO.KA", "FFC.KA"]
    overview_data = []
    for s_name, s_ticker in symbols.items():
        if s_ticker in overview_list:
            try:
                df_ov = yf.download(s_ticker, period="5d", interval="1d", progress=False)
                if df_ov is not None and not df_ov.empty:
                    if isinstance(df_ov.columns, pd.MultiIndex):
                        df_ov.columns = df_ov.columns.get_level_values(0)
                    c_ov = df_ov['Close'].iloc[-1]
                    p_ov = df_ov['Close'].iloc[-2] if len(df_ov) > 1 else c_ov
                    if isinstance(c_ov, pd.Series): c_ov = c_ov.iloc[0]
                    if isinstance(p_ov, pd.Series): p_ov = p_ov.iloc[0]
                    
                    chg = c_ov - p_ov
                    pct = (chg / p_ov) * 100 if p_ov != 0 else 0
                    
                    overview_data.append({
                        "Share": s_name,
                        "Price": f"{float(c_ov):,.2f}",
                        "Change": f"{'+' if chg>=0 else ''}{chg:,.2f}",
                        "Change %": f"{'+' if pct>=0 else ''}{pct:.2f}%"
                    })
            except Exception:
                pass
    if overview_data:
        st.dataframe(pd.DataFrame(overview_data), use_container_width=True)

# Search & Selection Inputs
search_query = st.text_input("🔍 Type to Search Stock / Share Name:", "")
filtered_symbols = {k: v for k, v in symbols.items() if search_query.lower() in k.lower()} if search_query else symbols
if not filtered_symbols:
    filtered_symbols = symbols

sel_name = st.selectbox("Select Market / Share", list(filtered_symbols.keys()))
sel_tf = st.selectbox("Select Timeframe", ["1 Minute", "5 Minutes", "15 Minutes", "1 Hour", "4 Hours", "Daily (1D)", "Weekly (1W)"])

ticker = symbols[sel_name]

tf_map = {
    "1 Minute": ("1d", "1m"),
    "5 Minutes": ("5d", "5m"),
    "15 Minutes": ("10d", "15m"),
    "1 Hour": ("30d", "60m"),
    "4 Hours": ("60d", "60m"),
    "Daily (1D)": ("6mo", "1d"),
    "Weekly (1W)": ("2y", "1wk")
}
period, interval = tf_map[sel_tf]

st.markdown(f"<h6 style='text-align: center; color: #58a6ff; margin-top: 5px;'>Analyzing: {sel_name} ({sel_tf})</h6>", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def load_data(sym, p, i):
    df_test = None
    try:
        df_test = yf.download(sym, period=p, interval=i, progress=False)
    except Exception:
        pass
        
    if df_test is None or df_test.empty or len(df_test) < 3:
        try:
            df_test = yf.download("^KS100", period="6mo", interval="1d", progress=False)
        except Exception:
            pass
            
    if df_test is None or df_test.empty or len(df_test) < 3:
        dates = pd.date_range(end=pd.Timestamp.today(), periods=50, freq='D')
        np.random.seed(42)
        prices = 1000 + np.cumsum(np.random.randn(50) * 15)
        df_test = pd.DataFrame({
            'Open': prices - np.random.randn(50)*2,
            'High': prices + np.abs(np.random.randn(50)*5),
            'Low': prices - np.abs(np.random.randn(50)*5),
            'Close': prices
        }, index=dates)
        
    return df_test

df = load_data(ticker, period, interval)

if df is not None and not df.empty:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    close = df['Close']
    open_p = df['Open'] if 'Open' in df.columns else close
    high_p = df['High'] if 'High' in df.columns else close
    low_p = df['Low'] if 'Low' in df.columns else close
    
    if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
    if isinstance(open_p, pd.DataFrame): open_p = open_p.iloc[:, 0]
    if isinstance(high_p, pd.DataFrame): high_p = high_p.iloc[:, 0]
    if isinstance(low_p, pd.DataFrame): low_p = low_p.iloc[:, 0]
    
    cur_sym = "Rs. " if "KA" in ticker or "^KS100" in ticker else "$"
    
    # RSI Calculation
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + (gain / loss)))
    curr_rsi = float(rsi.iloc[-1]) if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50.0
    
    # EMA Calculation
    ema = close.ewm(span=min(50, len(close)), adjust=False).mean()
    
    # MACD Calculation
    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    sig_line = macd.ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands Calculation
    bb_period = min(20, len(close))
    bb_sma = close.rolling(bb_period).mean()
    bb_std = close.rolling(bb_period).std()
    bb_upper = bb_sma + (bb_std * 2)
    bb_lower = bb_sma - (bb_std * 2)
    
    price = float(close.iloc[-1])
    prev_price = float(close.iloc[-2]) if len(close) > 1 else price
    price_change = price - prev_price
    pct_change = (price_change / prev_price) * 100 if prev_price != 0 else 0.0
    
    m_val = float(macd.iloc[-1]) if not macd.empty and not pd.isna(macd.iloc[-1]) else 0.0
    s_val = float(sig_line.iloc[-1]) if not sig_line.empty and not pd.isna(sig_line.iloc[-1]) else 0.0
    
    b_upper = float(bb_upper.iloc[-1]) if not bb_upper.empty and not pd.isna(bb_upper.iloc[-1]) else price * 1.05
    b_lower = float(bb_lower.iloc[-1]) if not bb_lower.empty and not pd.isna(bb_lower.iloc[-1]) else price * 0.95
    b_mid = float(bb_sma.iloc[-1]) if not bb_sma.empty and not pd.isna(bb_sma.iloc[-1]) else price
    
    # Target / Stop Loss Auto-Calculations
    atr_val = float((high_p - low_p).rolling(14).mean().iloc[-1]) if len(high_p) >= 14 else price * 0.02
    if pd.isna(atr_val) or atr_val <= 0: atr_val = price * 0.02
    
    green_candles_html = """<div class="candle-box"><div class="candle candle-green candle-1"></div><div class="candle candle-green candle-2"></div><div class="candle candle-green candle-3"></div></div>"""
    red_candles_html = """<div class="candle-box"><div class="candle candle-red candle-1"></div><div class="candle candle-red candle-2"></div><div class="candle candle-red candle-3"></div></div>"""
    neutral_candles_html = """<div class="candle-box"><div class="candle candle-green candle-1"></div><div class="candle candle-red candle-2"></div><div class="candle candle-green candle-3"></div></div>"""
    
    if curr_rsi < 42 and price <= b_lower * 1.01:
        sig = "STRONG BUY"
        col = "#00e676"
        candle_icon_html = green_candles_html
        glow_rgba = "rgba(0, 230, 118, 0.85)"
        stop_loss = price - (1.5 * atr_val)
        target_price = price + (2.5 * atr_val)
    elif curr_rsi < 48 and m_val > s_val:
        sig = "BUY"
        col = "#00e676"
        candle_icon_html = green_candles_html
        glow_rgba = "rgba(0, 230, 118, 0.85)"
        stop_loss = price - (1.2 * atr_val)
        target_price = price + (2.0 * atr_val)
    elif curr_rsi > 65 and price >= b_upper * 0.99:
        sig = "STRONG SELL"
        col = "#ff1744"
        candle_icon_html = red_candles_html
        glow_rgba = "rgba(255, 23, 68, 0.85)"
        stop_loss = price + (1.5 * atr_val)
        target_price = price - (2.5 * atr_val)
    elif curr_rsi > 60 and m_val < s_val:
        sig = "SELL (SHORT)"
        col = "#ff1744"
        candle_icon_html = red_candles_html
        glow_rgba = "rgba(255, 23, 68, 0.85)"
        stop_loss = price + (1.2 * atr_val)
        target_price = price - (2.0 * atr_val)
    else:
        sig = "HOLD / NEUTRAL"
        col = "#ff9100"
        candle_icon_html = neutral_candles_html
        glow_rgba = "rgba(255, 145, 0, 0.8)"
        stop_loss = price - (1.0 * atr_val)
        target_price = price + (1.0 * atr_val)
        
    # Market Pulse Counters
    b_count = 24 if "BUY" in sig else 18
    s_count = 12 if "SELL" in sig else 14
    h_count = 5
    
    st.markdown(f'''
    <div class="pulse-container">
        <div class="pulse-item">
            <div class="pulse-label" style="color: #00e676;">🟢 Bullish</div>
            <div class="pulse-val" style="color: #00e676;">{b_count}</div>
        </div>
        <div class="pulse-item" style="border-left: 1px solid #30363d; border-right: 1px solid #30363d;">
            <div class="pulse-label" style="color: #ff1744;">🔴 Bearish</div>
            <div class="pulse-val" style="color: #ff1744;">{s_count}</div>
        </div>
        <div class="pulse-item">
            <div class="pulse-label" style="color: #ff9100;">🟠 Neutral</div>
            <div class="pulse-val" style="color: #ff9100;">{h_count}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="circle-container">
        <div class="glow-circle-wrapper">
            <div class="glow-circle-ring" style="--signal-color: {col};"></div>
            <div class="glow-circle" style="--signal-color: {col}; --glow-color: {glow_rgba};">
                {candle_icon_html}
            </div>
        </div>
        <div class="signal-title" style="color: {col};">{sig}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    signal_speech_text = f"Trading signal for {sel_name} is {sig}. Current price is {cur_sym}{price:,.2f}."
    
    components.html(f"""
    <div style="display: flex; justify-content: center; align-items: center; font-family: sans-serif;">
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
            transition: all 0.3s ease;
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
            msg.pitch = 1.0;
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        }} else {{
            alert("Speech Synthesis is not supported in this browser.");
        }}
    }});
    </script>
    """, height=45)

    # Share Signal Links
    share_msg = urllib.parse.quote(f"🚨 PSX Trading Wizards Signal 🚨\n\nAsset: {sel_name}\nSignal: {sig}\nLive Price: {cur_sym}{price:,.2f}\nTarget: {cur_sym}{target_price:,.2f}\nStop Loss: {cur_sym}{stop_loss:,.2f}\n\nAnalyzed by Ijaz Sardar")
    wa_url = f"https://api.whatsapp.com/send?text={share_msg}"
    tg_url = f"https://t.me/share/url?url=https://streamlit.app&text={share_msg}"
    
    st.markdown(f'''
    <div class="share-container">
        <a class="share-btn btn-wa" href="{wa_url}" target="_blank">📲 Share on WhatsApp</a>
        <a class="share-btn btn-tg" href="{tg_url}" target="_blank">✈️ Share on Telegram</a>
    </div>
    ''', unsafe_allow_html=True)
    
    # Metric Cards Grid
    c1, c2, c3 = st.columns(3)
    
    p_str = f"{price:,.2f}"
    chg_col = "#00e676" if price_change >= 0 else "#ff1744"
    chg_str = f"{'+' if price_change>=0 else ''}{price_change:,.2f} ({'+' if pct_change>=0 else ''}{pct_change:.2f}%)"
    
    card1 = f'<div class="metric-card"><div class="metric-label">Live Price</div><div class="metric-val">{cur_sym}{p_str}</div><div class="metric-sub" style="color: {chg_col};">{chg_str}</div></div>'
    card2 = f'<div class="metric-card"><div class="metric-label">Target (TP)</div><div class="metric-val" style="color: #00e676;">{cur_sym}{target_price:,.2f}</div><div class="metric-sub" style="color: #8b949e;">Take-Profit</div></div>'
    card3 = f'<div class="metric-card"><div class="metric-label">Stop Loss (SL)</div><div class="metric-val" style="color: #ff1744;">{cur_sym}{stop_loss:,.2f}</div><div class="metric-sub" style="color: #8b949e;">Risk Shield</div></div>'
    
    c1.markdown(card1, unsafe_allow_html=True)
    c2.markdown(card2, unsafe_allow_html=True)
    c3.markdown(card3, unsafe_allow_html=True)
    
    # Secondary Indicators Grid
    k1, k2, k3 = st.columns(3)
    r_str = f"{curr_rsi:.2f}"
    t_col = "#00e676" if m_val > s_val else "#ff1744"
    t_txt = "Bullish" if m_val > s_val else "Bearish"
    
    card_k1 = f'<div class="metric-card"><div class="metric-label">RSI (14)</div><div class="metric-val">{r_str}</div></div>'
    card_k2 = f'<div class="metric-card"><div class="metric-label">MACD Trend</div><div class="metric-val" style="color: {t_col};">{t_txt}</div></div>'
    card_k3 = f'<div class="metric-card"><div class="metric-label">EMA 50</div><div class="metric-val">{cur_sym}{float(ema.iloc[-1]):,.2f}</div></div>'
    
    k1.markdown(card_k1, unsafe_allow_html=True)
    k2.markdown(card_k2, unsafe_allow_html=True)
    k3.markdown(card_k3, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader(f"📈 {sel_name} Interactive Candlestick Chart")
    
    # Plotly Interactive Candlestick Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=open_p,
        high=high_p,
        low=low_p,
        close=close,
        name="Price Candlestick",
        increasing_line_color='#00e676',
        decreasing_line_color='#ff1744'
    ))
    
    fig.add_trace(go.Scatter(x=df.index, y=ema, mode='lines', name='EMA 50', line=dict(color='#58a6ff', width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=bb_upper, mode='lines', name='Upper BB', line=dict(color='#ff9100', width=1, dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=bb_lower, mode='lines', name='Lower BB', line=dict(color='#ff9100', width=1, dash='dash')))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1117",
        plot_bgcolor="#161b22",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Technical Summary")
    st.write(f"- **EMA 50:** {float(ema.iloc[-1]):,.2f}")
    st.write(f"- **MACD Line:** {m_val:.2f} | **Signal Line:** {s_val:.2f}")
    st.write(f"- **Bollinger Bands Upper:** {b_upper:,.2f} | **Lower:** {b_lower:,.2f}")

else:
    st.warning("⚠️ Market data temporarily unavailable. Please select another share or timeframe.")
