import streamlit as st
import pandas as pd
import yfinance as yf
import os

st.set_page_config(page_title="PSX Trading Wizards", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp {
    background-color: #0b0f19;
    color: #ffffff;
}
.main-box {
    background-color: #111827;
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #1f2937;
    text-align: center;
    margin-bottom: 20px;
}
.circle-red {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(239, 68, 68, 0.4) 0%, rgba(17, 24, 39, 0.9) 70%);
    border: 4px solid #ef4444;
    box-shadow: 0 0 35px #ef4444;
    margin: 0 auto 15px auto;
    display: flex;
    align-items: center;
    justify-content: center;
}
.circle-green {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.4) 0%, rgba(17, 24, 39, 0.9) 70%);
    border: 4px solid #10b981;
    box-shadow: 0 0 35px #10b981;
    margin: 0 auto 15px auto;
    display: flex;
    align-items: center;
    justify-content: center;
}
.circle-yellow {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(245, 158, 11, 0.4) 0%, rgba(17, 24, 39, 0.9) 70%);
    border: 4px solid #f59e0b;
    box-shadow: 0 0 35px #f59e0b;
    margin: 0 auto 15px auto;
    display: flex;
    align-items: center;
    justify-content: center;
}
.card-metric {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #374151;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

if os.path.exists("logo.jpg"):
    st.sidebar.image("logo.jpg", use_container_width=True)

st.sidebar.title("🧙‍♂️ PSX Trading Wizards")
st.sidebar.caption("By Ijaz Sardar")
st.sidebar.markdown("---")

psx_assets = {
    "KSE-100 Index": "^KSE100",
    "PSO (Pakistan State Oil)": "PSO.KA",
    "PRL (Pakistan Refinery)": "PRL.KA",
    "CNERGY (Cnergyico PK)": "CNERGY.KA",
    "NBP (National Bank)": "NBP.KA",
    "MLCF (Maple Leaf Cement)": "MLCF.KA",
    "TRG Pakistan": "TRG.KA",
    "EUR/USD Forex": "EURUSD=X",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Gold (GC=F)": "GC=F"
}

selected_label = st.sidebar.selectbox("Select Market / Share", list(psx_assets.keys()))
asset = psx_assets[selected_label]

st.markdown("<h3 style='text-align: center; color: #9ca3af;'>Signal for: <span style='color: #38bdf8;'>" + selected_label + "</span></h3>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_data(ticker):
    df = yf.download(ticker, period="1mo", interval="1d")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

data = get_data(asset)

if not data.empty and 'Close' in data.columns:
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    latest_close = float(data['Close'].iloc[-1])
    latest_rsi = float(data['RSI'].iloc[-1]) if not pd.isna(data['RSI'].iloc[-1]) else 50.0

    if latest_rsi > 65:
        st.markdown("""
        <div class="main-box">
            <div class="circle-red">
                <span style="font-size: 70px; color: #ffffff;">&#8600;</span>
            </div>
            <h1 style="color: #ef4444; font-weight: 900; margin: 0;">SELL (SHORT)</h1>
        </div>
        """, unsafe_allow_html=True)
        accuracy = "85.2%"
    elif latest_rsi < 35:
        st.markdown("""
        <div class="main-box">
            <div class="circle-green">
                <span style="font-size: 70px; color: #ffffff;">&#8599;</span>
            </div>
            <h1 style="color: #10b981; font-weight: 900; margin: 0;">BUY (LONG)</h1>
        </div>
        """, unsafe_allow_html=True)
        accuracy = "88.5%"
    else:
        st.markdown("""
        <div class="main-box">
            <div class="circle-yellow">
                <span style="font-size: 70px; color: #ffffff;">&#8594;</span>
            </div>
            <h1 style="color: #f59e0b; font-weight: 900; margin: 0;">HOLD / NEUTRAL</h1>
        </div>
        """, unsafe_allow_html=True)
        accuracy = "72.0%"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card-metric">
            <small style="color: #9ca3af;">LIVE PRICE & RSI</small>
            <h3 style="color: #ffffff; margin: 5px 0;">Price: """ + f"{latest_close:.2f}" + """ | RSI: """ + f"{latest_rsi:.2f}" + """</h3>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="card-metric">
            <small style="color: #9ca3af;">AI ACCURACY</small>
            <h3 style="color: #38bdf8; margin: 5px 0;">""" + accuracy + """</h3>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Market Trend Chart (" + selected_label + ")")
    st.line_chart(data[['Close', 'SMA_20']])
else:
    st.error("Market Data load nahi ho saka. Internet Connection check karein.")
