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

.btn-
