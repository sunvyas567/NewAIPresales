from utils import headers

import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8001"

def show_reachouts():

    st.title("Reachouts")

    reachouts = requests.get(f"{API_URL}/reachouts", headers=headers()).json()

    df = pd.DataFrame(reachouts)
    #st.dataframe(df)
    if not df.empty:
        st.dataframe(df)
        #rid = st.selectbox("Select", df["id"])

        #if st.button("Generate Message"):
        #    res = requests.post(f"{API_URL}/reachouts/{rid}/render")
        #    st.session_state["msg"] = res.json()["message"]

        #if "msg" in st.session_state:
        #    st.text_area("Message", st.session_state["msg"], height=250)

        #if st.button("Send"):
        #    requests.post(f"{API_URL}/reachouts/{rid}/send")
        #    st.success("Sent")
    else:
        st.warning("No reachouts available")

def render_reachout_olf():

    st.subheader("📨 Reachout Center")

    channel = st.selectbox("Channel", ["Email", "LinkedIn"])

    lead_name = st.text_input("Lead Name")
    industry = st.text_input("Industry")
    solution = st.text_input("Solution")

    if channel == "Email":

        subject = st.text_input("Subject")
        body = st.text_area("Email Body", height=200)

        if st.button("✨ Generate with Agent"):
            payload = {
                "lead_name": lead_name,
                "solution": solution
            }

            response = requests.post(
                f"{API_BASE}/agents/run",
                params={"agent_type": "email"},
                json=payload
            )

            result = response.json()
            st.session_state["generated_subject"] = result.get("subject")
            st.session_state["generated_body"] = result.get("body")

        if "generated_subject" in st.session_state:
            subject = st.session_state["generated_subject"]
            body = st.session_state["generated_body"]

        if st.button("Send Email"):
            send_payload = {
                "to_email": "lead@email.com",
                "subject": subject,
                "body": body
            }

            requests.post(f"{API_BASE}/reachout/email", json=send_payload)
            st.success("Email sent")

    else:

        message = st.text_area("LinkedIn Message", height=200)

        if st.button("✨ Generate LinkedIn Message"):
            payload = {
                "lead_name": lead_name,
                "industry": industry
            }

            response = requests.post(
                f"{API_BASE}/agents/run",
                params={"agent_type": "linkedin"},
                json=payload
            )

            result = response.json()
            st.session_state["linkedin_message"] = result.get("message")

        if "linkedin_message" in st.session_state:
            message = st.session_state["linkedin_message"]

        if st.button("Post to LinkedIn"):
            requests.post(
                f"{API_BASE}/reachout/linkedin",
                json={"message": message}
            )
            st.success("Posted successfully")
