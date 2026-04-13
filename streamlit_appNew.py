import streamlit as st
from sidebar import render_sidebar   # your custom sidebar
from app.ui.main_appNew import show_login, show_register  # 👈 your existing functions

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="AI Presales",
    layout="wide"
)

# -----------------------
# HIDE DEFAULT SIDEBAR
# -----------------------
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
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
    # -----------------------
    # INIT SESSION
    # -----------------------
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Login"

    # -----------------------
    # AUTH FLOW
    # -----------------------
    if not st.session_state.logged_in:

        st.title("🔐 AI Presales Platform")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login"):
                st.session_state.auth_mode = "Login"

        with col2:
            if st.button("Register"):
                st.session_state.auth_mode = "Register"

        st.divider()

        # 👇 Use your existing functions
        if st.session_state.auth_mode == "Login":
            show_login()
        else:
            show_register()

        st.stop()


    # -----------------------
    # SIDEBAR (ROLE BASED)
    # -----------------------
    selected = render_sidebar()

    # -----------------------
    # PAGE ROUTING
    # -----------------------
    page_map = {
        "Dashboard": "pages/1_Dashboard.py",
        "Leads": "pages/2_Leads.py",
        "Reachouts": "pages/6_Reachouts.py",
        "Opportunities": "pages/3_Opportunities.py",
        "Proposals": "pages/4_Proposals.py",
        "Campaigns": "pages/5_Campaigns.py",
        "Collaterals": "pages/7_Collaterals",
        "Templates": "pages/8_Templates",
        "Admin": "pages/9_Admin",
        "Users": "pages/user_ui.py"
    }

    if selected:
        st.switch_page(page_map[selected])


    # -----------------------
    # DEFAULT LANDING
    # -----------------------
    st.title("🏠 AI Presales Dashboard")

    st.info("Use the sidebar to navigate modules")

    # Optional: show quick stats / welcome
    st.write(f"Welcome **{st.session_state.get('user')}** 👋")
    st.write(f"Role: **{st.session_state.get('role')}**")