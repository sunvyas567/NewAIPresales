import streamlit as st
import requests

API = "http://localhost:8001"

st.title("PreSales System Core Foundation")

#menu = st.sidebar.selectbox("Menu", ["Register", "Login"])
menu = st.sidebar.selectbox("Menu", 
    ["Register", "Login", "Create Lead", "Create Campaign""Dashboard",
    "Create Opportunity",
    "Move Opportunity",
])

if menu == "Register":
    company = st.text_input("Company Name")
    email = st.text_input("Admin Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post(
            f"{API}/auth/register",
            json={
                "company_name": company,
                "email": email,
                "password": password
            }
        )
        if res.status_code == 200:
            try:
                st.json(res.json())
            except:
                st.write(res.text)
        else:
            st.error(f"Error {res.status_code}")
            st.write(res.text)
        #st.json(res.json())

if menu == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{API}/auth/login",
            json={"email": email, "password": password}
        )
        st.json(res.json())

if menu == "Dashboard":
    res = requests.get(f"http://localhost:8000/dashboard/{company_id}")
    st.metric("Total Pipeline", res.json()["total_pipeline"])
    st.metric("Weighted Pipeline", res.json()["weighted_pipeline"])

if menu == "Create Opportunity":
    title = st.text_input("Title")
    value = st.number_input("Value")
    probability = st.slider("Probability", 0.0, 1.0, 0.5)

    if st.button("Create"):
        requests.post(
            f"http://localhost:8000/opportunities/{company_id}",
            json={
                "lead_id": 1,
                "stage_id": 1,
                "title": title,
                "value": value,
                "probability": probability
            }
        )
        st.success("Created")