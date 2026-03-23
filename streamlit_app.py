import streamlit as st


# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="Presales AI Platform",
    page_icon="🚀",
    layout="wide"
)


# ------------------------------------------------
# Global Styling
# ------------------------------------------------

st.markdown("""
<style>

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}


/* Reduce top padding */
.block-container {
    padding-top: 1.5rem;
}


/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}


/* Sidebar text color */
section[data-testid="stSidebar"] * {
    color: white !important;
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

    from demo_ui import show_demo

    show_demo()



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