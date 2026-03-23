import streamlit as st
import requests


API_BASE = "http://localhost:8000/api"


def render_dashboard():

    st.subheader("📊 Pipeline Dashboard")

    try:
        response = requests.get(f"{API_BASE}/pipeline/summary")
        data = response.json()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Leads", data.get("leads", 0))
        col2.metric("Opportunities", data.get("opportunities", 0))
        col3.metric("Revenue", data.get("revenue", 0))
        col4.metric("Campaigns", data.get("campaigns", 0))

    except Exception as e:
        st.error(f"Dashboard error: {e}")
