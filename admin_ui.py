import streamlit as st
import requests

import os
API_URL = os.getenv("API_URL")

def show_admin():
    
    st.title("System Config")

    cfg = requests.get(f"{API_URL}/config").json()

    st.json(cfg)

    if st.session_state.get("demo_mode", False):
            st.success("System configuration used for CRM. Database, AI Modles, Email , LinkedIn integration setup")