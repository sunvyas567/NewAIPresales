import streamlit as st

def headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }

def badge(status):
    if status in ["APPROVED", "CLOSED"]:
        st.success(status)
    elif status in ["PENDING", "IN_PROGRESS"]:
        st.warning(status)
    elif status in ["REJECTED"]:
        st.error(status)
    else:
        st.info(status)

def render_pipeline(stage):
    stages = ["REACHOUT", "OPEN", "OPPORTUNITY", "PROPOSAL", "NEGOTIATION", "SOW", "CLOSED"]

    cols = st.columns(len(stages))

    for i, s in enumerate(stages):
        if s == stage:
            cols[i].success(s)
        elif stages.index(s) < stages.index(stage):
            cols[i].info(s)
        else:
            cols[i].write(s)