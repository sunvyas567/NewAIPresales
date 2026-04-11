import streamlit as st
import requests
import pandas as pd

from utils import headers

API_URL = "http://localhost:8001"

def show_templates():

    st.title("Templates")

    demo = st.session_state.get("demo_mode", False)

    if demo:
        st.info("Demo Mode: Template creation disabled")
    else:
        name = st.text_input("Name")
        body = st.text_area("Body")

    if st.button("Create", disabled=demo):
        requests.post(
            f"{API_URL}/templates/create",
            json={"name": name, "body": body}
        )
        st.success("Created")

    templates = requests.get(f"{API_URL}/templates", headers=headers()).json()

    df = pd.DataFrame(templates)
    st.dataframe(df)