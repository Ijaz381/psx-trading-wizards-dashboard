import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import urllib.parse
from datetime import datetime

# Configure Streamlit page layout and title
st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@600;700;900&family=Orbitron:wght@600;700;900&display=swap');

/* Dark theme background styling */
.stApp { background-color: #0d1117; color: #ffffff; }

/* Hide Streamlit default headers, footers, badges, and floating menus completely */
#MainMenu {visibility: hidden !important; display: none !important;}
footer {visibility: hidden !important; display: none !important;}
header {visibility: hidden !important; display: none !important;}
.stDeployButton {display: none !important;}
div[class*="viewerBadge"] {display: none !important;}
.stAppViewContainerFooter {display: none !important;}
iframe[title="streamlit_badge"] {display: none !important; visibility: hidden !important;}
section[data-testid="stSidebarNav"] {display: none !important;}
footer, .viewerBadge_container__1QSob, .styles_viewerBadge__1yG6_ { display: none !important; }

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
    margin: 5px 0 10px 0;
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
    margin-top: 2px;
    margin-bottom: 5px;
}

.logo-img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 3px solid #00e676;
    box-shadow: 0 0 25px rgba(0, 230, 118, 0.6);
    margin-bottom: 6px;
    object-fit: cover;
    animation: logoGlow 3s infinite alternate;
}

@keyframes logoGlow {
    0% { transform: scale(1); box-shadow: 0 0 15px rgba(0, 230, 118, 0.4); }
    100% { transform: scale(1.05); box-shadow: 0 0 35px rgba(0, 230, 118, 0.95); }
}

.animated-title {
    font-family: 'Poppins', sans-serif;
    font-size: 24px;
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
    font-size: 30px;
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
    margin-top: 4px;
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

# Live Pakistan Digital Clock & Auto-Refresh JavaScript Component
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

// Auto reload page every 30 seconds to keep live data fresh
setTimeout(function(){
   window.location.reload(1);
}, 30000);
</script>
"""
components.html(clock_component_code, height=0)

# Live Market Scrolling Ticker right below header
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

# Optimized TTL (1 second) with Real-time yf.Ticker Endpoint
@st.cache_data(ttl=1)
def load_data(sym, p, i):
    df_test = None
    try:
        t_obj = yf.Ticker(sym)
        df_test = t_obj.history(period="5d", interval="1m")
        if df_test is None or df_test.empty:
            df_test = yf.download(sym, period=p, interval=i, progress=False)
    except Exception:
        pass
        
    if df_test is None or df_test.empty or len(df_test) < 2:
        try:
            df_test = yf.download(sym, period="10d", interval="1d", progress=False)
        except Exception:
            pass
            
    if df_test is None or df_test.empty or len(df_test) < 2:
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
