import streamlit as st
from streamlit_quill import st_quill
from editor_utils import payload_to_html, html_to_payload
#from services.proposal_service import parse_to_payload
import requests


API_URL = "http://localhost:8001"


from core.parser_utils import parse_to_payload

def unified_editor(
    title,
    fetch_url,
    save_url,
    headers,
    key_prefix="editor"
):
    st.subheader(title)

    # -------------------------
    # LOAD CONTENT
    # -------------------------

    res = requests.get(fetch_url, headers=headers()).json()

    formatted = res.get("formatted", "")
    raw = res.get("raw")

    #print("Fetched Content:", formatted)
    #print("Fetched Raw Content:", raw)
    # Convert to HTML for Quill
    try:
        #print("Attempting to parse raw content to payload for editor.")
        payload = parse_to_payload(raw)
        #print("Parsed Payload:", payload)
        html_value = payload_to_html(payload)
        #print("Converted HTML Value:", html_value)
    except:
        #print("Failed to parse raw content. Falling back to formatted content.")
        html_value = formatted

    #print(("HTML Value for Editor:", html_value))
    # -------------------------
    # EDITOR
    # -------------------------
    edited_content = ""  # Initialize edited_content
    col1, col2 = st.columns([1,1])

    with col1:
        edited_content = st_quill(
            value=html_value,
            html=True,
            key=f"{key_prefix}_quill"
        )
    with col2:
        st.markdown(formatted)
    # -------------------------
    # ACTIONS
    # -------------------------

    col1, col2 = st.columns([1,1])

    if col1.button("💾 Save", key=f"{key_prefix}_save",disabled=st.session_state.get("demo_mode", False)):

        #print("Edited HTML Content:", edited_content)
        payload = html_to_payload(edited_content)

        requests.post(
            save_url,
            json={"content": payload},
            headers=headers()
        )

        st.success("Saved successfully")
        st.rerun()

    if col2.button("🔄 Reset", key=f"{key_prefix}_reset"):
        st.rerun()

    # -------------------------
    # PREVIEW
    # -------------------------

    #with st.expander("👁 Preview"):
    #    st.markdown(formatted)