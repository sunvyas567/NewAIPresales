import streamlit as st
import requests
import pandas as pd

from utils import headers

API_URL = "http://localhost:8001"

def show_collaterals():

    st.title("Collaterals")

    demo = st.session_state.get("demo_mode", False)
    
    if not demo:
        title = st.text_input("Title")
        file = st.file_uploader("Upload", type=["pdf", "pptx"])

    if st.button("Upload",disabled=demo):
        requests.post(
            f"{API_URL}/collaterals/upload",
            files={"file": file},
            data={"title": title}
        )
        st.success("Uploaded")

    data = requests.get(f"{API_URL}/collaterals", headers=headers()).json()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)