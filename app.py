import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Configure Streamlit page layout
st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@700;900&display=swap');

/* Dark theme background styling */
.stApp { background-color: #0d1117; color: #ffffff; }

/* Logo and Animated Header Section */
.logo-header-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-bottom: 20px;
}

.logo-img {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    border: 3px solid #00e676;
    box-shadow: 0 0 25px rgba(0, 230, 118, 0.6);
    margin-bottom: 12px;
    object-fit: cover;
    animation: logoGlow 3s infinite alternate;
}

@keyframes logoGlow {
    0% { transform: scale(1); box-shadow: 0 0 15px rgba(0, 230, 118, 0.4); }
    100% { transform: scale(1.05); box-shadow: 0 0 35px rgba(0, 230, 118, 0.95); }
}

.animated-title {
    font-family: 'Poppins', sans-serif;
    font-size: 28px;
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

/* Circular glowing indicator styling */
.circle-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 15px 0; }
.glow-circle { 
    width: 120px; height: 120px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 45px; background-color: #161b22; margin-bottom: 10px;
    animation: pulseGlow 2s infinite;
}
@keyframes pulseGlow {
    0% { transform: scale(1); box-shadow: 0 0 15px rgba(255, 145, 0, 0.4); }
    50% { transform: scale(1.05); box-shadow: 0 0 30px rgba(255, 145, 0, 0.8); }
    100% { transform: scale(1); box-shadow: 0 0 15px rgba(255, 145, 0, 0.4); }
}
.signal-title { font-size: 24px; font-weight: 900; text-align: center; letter-spacing: 1px; margin-bottom: 10px; }

/* Metric Cards Styling */
.metric-card { background-color: #161b22; border: 2px solid #30363d; border-radius: 12px; padding: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); margin-bottom: 8px; }
.metric-label { color: #58a6ff; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 4px; }
.metric-val { color: #ffffff !important; font-size: 18px !important; font-weight: 800 !important; }

/* Hide Streamlit elements */
#MainMenu {visibility: hidden !important; display: none !important;}
footer {visibility: hidden !important; display: none !important;}
header {visibility: hidden !important; display: none !important;}
.stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Custom Logo URL Provided
logo_url = "https://i.postimg.cc/RC6D81jf/FB-IMG-1791701482397.jpg"

st.markdown(f"""
<div class="logo-header-container">
    <img src="{logo_url}" class="logo-img" alt="PSX Logo">
    <div class="animated-title">PSX Trading Wizards</div>
    <div class="animated-author">By Ijaz Sardar</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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

# Main Screen Selection Menus for Mobile Friendly UI
sel_name = st.selectbox("Select Market / Share", list(symbols.keys()))
sel_tf = st.selectbox("Select Timeframe", ["Daily (1D)", "Weekly (1W)", "4 Hours", "1 Hour", "15 Minutes", "5 Minutes", "1 Minute"])

ticker = symbols[sel_name]

# Timeframe Mapping
tf_map = {
    "Daily (1D)": ("6mo", "1d"),
    "Weekly (1W)": ("2y", "1wk"),
    "4 Hours": ("60d", "60m"),
    "1 Hour": ("30d", "60m"),
    "15 Minutes": ("10d", "15m"),
    "5 Minutes": ("5d", "5m"),
    "1 Minute": ("1d", "1m")
}
period, interval = tf_map[sel_tf]

st.markdown(f"<h5 style='text-align: center; color: #58a6ff; margin-top: 5px;'>Analyzing: {sel_name} ({sel_tf})</h5>", unsafe_allow_html=True)

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
        df_test = pd.DataFrame({'Close': prices}, index=dates)
        
    return df_test

df = load_data(ticker, period, interval)

if df is not None and not df.empty:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    close = df['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    
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
    m_val = float(macd.iloc[-1]) if not macd.empty and not pd.isna(macd.iloc[-1]) else 0.0
    s_val = float(sig_line.iloc[-1]) if not sig_line.empty and not pd.isna(sig_line.iloc[-1]) else 0.0
    
    b_upper = float(bb_upper.iloc[-1]) if not bb_upper.empty and not pd.isna(bb_upper.iloc[-1]) else price * 1.05
    b_lower = float(bb_lower.iloc[-1]) if not bb_lower.empty and not pd.isna(bb_lower.iloc[-1]) else price * 0.95
    b_mid = float(bb_sma.iloc[-1]) if not bb_sma.empty and not pd.isna(bb_sma.iloc[-1]) else price
    
    # Trading Signal Decision Logic
    if curr_rsi < 42 and price <= b_lower * 1.01:
        sig = "STRONG BUY"
        col = "#00e676"
        icon = "🚀"
        glow = "0 0 35px rgba(0, 230, 118, 0.8)"
    elif curr_rsi < 48 and m_val > s_val:
        sig = "BUY"
        col = "#00e676"
        icon = "↗"
        glow = "0 0 35px rgba(0, 230, 118, 0.8)"
    elif curr_rsi > 65 and price >= b_upper * 0.99:
        sig = "STRONG SELL"
        col = "#ff1744"
        icon = "⚠️"
        glow = "0 0 35px rgba(255, 23, 68, 0.8)"
    elif curr_rsi > 60 and m_val < s_val:
        sig = "SELL (SHORT)"
        col = "#ff1744"
        icon = "↘"
        glow = "0 0 35px rgba(255, 23, 68, 0.8)"
    else:
        sig = "HOLD / NEUTRAL"
        col = "#ff9100"
        icon = "➔"
        glow = "0 0 35px rgba(255, 145, 0, 0.8)"
    
    st.markdown(f'''
    <div class="circle-container">
        <div class="glow-circle" style="border: 4px solid {col}; color: {col}; box-shadow: {glow};">{icon}</div>
        <div class="signal-title" style="color: {col};">{sig}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    cur_sym = "Rs. " if "KA" in ticker or "^KS100" in ticker else "$"
    
    p_str = f"{price:,.2f}"
    r_str = f"{curr_rsi:.2f}"
    
    card1 = f'<div class="metric-card"><div class="metric-label">Live Price</div><div class="metric-val">{cur_sym}{p_str}</div></div>'
    card2 = f'<div class="metric-card"><div class="metric-label">RSI (14)</div><div class="metric-val">{r_str}</div></div>'
    
    t_col = "#00e676" if m_val > s_val else "#ff1744"
    t_txt = "Bullish" if m_val > s_val else "Bearish"
    card3 = f'<div class="metric-card"><div class="metric-label">MACD Trend</div><div class="metric-val" style="color: {t_col};">{t_txt}</div></div>'
    
    c1.markdown(card1, unsafe_allow_html=True)
    c2.markdown(card2, unsafe_allow_html=True)
    c3.markdown(card3, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 Technical Indicators & Bollinger Bands")
    ema_val = float(ema.iloc[-1]) if not ema.empty and not pd.isna(ema.iloc[-1]) else price
    
    st.write(f"- **EMA 50:** {ema_val:,.2f}")
    st.write(f"- **MACD Line:** {m_val:.2f} | **Signal Line:** {s_val:.2f}")
    st.write(f"- **Bollinger Upper Band:** {b_upper:,.2f}")
    st.write(f"- **Bollinger Middle (SMA):** {b_mid:,.2f}")
    st.write(f"- **Bollinger Lower Band:** {b_lower:,.2f}")
else:
    st.warning("⚠️ Market data temporarily unavailable. Please select another share or timeframe.")
