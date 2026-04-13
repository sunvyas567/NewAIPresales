import streamlit as st
import requests
from utils import headers

import os
API_URL = os.getenv("API_URL")

def show_pipeline():

    STAGE_COLORS = {
        "DRAFT": "#d6eaff",
        "QUALIFIED": "#ffe6c7",
        "PROPOSAL": "#e6dcff",
        "NEGOTIATION": "#ffd6e7",
        "WON": "#d7f5e6",
        "LOST": "#ffd6d6"
    }
    TEXT_COLOR = "#1f2933"
    #col1, col2, col3 = st.columns(3)

    #col1.metric("Total Opportunities", len(all_opps))
    #col2.metric("Pipeline Value", total_value)
    #col3.metric("Proposals", proposal_count)

    st.title("Opportunity Pipeline")

    if st.session_state.get("demo_mode", False):
        st.success("Shows the current sales pipeline with opportunities categorized by stage. Allows 'Next Stage' to move opportunities through the pipeline and see real-time updates.")

    res = requests.get(f"{API_URL}/crm/health")

    status = res.json()

    #print("CRM status in pipeline", status)

    if status["status"] == "offline":
        st.warning("CRM integration unavailable")

    res = requests.get(f"{API_URL}/opportunities/pipeline",headers=headers(),timeout=5)

    #print("Pipeline response", res.status_code, res.text)
    if res.status_code != 200:
        st.error("Failed to load pipeline")
        return
    data = res.json()

    #print("Pipeline data", data)
    #return
    total_deals = sum(len(v) for v in data.values())

    total_value = sum(
        opp["value"]
        for stage in data.values()
        for opp in stage
    )

    col1, col2 = st.columns(2)

    col1.metric("Total Deals", total_deals)
    col2.metric("Pipeline Value", f"${total_value}")

    stages = list(data.keys())

    cols = st.columns(len(stages))

    for i, stage in enumerate(stages):

        with cols[i]:
            #print("data", data[stage])
            st.subheader(stage.upper())

            for opp in data[stage]:

                with st.container():

                    #st.markdown(
                    #    f"""
                    #    **{opp['title']}**

                    #    Value: ${opp['value']}
                    #    """
                    #)
                    #color = STAGE_COLORS.get(stage, "#f7f7f7")
                    color = STAGE_COLORS.get(stage.upper(), "#f5f5f5")
                    #print("Color for stage", stage, "is", color)

                    if data.get(stage):
                        st.markdown(
                            f"""
                            <div style="
                                border:1px solid #ddd;
                                padding:12px;
                                border-radius:10px;
                                margin-bottom:10px;
                                background-color:{color};
                                color:{TEXT_COLOR};
                                box-shadow:0px 1px 3px rgba(0,0,0,0.15);
                            ">
                                <b>{opp.get('title','No Name')}</b><br>
                                💰 Value: ${opp.get('value',0)}<br>
                                🆔 ID: {opp.get('id')}<br>
                                🎯 Probability: {opp.get('probability', 0)}%
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        #print("No opportunities in stage", stage)
                        st.markdown(
                            """
                            <div style="
                                border:1px dashed #ccc;
                                padding:10px;
                                border-radius:8px;
                                margin-bottom:10px;
                                color:#888;
                                text-align:center;
                            ">
                            No opportunities
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    if stage not in ["WON", "LOST"]:

                        if st.button(
                            "Next Stage",
                            key=f"{opp['id']}_{stage}"
                        ):

                            requests.post(
                                f"{API_URL}/opportunities/{opp['id']}/next"
                            )

                            st.rerun()