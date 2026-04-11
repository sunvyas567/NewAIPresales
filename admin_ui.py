import streamlit as st
import requests

import os
API_URL = os.getenv("API_URL")

def show_admin():
    
    st.title("System Config")

    cfg = requests.get(f"{API_URL}/config").json()

    st.json(cfg)