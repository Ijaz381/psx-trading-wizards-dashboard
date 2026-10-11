
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0d1117; color: #ffffff; }
.circle-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 25px 0; }
.glow-circle { width: 180px; height: 180px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 65px; background-color: #161b22; margin-bottom: 15px; }
.signal-title { font-size: 38px; font-weight: 900; text-align: center; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📈 PSX Trading Wizards")
st.sidebar.markdown("By Ijaz Sardar")

symbols = {
    "KSE-100 Index": "^KS100",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Gold (GC=F)": "GC=F",
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

sel_name = st.sidebar.selectbox("Select Market / Share", list(symbols.keys()))
ticker = symbols[sel_name]

tf_map = {
    "1 Minute": ("1d", "1m"),
    "5 Minutes": ("1d", "5m"),
    "15 Minutes": ("5d", "15m"),
    "1 Hour": ("5d", "60m"),
    "4 Hours": ("1mo", "60m"),
    "Daily (1D)": ("6mo", "1d"),
    "Weekly (1W)": ("2y", "1wk")
}

sel_tf = st.sidebar.selectbox("Select Timeframe", list(tf_map.keys()))
period, interval = tf_map[sel_tf]

st.markdown("### Analyzing Market: " + sel_name + " (" + sel_tf + ")")

@st.cache_data(ttl=60)
def load_data(sym, p, i):
    try:
        return yf.download(sym, period=p, interval=i, progress=False)
    except:
        return None

df = load_data(ticker, period, interval)

if df is not None and not df.empty and len(df) >= 14:
    close = df['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + (gain / loss)))
    curr_rsi = float(rsi.iloc[-1])
    
    ema = close.ewm(span=min(50, len(df)), adjust=False).mean()
    
    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    sig_line = macd.ewm(span=9, adjust=False).mean()
    
    price = float(close.iloc[-1])
    m_val = float(macd.iloc[-1])
    s_val = float(sig_line.iloc[-1])
    
    if curr_rsi < 45 and m_val > s_val:
        sig = "BUY"
        col = "#00e676"
        icon = "↗"
        glow = "0 0 50px rgba(0, 230, 118, 0.85)"
    elif curr_rsi > 65 and m_val < s_val:
        sig = "SELL (SHORT)"
        col = "#ff1744"
        icon = "↘"
        glow = "0 0 50px rgba(255, 23, 68, 0.85)"
    else:
        sig = "HOLD / NEUTRAL"
        col = "#ff9100"
        icon = "➔"
        glow = "0 0 50px rgba(255, 145, 0, 0.85)"
    
    st.markdown('<div class="circle-container"><div class="glow-circle" style="border: 5px solid ' + col + '; color: ' + col + '; box-shadow: ' + glow + ';">' + icon + '</div><div class="signal-title" style="color: ' + col + ';">' + sig + '</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    cur_sym = "Rs. " if "KA" in ticker or "^KS100" in ticker else "$"
    
    c1.metric("Live Price", cur_sym + f"{price:,.2f}")
    c2.metric("RSI (14)", f"{curr_rsi:.2f}")
    
    t_text = "Bullish" if m_val > s_val else "Bearish"
    c3.metric("MACD Trend", t_text)
    
    st.markdown("---")
    st.subheader("📊 Technical Indicators Summary")
    st.write("- **EMA 50:** " + f"{float(ema.iloc[-1]):,.2f}")
    st.write("- **MACD Line:** " + f"{m_val:.2f}" + " | **Signal Line:** " + f"{s_val:.2f}")
else:
    st.warning("⚠️ Yahoo Finance per " + sel_tf + " ka live data is asset ke liye filhal dastyab nahi hai. Baraye meharbani 'Daily (1D)' ya 'Weekly (1W)' timeframe select karein.")
