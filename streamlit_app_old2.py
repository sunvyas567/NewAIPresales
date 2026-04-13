import streamlit as st


# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="Presales AI Platform",
    page_icon="🚀",
    layout="wide"
)

#st.write("MODE:", st.session_state.get("mode"))
#st.write("TOKEN:", "token" in st.session_state)
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
    #st.markdown("""
    #<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
    #    <h2 style="margin:0;">🚀 Presales AI Platform</h2>
    #</div>
    #""", unsafe_allow_html=True)

    from app.ui.main_app import show_main_app

    show_main_app()