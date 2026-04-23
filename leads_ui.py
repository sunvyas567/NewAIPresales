import streamlit as st
import requests
import pandas as pd
#from app.ui.demo_ui import get_demo_leads
from utils import headers

import os
API_URL = os.getenv("API_URL")
def show_leads():

    st.title("Leads")
    demo = st.session_state.get("demo_mode", False)
    if demo:
        st.success("Step 1: Leads data loaded → Ready for campaign execution")
    tab1, tab2 = st.tabs(["Upload", "View"])

    with tab1:
        if demo:
            st.info("Demo Mode: Using sample leads data, click view tab to see leads table")

            
        else:
            file = st.file_uploader("Upload CSV", type=["csv"])

            if file:
                res = requests.post(
                    f"{API_URL}/leads/upload",
                    headers=headers(),
                    files={"file": file}
                )
                st.success("Uploaded")
                st.json(res.json())

    with tab2:

        leads = requests.get(
                f"{API_URL}/leads",
                headers=headers()
            ).json()

        if leads:
            df = pd.DataFrame(leads)
            st.dataframe(df)
        else:
            st.info("No leads available , please upload leads.")

        if demo:
            st.success("Step 1: Leads data loaded → Ready for campaign execution")