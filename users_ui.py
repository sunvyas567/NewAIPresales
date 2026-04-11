import streamlit as st
import requests

API_URL = "http://localhost:8001"


def show_users():

    st.title("User Management")

    st.subheader("Create User")

    demo = st.session_state.get("demo_mode", False)
    #name = st.text_input("Name")
    if demo:
        st.info("Demo Mode: User creation disabled")
    else:
        email = st.text_input("Email")

        password = st.text_input("Password", type="password")

        role = st.selectbox(
            "Role",
            ["admin", "presales", "sales", "viewer"]
        )

    if st.button("Create User", disabled=demo):

        res = requests.post(
            f"{API_URL}/users/create",
            json={
                #"name": name,
                "email": email,
                "password": password,
                "role": role
            }
        )

        st.success("User created")

        st.rerun()


    st.divider()

    st.subheader("Existing Users")

    res = requests.get(f"{API_URL}/users")

    users = res.json()

    for u in users:

        col1, col2, col3 = st.columns([2,2,1])

        col1.write(u["email"])

        col2.write(u["role"])

        if u["role"] in ["admin", "sales"]:
            col3.button("Delete", disabled=True, key=f"del_{u['id']}")
        else:
            if col3.button("Delete", key=f"del_{u['id']}",disabled=demo):
                requests.delete(f"{API_URL}/users/{u['id']}")
                st.rerun()
        #if col3.button("Delete", key=f"user_{u['id']}"):

        #    requests.delete(
        #        f"{API_URL}/users/{u['id']}"
        #    )

        #    st.rerun()
