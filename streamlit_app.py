import requests
import streamlit as st

import sys
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL")


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="Presales AI Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------
# HIDE DEFAULT SIDEBAR
# -----------------------
#st.markdown("""
#<style>
#[data-testid="stSidebarNav"] {display: none;}
#</style>
#""", unsafe_allow_html=True)

# ------------------------------------------------
# Global Styling
# ------------------------------------------------

st.markdown("""
<style>

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
#header {visibility: hidden;}


/* Reduce top padding */
.block-container {
    padding-top: 1.5rem;
}


 /* 1. Ensure the sidebar is actually visible */
    [data-testid="stSidebarNav"] {
        display: block !important;
    }

    /* 2. Set Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
    }

    /* 3. Style only the navigation links, not every single element */
    section[data-testid="stSidebar"] .st-emotion-cache-17l69k g, 
    section[data-testid="stSidebar"] span {
        color: white !important;
    }

    /* 4. Fix for the "Active" page background so text doesn't disappear */
    [data-testid="stSidebarNavLink"] {
        background-color: transparent !important;
    }
    [data-testid="stSidebarNavLink"]:hover {
        background-color: #1e293b !important;
    }
/* Card styling */
.card {
    padding: 14px;
    border-radius: 10px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    margin-bottom: 10px;
}


/* Metric cards */
.metric-card {
    padding: 18px;
    border-radius: 10px;
    background: #f1f5f9;
    border: 1px solid #e5e7eb;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)



# ------------------------------------------------
# Default Mode
# ------------------------------------------------

if "mode" not in st.session_state:
    st.session_state.mode = "landing"



# ------------------------------------------------
# Landing Page
# ------------------------------------------------

if st.session_state.mode == "landing":

    from landing_page import show_landing_page

    show_landing_page()



# ------------------------------------------------
# Demo Mode
# ------------------------------------------------

elif st.session_state.mode == "demo":

    #if st.button("🚀 Try Demo"):

    res = requests.post(
        f"{API_URL}/auth/login",
        json={"email": "demo@demo.com", "password": "demo123"}
    )

    data = res.json()

    st.session_state.token = data["access_token"]
    st.session_state.tenant_id = data["tenant_id"]
    st.session_state.user = "demo@demo.com"
    st.session_state.demo_mode = True
    st.session_state.mode = "app"
    st.rerun()
    #show_main_app()

    #from demo_ui import show_demo

    #show_demo()



# ------------------------------------------------
# Full Application
# ------------------------------------------------

elif st.session_state.mode == "app":

    # App Header
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
        <h2 style="margin:0;">🚀 Presales AI Platform</h2>
    </div>
    """, unsafe_allow_html=True)

    from main_app import show_main_app

    show_main_app()