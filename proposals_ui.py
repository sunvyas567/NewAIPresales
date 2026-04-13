import streamlit as st
import requests
from utils import badge, headers, render_pipeline
from unified_editor import unified_editor

import os
API_URL = os.getenv("API_URL")

def show_proposals():

    st.title("📄 Proposals")

    demo = st.session_state.get("demo_mode", False)

    if demo:
            st.success("Step 5 & 6: Proposals created , SOW generated and approved → Ready for download")
    # -------------------------
    # Opportunity
    # -------------------------
    opps = requests.get(f"{API_URL}/opportunities", headers=headers()).json()

    if not opps:
        st.stop()

    opp_map = {o["title"]: o["id"] for o in opps}

    opp_name = st.selectbox("Opportunity", list(opp_map.keys()))
    opp_id = opp_map[opp_name]

    opp_detail = requests.get(f"{API_URL}/opportunities/{opp_id}", headers=headers()).json()

    #is_open = opp_detail.get("status") == "OPEN"

    
    badge(opp_detail.get("stage"))
    render_pipeline(opp_detail.get("stage"))

    progress_map = {
        "OPEN": 20,
        "PROPOSAL": 50,
        "NEGOTIATION": 75,
        "CLOSED": 100
    }

    stage = opp_detail.get("stage", "OPEN")

    st.progress(progress_map.get(stage, 10) / 100)

    st.caption(f"Stage Progress: {stage}")

    # -------------------------
    # Proposal Templates
    # -------------------------

    templates = requests.get(
        f"{API_URL}/templates?type=proposal",
        headers=headers()
    ).json()

    template_map = {t["name"]: t["id"] for t in templates}

    template_name = st.selectbox("Proposal Template", list(template_map.keys()))
    template_id = template_map[template_name]

    # -------------------------
    # Mode
    # -------------------------

    is_open = opp_detail.get("stage") == "OPEN"

    mode = st.radio(
        "Mode",
        ["Template Only", "AI Assisted"],
        horizontal=True,
        index=0 if not demo else 1,
        disabled=not is_open
    )

    use_ai = mode == "AI Assisted"
    # -------------------------
    # Create
    # -------------------------
    if st.button("Create Proposal",disabled=not is_open):
        requests.post(f"{API_URL}/proposals/create", json={"opportunity_id": opp_id}, headers=headers())
        st.rerun()

    # -------------------------
    # Load
    # -------------------------
    proposals = requests.get(
        f"{API_URL}/proposals?opportunity_id={opp_id}",
        headers=headers()
    ).json()

    if not proposals:
        st.stop()

    selected = st.selectbox(
        "Proposal",
        proposals,
        format_func=lambda x: f"{x['title']} ({x['status']}) {x['sow_status']})"
    )

    proposal_id = selected["id"]

    
    badge(selected.get("status", "DRAFT"))

    # -------------------------
    # Generate
    # -------------------------
    if selected["status"] != "GENERATED":
        if st.button("Generate", disabled=not is_open):
            requests.post(
                f"{API_URL}/proposals/{proposal_id}/generate",
                params={"template_id": template_id, "use_ai": use_ai},
                headers=headers()
            )
            st.rerun()

    # -------------------------
    # EDIT PROPOSAL
    # -------------------------
    st.subheader("Edit Proposal")


    unified_editor(
        title="📄 Edit Proposal",
        fetch_url=f"{API_URL}/proposals/{proposal_id}/latest?type=proposal",
        save_url=f"{API_URL}/proposals/{proposal_id}/update",
        headers=headers,
        key_prefix=f"proposal_{proposal_id}"
    )
    
    # -------------------------
    # SOW
    # -------------------------
    st.subheader("📑 SOW")

    
    # -------------------------
    # Proposal Templates
    # -------------------------

    sow_templates = requests.get(
        f"{API_URL}/templates?type=sow",
        headers=headers()
    ).json()

    sow_template_map = {t["name"]: t["id"] for t in sow_templates}

    sow_template_name = st.selectbox("SoW Template", list(sow_template_map.keys()))
    sow_template_id = sow_template_map[sow_template_name]

    if selected["sow_status"] == "NOT_GENERATED":


        is_sow_not_generated = True;

        sow_mode = st.radio(
            "Mode",
            ["Template Only", "AI Assisted"],
            horizontal=True,
            disabled=not is_sow_not_generated
        )
        

        use_ai_for_sow = sow_mode == "AI Assisted"
        if st.button("Generate SOW"):
            requests.post(f"{API_URL}/proposals/{proposal_id}/sow/generate", 
                        params={"template_id": sow_template_id, "use_ai": use_ai_for_sow},
                        headers=headers())

    unified_editor(
        title="📑 Edit SOW",
        fetch_url=f"{API_URL}/proposals/{proposal_id}/latest?type=sow",
        save_url=f"{API_URL}/proposals/{proposal_id}/update-sow",
        headers=headers,
        key_prefix=f"sow_{proposal_id}"
    )
    #res = requests.get(

    if st.button("Download SOW"):

        res = requests.get(
            f"{API_URL}/proposals/{proposal_id}/sow/download",
            headers=headers()
        )

        if res.status_code == 200:
            st.download_button(
                label="Click to Download",
                data=res.content,
                file_name="sow.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.error("Download failed")

    # -------------------------
    # APPROVAL
    # -------------------------
    if selected["status"] == "DRAFT":
        if st.button("Submit for Approval"):
            requests.post(f"{API_URL}/proposals/{proposal_id}/submit", headers=headers())

    if selected["status"] == "PENDING":
        col1, col2 = st.columns(2)

        if col1.button("Approve"):
            requests.post(f"{API_URL}/approvals/approve", json={"proposal_id": proposal_id}, headers=headers())

        if col2.button("Reject"):
            requests.post(f"{API_URL}/approvals/reject", json={"proposal_id": proposal_id}, headers=headers())

    # -------------------------
    # DOWNLOAD
    # -------------------------
    #st.link_button("Download PDF", f"{API_URL}/proposals/{proposal_id}/download/pdf")
    #st.link_button("Download PPT", f"{API_URL}/proposals/{proposal_id}/download/ppt")


    if st.button("Download Proposal as PDF"):

        res = requests.get(
            f"{API_URL}/proposals/{proposal_id}/download/pdf",
            headers=headers()
        )

        if res.status_code == 200:
            st.download_button(
                label="Click to Download",
                data=res.content,
                file_name="proposal.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Download failed")
    
    if st.button("Download Proposal as PPT"):

        res = requests.get(
            f"{API_URL}/proposals/{proposal_id}/download/ppt",
            headers=headers()
        )

        if res.status_code == 200:
            st.download_button(
                label="Click to Download",
                data=res.content,
                file_name="proposal.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        else:
            st.error("Download failed")

    