if st.button("Generate Proposal"):
    response = requests.post(
        f"{API_BASE}/proposals/generate",
        json={
            "opportunity_id": selected_opportunity,
            "template_id": selected_template,
            "collateral_ids": selected_collaterals
        }
    )

    st.session_state["generated_proposal"] = response.json()["generated_proposal"]


if "generated_proposal" in st.session_state:
    st.text_area(
        "Proposal Preview",
        value=st.session_state["generated_proposal"],
        height=400
    )

    if st.button("Send Proposal"):
        requests.post(
            f"{API_BASE}/proposals/send",
            json={
                "to_email": client_email,
                "subject": "Proposal for Engagement",
                "body": st.session_state["generated_proposal"]
            }
        )

        st.success("Proposal sent successfully")

if st.button("Download PDF"):

    response = requests.post(
        f"{API_BASE}/proposals/export-pdf",
        json={
            "opportunity_id": selected_opportunity,
            "content": st.session_state["generated_proposal"]
        }
    )

    st.success("PDF Generated")

if proposal_id:
    history = requests.get(
        f"{API_BASE}/proposals/{proposal_id}/versions"
    ).json()

    st.subheader("Version History")

    for v in history:
        st.write(f"Version {v['version_number']} - {v['created_at']}")

if proposal_status == "Draft":
    if st.button("Submit for Approval"):
        requests.post(
            f"{API_BASE}/approval/submit",
            json={"proposal_id": proposal_id}
        )

elif proposal_status == "PendingApproval":

    if current_user_role == "approver":

        if st.button("Approve"):
            requests.post(
                f"{API_BASE}/approval/approve",
                json={
                    "proposal_id": proposal_id,
                    "user_id": current_user_id
                }
            )

        if st.button("Reject"):
            requests.post(
                f"{API_BASE}/approval/reject",
                json={
                    "proposal_id": proposal_id,
                    "user_id": current_user_id,
                    "comments": "Needs pricing correction"
                }
            )
