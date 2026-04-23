    #from app.models import reachout
import streamlit as st
import requests
from utils import headers, badge, render_pipeline

import os
API_URL = os.getenv("API_URL")
def show_opportunties():

    st.title("Opportunities")

    # -------------------------
    # Reachout → Opportunity
    # -------------------------
    demo = st.session_state.get("demo_mode", False)

    if demo:
        st.success("Step 4: Opportunity created from Eligible Reachouts → AI suggestions available")

    st.subheader("Convert Reachouts")

    reachouts = requests.get(
        f"{API_URL}/reachouts",
        headers=headers()
    ).json()

    reachouts = [r for r in reachouts if r["status"] == "SENT"]

    for r in reachouts:

        col1, col2, col3, col4 = st.columns([3,2,2,2])

        col1.write(f"Reachout #{r['id']}")
        col2.write(r["channel"])
        col3.write(r["status"])

        #if col4.button("Create Opp", key=f"r_{r['id']}"):

        if r["opportunity_id"]:
            col4.button("Opportunity Created", disabled=True)
        else:
            if col4.button("Create Opportunity",disabled=demo):
                opp = requests.post(
                    f"{API_URL}/opportunities",
                    json={
                        "lead_id": r["lead_id"],
                        "stage_id": 1,   # default to first stage
                        "title": f"Opportunity for Reachout #{r['id']}",
                        "value": 10000,   # default value
                        "probability": 10,
                        "reachout_id": r["id"]   # 🔗 link reachout to opportunity
                    },
                    headers=headers()
                )
                if opp.status_code == 200:
                    data = opp.json()
                    r["opportunity_id"] = data.get("id")
                else:
                    st.error(f"Failed to create opportunity: {opp.text}")
                #r["opportunity_id"] = opp.json().get("id")
                st.rerun()
            #st.session_state["selected_reachout"] = r
            #st.switch_page("pages/3_Opportunities.py")


    # -------------------------
    # Opportunities List
    # -------------------------

    st.subheader("Existing Opportunities")

    opps = requests.get(f"{API_URL}/opportunities", headers=headers()).json()

    for opp in opps:

        with st.container():

            col1, col2, col3, col4, col5 = st.columns([2,3,2,2,2])

            col1.write(f"#{opp['id']}")
            col2.write(opp["title"])
            col3.write(f"${opp['value']}")

            crm_id = opp.get("crm_id")
        # crm_id = opp.get("crm_id")

            if crm_id:
                col4.success(f"CRM: {crm_id}")
                #st.button("Synced", disabled=True)
            else:
                if col4.button("Sync CRM",disabled=demo):
                    requests.post(f"{API_URL}/opportunities/{opp['id']}/sync-crm",headers=headers())
                    st.rerun()
            #if crm_id:
            #    col4.success(f"CRM: {crm_id}")
            #else:
            #    col4.warning("Not Synced")
            #col4.success(f"CRM: {crm_id}") if crm_id else col4.warning("Not Synced")

            badge(opp.get("status", "OPEN"))

            render_pipeline(opp.get("status", "OPEN"))

            # -----------------
            # AI Suggestion
            # -----------------

            is_open = (opp.get("status") or "").upper() == "OPEN"

            if not is_open:
                st.warning("AI Suggest is only available for OPEN opportunities")

            if col5.button("AI Suggest", key=f"ai_{opp['id']}", disabled=not is_open):
                # call API
            #if col5.button("AI Suggest", key=f"ai_{opp['id']}"):

                res = requests.get(
                    f"{API_URL}/opportunities/{opp['id']}/analyze",
                    headers=headers()
                )

                st.session_state[f"ai_{opp['id']}"] = res.json()

            ai = st.session_state.get(f"ai_{opp['id']}")

            if ai:
                st.info(f"""
    Solution: {ai.get('solution_area')}
    Template: {ai.get('recommended_template')}
    """)

    # -----------------
   
            # Actions
            # -----------------