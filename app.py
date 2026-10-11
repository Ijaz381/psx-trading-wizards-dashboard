import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0d1117; color: #ffffff; }

@keyframes pulseGlow {
    0% { transform: scale(1); box-shadow: 0 0 15px rgba(255, 145, 0, 0.4); }
    50% { transform: scale(1.06); box-shadow: 0 0 40px rgba(255, 145, 0, 0.9); }
    100% { transform: scale(1); box-shadow: 0 0 15px rgba(255, 145, 0, 0.4); }
}

.anim-circle {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 60px;
    background-color: #161b22;
    margin: 0 auto 15px auto;
    animation: pulseGlow 2s infinite ease-in-out;
}

.signal-title { font-size: 36px; font-weight: 900; text-align: center; letter-spacing: 2px; }
.metric-card { background-color: #161b22; border: 2px solid #30363d; border-radius: 14px; padding: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); }
.metric-label { color: #58a6ff; font-size: 15px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; }
.metric-val { color: #ffffff !important; font-size: 28px !important; font-weight: 800 !important; }

/* Hiding Streamlit Branding & Footer Badges Completely */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
div[data-testid="stDecoration"] {display: hidden;}
header {visibility: hidden;}
[data-testid="stFooter"] {display: none !important;}
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

# Voice Assistant Widget in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("🎙️ **Voice Assistant**")
voice_html = """
<div style="background: #161b22; padding: 12px; border-radius: 10px; border: 1px solid #30363d; text-align: center;">
    <button onclick="startListening()" style="background: #238636; color: white; border: none; padding: 10px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px;">🎙️ Speak Command</button>
    <p id="voice-status" style="color: #8b949e; font-size: 12px; margin-top: 8px;">Tap & speak market name</p>
</div>
<script>
function startListening() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Speech Recognition not supported in this browser.");
        return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    document.getElementById("voice-status").innerText = "Listening...";
    
    recognition.onresult = function(event) {
        const speechToText = event.results[0][0].transcript.toLowerCase();
        document.getElementById("voice-status").innerText = "Heard: " + speechToText;
    };
    
    recognition.onerror = function() {
        document.getElementById("voice-status").innerText = "Try again.";
    };
    
    recognition.start();
}
</script>
"""
st.sidebar.markdown(voice_html, unsafe_allow_html=True)

sel_name = st.sidebar.selectbox("Select Market / Share", list(symbols.keys()))
ticker = symbols[sel_name]

tf_map = {
    "Daily (1D)": ("6mo", "1d"),
    "Weekly (1W)": ("2y", "1wk"),
    "1 Hour": ("5d", "60m"),
    "15 Minutes": ("5d", "15m"),
    "5 Minutes": ("1d", "5m"),
    "1 Minute": ("1d", "1m")
}

sel_tf = st.sidebar.selectbox("Select Timeframe", list(tf_map.keys()))
period, interval = tf_map[sel_tf]

st.markdown("<h3 style='text-align: center; color: #58a6ff;'>Analyzing Market: " + sel_name + " (" + sel_tf + ")</h3>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data(sym, p, i):
    try:
        df_test = yf.download(sym, period=p, interval=i, progress=False)
        if df_test is None or len(df_test) < 10:
            # Fallback to Daily data if short timeframe fails
            return yf.download(sym, period="6mo", interval="1d", progress=False)
        return df_test
    except:
        return yf.download(sym, period="6mo", interval="1d", progress=False)

df = load_data(ticker, period, interval)

if df is not None and not df.empty:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    close = df['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + (gain / loss)))
    curr_rsi = float(rsi.iloc[-1]) if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50.0
    
    ema = close.ewm(span=min(50, len(close)), adjust=False).mean()
    
    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    sig_line = macd.ewm(span=9, adjust=False).mean()
    
    price = float(close.iloc[-1])
    m_val = float(macd.iloc[-1]) if not macd.empty else 0.0
    s_val = float(sig_line.iloc[-1]) if not sig_line.empty else 0.0
    
    if curr_rsi < 45 and m_val > s_val:
        sig = "BUY"
        col = "#00e676"
        icon = "↗"
    elif curr_rsi > 65 and m_val < s_val:
        sig = "SELL (SHORT)"
        col = "#ff1744"
        icon = "↘"
    else:
        sig = "HOLD / NEUTRAL"
        col = "#ff9100"
        icon = "➔"
    
    st.markdown(f'''
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 25px 0;">
        <div class="anim-circle" style="border: 5px solid {col}; color: {col};">{icon}</div>
        <div class="signal-title" style="color: {col};">{sig}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Text-to-Speech Button for Signal
    speech_text = f"The current signal for {sel_name} is {sig}. Live price is {price:.2f}."
    tts_html = f"""
    <div style="text-align: center; margin-bottom: 25px;">
        <button onclick="speakSignal()" style="background: #1f6feb; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer;">🔊 Listen to Signal</button>
    </div>
    <script>
    function speakSignal() {{
        const utterance = new SpeechSynthesisUtterance("{speech_text}");
        window.speechSynthesis.speak(utterance);
    }}
    </script>
    """
    st.markdown(tts_html, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    cur_sym = "Rs. " if "KA" in ticker or "^KS100" in ticker else "$"
    
    p_str = f"{price:,.2f}"
    r_str = f"{curr_rsi:.2f}"
    
    card1 = '<div class="metric-card"><div class="metric-label">Live Price</div><div class="metric-val">' + cur_sym + p_str + '</div></div>'
    card2 = '<div class="metric-card"><div class="metric-label">RSI (14)</div><div class="metric-val">' + r_str + '</div></div>'
    
    t_col = "#00e676" if m_val > s_val else "#ff1744"
    t_txt = "Bullish" if m_val > s_val else "Bearish"
    card3 = '<div class="metric-card"><div class="metric-label">MACD Trend</div><div class="metric-val" style="color: ' + t_col + ';">' + t_txt + '</div></div>'
    
    c1.markdown(card1, unsafe_allow_html=True)
    c2.markdown(card2, unsafe_allow_html=True)
    c3.markdown(card3, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 Technical Indicators Summary")
    st.write("- **EMA 50:** " + f"{float(ema.iloc[-1]):,.2f}")
    st.write("- **MACD Line:** " + f"{m_val:.2f}" + " | **Signal Line:** " + f"{s_val:.2f}")
else:
    st.warning("⚠️ Data load karne mein masla aa raha hai. Baraye meharbani doosra share ya timeframe select karein.")
