import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components
from users_ui import show_users
from admin_ui import show_admin
from dashboard_ui import show_pipeline

import os
API_URL = os.getenv("API_URL")
 
def headers():
        return {
            "Authorization": f"Bearer {st.session_state.token}"
        }

def show_login():

    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        res = requests.post(
            f"{API_URL}/auth/login",
            json={"email": email, "password": password}
        )

        if res.status_code != 200:
            st.error("Invalid login")
            return

        data = res.json()

        print("Login response:", data)

        st.session_state.token = data["access_token"]
        st.session_state.user = data["user"]
        st.session_state.tenant_id = data["tenant_id"]
        st.session_state.tenant_name = data["tenant_name"]
        st.session_state.plan = data["plan"]

        user = requests.get(
            f"{API_URL}/users/by-email/{email}"
        ).json()

        st.session_state.role = user["role"]

        st.success("Logged in")

        st.rerun()
def show_register():


        st.title("Register")

        company = st.text_input("Company Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            res = requests.post(f"{API_URL}/auth/register", json={
                "company_name": company,
                "email": email,
                "password": password
            })
            if res.status_code == 200:
                try:
                    st.json(res.json())
                except:
                    st.write(res.text)
            else:
                st.error(f"Error {res.status_code}")
                st.write(res.text)
            st.success(res.json())
def show_main_app():

    # ------------------------
    # SESSION STATE
    # ------------------------

    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = None

    # ------------------------
    # AUTH GUARD
    # ------------------------

    if not st.session_state.token:

        menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

        if menu == "Login":
            show_login()   # move login code into a function

        elif menu == "Register":
            show_register()

        st.stop()   # 🚨 THIS IS THE KEY
    
    col1, col2 = st.columns([8, 2])

    with col1:
        st.markdown("## 🚀 Agentic Presales")

    with col2:
        st.markdown(f"👤 {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    st.divider()

    role = st.session_state.get("role")
    email = st.session_state.get("user")
    # ------------------------
    # AUTH
    # ------------------------
    with st.sidebar:

        st.markdown("## Navigation")

        section = st.radio(
            "Go to",
            ["Sales", "Presales Engagement", "Admin", "Dashboard"]
        )

        if section == "Dashboard":
            menu = "Dashboard"

        elif section == "Sales":
            menu = st.radio(
                "Sales",
                ["Leads", "Campaigns", "ReachOut" ]
            )

        elif section == "Presales Engagement":
            menu = st.radio(
                "Presale Engagement",
                ["Opportunities", "Proposals & SoW"]
            )

        elif section == "Admin":
            if role in ["admin", "sales"]:
                menu = st.radio(
                    "Admin",
                    ["Templates", "Collaterals", "Users", "SystemConfig"]
                )
            else:
                menu = st.radio(
                    "Admin",
                    ["Templates", "Collaterals", "SystemConfig"]
                )

    if menu == "Logout":
        st.session_state.token = None
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

    elif menu == "Users": 
        show_users()

    # ------------------------
    # DASHBOARD
    # ------------------------
    elif menu == "Dashboard":
        st.title("Revenue Dashboard")
        show_pipeline()
    # ------------------------
    # LEADS
    # ------------------------
    elif menu == "SystemConfig":
        show_admin()
    # ------------------