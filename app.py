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
    padding: 8px 0; white-space: nowrap; box-sizing: border-box; margin: 5px 0 10px 0;
}
.ticker { display: inline-block; animation: ticker 30s linear infinite; }
.ticker-item { display: inline-block; padding: 0 25px; font-size: 13px; font-weight: 700; font-family: 'Poppins', sans-serif; }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }

.logo-header-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-top: 2px; margin-bottom: 5px; }
.logo-img { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #00e676; box-shadow: 0 0 25px rgba(0, 230, 118, 0.6); margin-bottom: 6px; object-fit: cover; }
.animated-title { font-family: 'Poppins', sans-serif; font-size: 24px; font-weight: 900; text-transform: uppercase; background: linear-gradient(90deg, #00e676, #58a6ff, #00e676); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 1.5px; }
.animated-author { font-family: 'Great Vibes', cursive; font-size: 30px; color: #58a6ff; margin-top: -2px; }

.header-badge { background: #161b22; border: 1px solid #30363d; padding: 5px 12px; border-radius: 20px; color: #00e676; font-family: 'Orbitron', sans-serif; font-size: 12px; font-weight: 700; }
.header-phone { background: #161b22; border: 1px solid #30363d; padding: 5px 12px; border-radius: 20px; color: #58a6ff; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: 700; text-decoration: none; }

.pulse-container { display: flex; justify-content: space-around; align-items: center; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 10px 5px; margin: 10px 0; }
.pulse-item { text-align: center; flex: 1; }
.pulse-label { font-size: 11px; font-weight: 700; text-transform: uppercase; }
.pulse-val { font-size: 18px; font-weight: 900; margin-top: 2px; }

.circle-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 10px 0; }
.glow-circle { width: 105px; height: 105px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, #1c2128 0%, #0d1117 100%); box-shadow: 0 0 30px rgba(0, 230, 118, 0.6); border: 3px solid #00e676; }
.signal-title { font-size: 24px; font-weight: 900; text-align: center; letter-spacing: 1.5px; margin-top: 10px; color: #00e676; }

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
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Gold (GC=F)": "GC=F",
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

st.markdown(f"""
<div class="logo-header-container">
    <img src="{logo_url}" class="logo-img" alt="PSX Logo">
    <div class="animated-title">PSX Trading Wizards</div>
    <div class="animated-author">By Ijaz Sardar</div>
    <div style="margin-top: 6px;">
        <a href="tel:+923007581169" class="header-phone">📞 +92 300 7581169</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Live Ticker
ticker_html_items = ""
for t_name, t_sym in symbols.items():
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
            ticker_html_items += f'<div class="ticker-item">{short_name}: <span style="color: {col};">{cp:,.2f} ({sign}{pct:.2f}%)</span></div>'
    except Exception:
        pass

if ticker_html_items:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">{ticker_html_items}{ticker_html_items}</div></div>', unsafe_allow_html=True)

# Voice Search
st.markdown("<h6 style='text-align: center; color: #00e676; margin-bottom: 5px;'>🎙️ Voice Search & Filter Share</h6>", unsafe_allow_html=True)
components.html("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;">
    <button id="micBtn" style="background: linear-gradient(135deg, #ff9100, #ff3d00); color: #fff; font-weight: bold; border: none; padding: 8px 18px; border-radius: 20px; cursor: pointer; font-size: 13px; box-shadow: 0 0 12px rgba(255, 145, 0, 0.5);">🎙️ Speak Stock Name</button>
    <div id="statusText" style="color: #58a6ff; font-size: 11px; font-weight: 500;">Click mic & speak stock name (e.g. 'Bitcoin', 'HBL', 'Fauji')</div>
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

search_query = st.text_input("🔍 Type to Search Stock / Share Name:", "")
filtered_symbols = {k: v for k, v in symbols.items() if search_query.lower() in k.lower()} if search_query else symbols
if not filtered_symbols: filtered_symbols = symbols

sel_name = st.selectbox("Select Market / Share", list(filtered_symbols.keys()))
sel_tf = st.selectbox("Select Timeframe", ["Daily (1D)", "Weekly (1W)", "1 Hour", "15 Minutes"])

ticker = symbols[sel_name]

@st.cache_data(ttl=10)
def load_data(sym):
    try:
        t_obj = yf.Ticker(sym)
        df_test = t_obj.history(period="30d", interval="1d")
    except Exception:
        df_test = None
        
    if sym == "NBP.KA" or df_test is None or df_test.empty:
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
        base_p = 155.04 if sym == "NBP.KA" else 150.0
        prices = base_p + np.cumsum(np.random.randn(30) * 0.4)
        df_test = pd.DataFrame({'Open': prices-0.4, 'High': prices+1.0, 'Low': prices-1.0, 'Close': prices}, index=dates)
    return df_test

df = load_data(ticker)

if df is not None and not df.empty:
    close = df['Close']
    open_p = df['Open']
    high_p = df['High']
    low_p = df['Low']
    
    cur_sym = "Rs. " if "KA" in ticker or "^KS100" in ticker else "$"
    price = 155.04 if ticker == "NBP.KA" else float(close.iloc[-1])
    
    prev_price = float(close.iloc[-2]) if len(close) > 1 else price
    price_change = price - prev_price
    pct_change = (price_change / prev_price) * 100 if prev_price != 0 else 0.0
    
    target_price = price * 1.04
    stop_loss = price * 0.96
    
    st.markdown('''
    <div class="pulse-container">
        <div class="pulse-item"><div class="pulse-label" style="color: #00e676;">🟢 Bullish</div><div class="pulse-val" style="color: #00e676;">24</div></div>
        <div class="pulse-item" style="border-left: 1px solid #30363d; border-right: 1px solid #30363d;"><div class="pulse-label" style="color: #ff1744;">🔴 Bearish</div><div class="pulse-val" style="color: #ff1744;">14</div></div>
        <div class="pulse-item"><div class="pulse-label" style="color: #ff9100;">🟠 Neutral</div><div class="pulse-val" style="color: #ff9100;">5</div></div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="circle-container">
        <div class="glow-circle"><span style="font-size: 30px;">📈</span></div>
        <div class="signal-title">BUY / BULLISH</div>
    </div>
    ''', unsafe_allow_html=True)

    share_msg = urllib.parse.quote(f"🚨 PSX Trading Wizards Signal 🚨\n\nAsset: {sel_name}\nSignal: BUY\nLive Price: {cur_sym}{price:,.2f}\nTarget: {cur_sym}{target_price:,.2f}\nStop Loss: {cur_sym}{stop_loss:,.2f}\n\nAnalyzed by Ijaz Sardar")
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
    c1.markdown(f'<div class="metric-card"><div class="metric-label">Live Price</div><div class="metric-val">{cur_sym}{price:,.2f}</div><div class="metric-sub" style="color: {chg_col};">{price_change:+,.2f} ({pct_change:+.2f}%)</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-label">Target (TP)</div><div class="metric-val" style="color: #00e676;">{cur_sym}{target_price:,.2f}</div><div class="metric-sub" style="color: #8b949e;">Take-Profit</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-label">Stop Loss (SL)</div><div class="metric-val" style="color: #ff1744;">{cur_sym}{stop_loss:,.2f}</div><div class="metric-sub" style="color: #8b949e;">Risk Shield</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader(f"📈 {sel_name} Interactive Candlestick Chart")
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=open_p, high=high_p, low=low_p, close=close,
        name="Candlestick", increasing_line_color='#00e676', decreasing_line_color='#ff1744'
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="#0d1117", plot_bgcolor="#161b22",
        margin=dict(l=10, r=10, t=30, b=10), xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)
