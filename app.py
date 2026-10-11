import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PSX Trading Wizards", page_icon="📈", layout="wide")

# JavaScript to auto-remove the red badge and floating buttons
js_cleaner = """
<script>
function removeBadges() {
    // Select all potential badges, footers, and host bars
    const selectors = [
        'div[class*="viewerBadge"]',
        'a[class*="viewerBadge"]',
        'div[class*="stAppViewerToolBar"]',
        '[data-testid="stStatusWidget"]',
        '[data-testid="stHeader"]',
        'footer'
    ];
    
    selectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => el.remove());
    });
    
    // Also target elements inside shadow root if present
    document.querySelectorAll('*').forEach(el => {
        if (el.shadowRoot) {
            selectors.forEach(selector => {
                el.shadowRoot.querySelectorAll(selector).forEach(e => e.remove());
            });
        }
    });
}

// Run immediately and continuously every 500ms
removeBadges();
setInterval(removeBadges, 500);
</script>
"""

# Inject JS into app
components.html(js_cleaner, height=0, width=0)

# CSS Backup for instant hidden state
hide_css = """
    <style>
    #MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    div[class*="viewerBadge"], a[href*="streamlit.io"] {
        display: none !important;
    }
    </style>
"""
st.markdown(hide_css, unsafe_allow_html=True)

# Main Application Content
st.title("PSX Trading Wizards 📈")
st.write("Welcome to PSX Trading Wizards! Your custom stock market analysis platform.")
