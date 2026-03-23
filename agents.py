import streamlit as st
import requests

API_BASE = "http://localhost:8000/api"


def render_agents():

    st.subheader("🤖 Agent Playground")

    agent_type = st.selectbox(
        "Select Agent",
        ["email", "linkedin"]
    )

    payload = st.text_area("Payload (JSON)")

    if st.button("Run Agent"):
        import json
        response = requests.post(
            f"{API_BASE}/agents/run",
            params={"agent_type": agent_type},
            json=json.loads(payload)
        )

        st.json(response.json())
