import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="wide")

st.sidebar.title("📈 PSX Trading Wizards")
st.sidebar.markdown("By Ijaz Sardar")

stock_symbols = {
          "PSO (Pakistan State Oil)": "PSO.KA",
          "PRL (Pakistan Refinery)": "PRL.KA",
          "CNERGY (Cnergyico PK)": "CNERGY.KA",
          "NBP (National Bank of Pakistan)": "NBP.KA",
          "MLCF (Maple Leaf Cement)": "MLCF.KA"
}

selected_name = st.sidebar.selectbox("Select Market / Share", list(stock_symbols.keys()))
ticker = stock_symbols[selected_name]

timeframe_map = {
          "1 Minute": ("1d", "1m"),
          "5 Minutes": ("1d", "5m"),
          "15 Minutes": ("5d", "15m"),
          "1 Hour": ("1mo", "60m"),
          "4 Hours": ("1mo", "60m"),
          "Daily (1D)": ("6mo", "1d"),
          "Weekly (1W)": ("2y", "1wk")
}

selected_tf = st.sidebar.selectbox("Select Timeframe", list(timeframe_map.keys()))
period_val, interval_val = timeframe_map[selected_tf]

st.markdown(f"<h2 style='text-align: center; color: #00aced;'>Signal for: {selected_name} ({selected_tf})</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_stock_data(sym, period, interval):
          try:
                        df = yf.download(sym, period=period, interval=interval, progress=False)
                        return df
except Exception:
        return None

data = fetch_stock_data(ticker, period_val, interval_val)

if data is not None and not data.empty and len(data) >= 14:
          try:
                        close_prices = data['Close']
                        if isinstance(close_prices, pd.DataFrame):
                                          close_prices = close_prices.iloc[:, 0]

                        delta = close_prices.diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi = 100 - (100 / (1 + rs))
                        current_rsi = float(rsi.iloc[-1])

        ema_50 = close_prices.ewm(span=min(50, len(data)), adjust=False).mean()

        exp1 = close_prices.ewm(span=12, adjust=False).mean()
        exp2 = close_prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()

        current_price = float(close_prices.iloc[-1])
        current_macd = float(macd.iloc[-1])
        current_signal = float(signal_line.iloc[-1])

        if current_rsi < 45 and current_macd > current_signal:
                          signal = "STRONG BUY"
                          color = "#00FF00"
elif current_rsi > 65 and current_macd < current_signal:
                  signal = "STRONG SELL"
                  color = "#FF0000"
else:
                  signal = "HOLD / NEUTRAL"
                  color = "#FFA500"

        st.markdown(f"<div style='background-color: #1e1e1e; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid {color};'><h1 style='color: {color}; font-size: 38px; margin: 0;'>{signal}</h1></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Live Price", f"Rs. {current_price:.2f}")
        col2.metric("RSI (14)", f"{current_rsi:.2f}")
        col3.metric("MACD Trend", "Bullish" if current_macd > current_signal else "Bearish")

        st.markdown("---")
        st.subheader("📊 Key Indicators Summary")
        st.write(f"- **EMA:** {float(ema_50.iloc[-1]):.2f}")
        st.write(f"- **MACD Line:** {current_macd:.2f} | **Signal Line:** {current_signal:.2f}")
except Exception:
        st.error("Data processing error. Please try selecting 'Daily (1D)' timeframe.")
else:
    st.warning(f"⚠️ Yahoo Finance per {selected_tf} ka live data PSX ke liye filhal dastyab nahi hai. Baraye meharbani 'Daily (1D)' ya 'Weekly (1W)' timeframe select karein.")
      
