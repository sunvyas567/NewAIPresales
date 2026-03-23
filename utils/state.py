import streamlit as st

def init_state():
    if "user" not in st.session_state:
        st.session_state.user = None
