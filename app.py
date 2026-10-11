import streamlit as st

st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="wide")

hide_streamlit_style = """
    <style>
    /* Streamlit Cloud Bottom Red Badge / Hosted Button Hide */
    .stAppViewerToolBar, 
    [data-testid="stStatusWidget"],
    [data-testid="stHeader"],
    footer,
    #MainMenu,
    header {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Target Red Hosted with Streamlit badge specifically */
    div[class*="viewerBadge"],
    div[class*="styles_viewerBadge"],
    a[class*="viewerBadge"] {
        display: none !important;
    }

    /* Remove bottom margin/padding */
    .main .block-container {
        padding-bottom: 0px !important;
    }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Main Application Content
st.title("PSX Trading Wizards 📈")
st.write("Welcome to PSX Trading Wizards! Your custom stock market analysis platform.")
