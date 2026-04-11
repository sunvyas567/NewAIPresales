import streamlit as st
import requests

API_URL = "http://localhost:8001"

def show_admin():
    
    st.title("System Config")

    cfg = requests.get(f"{API_URL}/config").json()

    st.json(cfg)