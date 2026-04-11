from bs4 import BeautifulSoup
import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components

#from app.ui.main_app import to_unicode_bold
#from app.ui.mqinOLD import to_unicode_bold
from utils import headers
from unified_editor import unified_editor

import os
API_URL = os.getenv("API_URL")
def show_campaingns():

    st.title("📢 Campaigns")

    # ---------------------------------------
    # HELPERS (Formatting functions)
    # ---------------------------------------

    def to_unicode_bold(text):
        return "".join(
            chr(ord(c) + 0x1D400 - ord("A")) if "A" <= c <= "Z"
            else chr(ord(c) + 0x1D41A - ord("a")) if "a" <= c <= "z"
            else c
            for c in text
        )

    def add_bullet(text):
        return "\n".join([f"• {line}" for line in text.split("\n")])

    def add_emoji(text):
        return "🚀 " + text

    def apply_to_lines(text, start, end, func):
        lines = text.split("\n")
        for i in range(len(lines)):
            if start - 1 <= i <= end - 1:
                lines[i] = func(lines[i])
        return "\n".join(lines)

    from bs4 import BeautifulSoup

    def html_to_linkedin_text(html):

        soup = BeautifulSoup(html, "html.parser")

        lines = []

        for tag in soup.find_all(["p", "li", "h1", "h2", "h3", "strong", "b"]):

            text = tag.get_text().strip()

            if not text:
                continue

            # 🔥 Bold handling (convert to unicode bold)
            if tag.name in ["strong", "b"]:
                text = to_unicode_bold(text)

            # 🔥 Bullet handling
            if tag.name == "li":
                text = f"• {text}"

            lines.append(text)

        return "\n".join(lines)
    
    def preview_personalize(text, user_name):

        replacements = {
            "{{first_name}}": "there",
            "{{company}}": "your organization",
            "{{industry}}": "your industry",
            "{{i ndustry}}": "your industry",
            "{{title}}": "your role",
            "{{solution_area}}": "your solution area",
            "{{sender_name}}": "Agent",
            "{{your_name}}": user_name
        }
        #print("LinekdIn msg text before replacements",text)
        for k, v in replacements.items():
            text = text.replace(k, v)
        #print("LinkedIn Msg after replacement", text)
        return text
    def preview_personalize_old(text, user):
        return text.replace("{name}", user)

    
    # ---------------------------------------
    # CREATE CAMPAIGN
    # ---------------------------------------

    st.header("Create Campaign")

    demo = st.session_state.get("demo_mode", False)

    if demo:
        demo_campaigns = requests.get(f"{API_URL}/campaigns", headers=headers()).json()

    name = st.text_input("Campaign Name",value="" if not demo else demo_campaigns[0].get("name", ""),disabled=demo)

    campaign_type = st.selectbox(
        "Campaign Type",
        ["email", "linkedin", "event"],index=0 if not demo else ["email", "linkedin", "event"].index(demo_campaigns[0].get("campaign_type", "email")),disabled=demo
    )

    # ---------------------------------------
    # LEADS (skip for linkedin)
    # ---------------------------------------

    lead_ids = []

    if campaign_type != "linkedin" and not st.session_state.get("demo_mode", False):

        leads = requests.get(f"{API_URL}/leads").json()
        df_leads = pd.DataFrame(leads)

        selected_leads = st.multiselect(
            "Select Leads",
            df_leads["name"] if not df_leads.empty else []
        )

        lead_ids = df_leads[
            df_leads["name"].isin(selected_leads)
        ]["id"].tolist()

    else:
        st.info("LinkedIn campaigns do not require lead selection.")


    # ---------------------------------------
    # COLLATERALS
    # ---------------------------------------

    coll = requests.get(f"{API_URL}/collaterals",headers=headers()).json()

    #print("Collaterals fetched for campaign creation:", coll)

    if not coll:
        st.warning("No collaterals available")
    else:
        df_coll = pd.DataFrame(coll)

        selected_coll = st.multiselect(
            "Attach Collaterals",
            df_coll["title"] if not df_coll.empty else []
        )

        coll_ids = df_coll[
            df_coll["title"].isin(selected_coll)
        ]["id"].tolist()


    # ---------------------------------------
    # TEMPLATES
    # ---------------------------------------

    templates = requests.get(
        f"{API_URL}/templates/type/{campaign_type}",headers=headers()
    ).json()

    #print("Templates fetched for campaign creation:", templates)

    if not templates:
        st.warning("No templates available")
        df_temp = pd.DataFrame()
    else:
        df_temp = pd.DataFrame(templates)

    template_id = None
    preview_text = ""

    if not df_temp.empty:

        template_options = {
            row["name"]: row["id"]
            for _, row in df_temp.iterrows()
        }

        template_name = st.selectbox(
            "Template",
            list(template_options.keys())
        )

        template_id = template_options[template_name]

    else:
        st.warning("No templates available")

    #print("Selected template ID, name", template_id, template_name)
    # ---------------------------------------
    # LINKEDIN BUILDER
    # ---------------------------------------

    if campaign_type in ["linkedin", "email", "event"] and template_id:
    #if campaign_type  and template_id:

        preview = requests.get(
            f"{API_URL}/templates/{template_id}",
            headers=headers()

        ).json()

        if preview and isinstance(preview, list):
            default_text = preview[0].get("body", "")
        else:
            default_text = ""
        #print("Default message, preview, template_id", default_text, preview, template_id)
        if "linkedin_msg" not in st.session_state:
            st.session_state.linkedin_msg = default_text
            #print("1st time setting session state linkedin message to default text")
        else:
            # If template changes, update message
            #if st.session_state.linkedin_msg == "" or st.session_state.linkedin_msg == default_text:
            st.session_state.linkedin_msg = default_text
            #print("2nd time setting session state linkedin message to default text (template change or empty)", st.session_state.linkedin_msg)
        #print("Session state linkedin message : BEFORE PREVIEW", st.session_state.linkedin_msg)
        display_text = preview_personalize(
            st.session_state.linkedin_msg,
            st.session_state.get("user", "Your Name")
        )
        #print("Display text after personalization: AFTER PERSONLIZE", display_text)
        if campaign_type != "linkedin":
            st.subheader("Email-Event Message Builder")
        else:
            st.subheader("LinkedIn Message Builder")

        #col1, col2, col3 = st.columns([1,1,2])

        #with col1:
        #    action = st.selectbox("Format", ["Bold", "Bullets", "Emoji"])

        #with col2:
        #    mode = st.radio("Apply to", ["All", "Lines"])

        #with col3:
        #    start_line = st.number_input("Start Line", min_value=1, value=1)
       #     end_line = st.number_input("End Line", min_value=1, value=1)

        col1, col2 = st.columns(2)

        # -----------------------
        # EDITOR
        # -----------------------
        from streamlit_quill import st_quill

        # -----------------------
        # EDITOR (Quill)
        # -----------------------

        with col1:

            #html_value = st.session_state.linkedin_msg.replace("\n", "<br>")
            html_value = display_text.replace("\n", "<br>")

            #print("HTML value set in editor", html_value)

            # -------------------------
            # Detect change
            # -------------------------
            current_template = f"{campaign_type}_{template_id}"

            if st.session_state.get("last_template") != current_template:
                st.session_state.linkedin_msg = default_text
                st.session_state.last_template = current_template

            # -------------------------
            # Dynamic editor key
            # -------------------------
            editor_key = f"editor_{current_template}"


            linkedin_message_html = st_quill(
                value=html_value,
                html=True,
                key=editor_key,
                toolbar=[
                    ["bold", "italic", "underline"],
                    [{"list": "ordered"}, {"list": "bullet"}],
                    ["link"],
                    ["clean"]
                ]
            )

            # 🔥 Convert HTML → LinkedIn-safe text
            linkedin_message = html_to_linkedin_text(linkedin_message_html)

            # Store clean text (important)
            st.session_state.linkedin_msg = linkedin_message
        
        with col2:

            preview_html = f"""
            <div style="background:#f3f2ef;padding:20px;">
                <div style="background:white;padding:16px;border-radius:10px;">
                    <b>Your Name</b><br><br>
                    <div style="white-space:pre-wrap;font-size:14px;">
                        {linkedin_message}
                    </div>
                </div>
            </div>
            """

            components.html(preview_html, height=350)
        #with col1:
        #    linkedin_message = st.text_area(
        #        "Edit Message",
        #        value=display_text,
        #        height=350
        #    )

        # -----------------------
        # PREVIEW
        # -----------------------

        #with col2:

        #    preview_html = f"""
        #    <div style="background:#f3f2ef;padding:20px;">
        #        <div style="background:white;padding:16px;border-radius:10px;">
        #            <b>Your Name</b><br><br>
        #            <div style="white-space:pre-wrap;">
        #                {linkedin_message}
        #            </div>
        #        </div>
        #    </div>
        #    """

        #    components.html(preview_html, height=350)

        # -----------------------
        # APPLY FORMATTING
        # -----------------------

        #if st.button("Apply Formatting"):

            #text = st.session_state.linkedin_msg

            #if action == "Bold":
            #    func = to_unicode_bold
            #elif action == "Bullets":
            #    func = add_bullet
            #else:
            #    func = add_emoji

            #if mode == "All":
            #    new_text = func(text)
            #else:
           #     new_text = apply_to_lines(text, start_line, end_line, func)

            #st.session_state.linkedin_msg = new_text
            #st.rerun()

        preview_text = linkedin_message


    # ---------------------------------------
    # CREATE CAMPAIGN BUTTON
    # ---------------------------------------
    demo = st.session_state.get("demo_mode", False)

    if st.button("Create Campaign", disabled=demo):
    #if st.button("Create Campaign"):

        payload = {
            "name": name,
            "campaign_type": campaign_type,
            "template_id": int(template_id) if template_id else None,
            "lead_ids": lead_ids,
            "collateral_ids": coll_ids,
            "description": preview_text #if campaign_type == "linkedin" else ""
        }

        res = requests.post(
            f"{API_URL}/campaigns/create",
            json=payload
        )

        if res.status_code == 200:
            st.success("Campaign Created")
        else:
            st.error("Failed to create campaign")


    # ---------------------------------------
    # RUN CAMPAIGN
    # ---------------------------------------

    st.divider()
    st.header("Run Campaign")

    campaigns = requests.get(f"{API_URL}/campaigns", headers=headers()).json()
    df = pd.DataFrame(campaigns)

    #st.dataframe(df)

    col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])

    col1.write("Campaign Name")
    col2.write("Campaign Type")
    col3.write("Campaign Status")
    col4.write("Campaign Preview")
    col5.write("Campaign Actions")

    for _, row in df.iterrows():

        col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])

        col1.write(row["name"])
        col2.write(row["campaign_type"])
        col3.write(row.get("status", "CREATED"))

        # -------------------------
        # Keys
        # -------------------------
        btn_key = f"preview_btn_{row['id']}"      # ✅ button key
        state_key = f"preview_data_{row['id']}"   # ✅ session state key

        # -------------------------
        # Initialize state (SAFE)
        # -------------------------
        if state_key not in st.session_state:
            st.session_state[state_key] = None
        #print(f"Session state for {state_key} initialized to", st.session_state[state_key])
        # -------------------------
        # ▶ Preview Button
        # -------------------------
        if col4.button("Preview Campaign Message", key=btn_key):

            # OPTION 1: from backend API
            # msgs = requests.post(
            #     f"{API_URL}/reachouts/campaign/{row['id']}/generate"
            # ).json()

            # OPTION 2: from existing data (your current logic)
            #msgs = row.get("preview_messages", [])

            msgs = row.get("description", [])
            st.session_state[state_key] = msgs
            #print("Preview messages stored in session state", st.session_state[state_key])
            st.rerun()   # ✅ ensures clean refresh

        # -------------------------
        # ▶ Run Button
        # -------------------------
        disabled = (row.get("status") in ["COMPLETED", "completed"])

        if col5.button("Run", key=f"run_{row['id']}", disabled=disabled):
            requests.post(f"{API_URL}/campaigns/{row['id']}/start")
            st.success("Campaign started")
            st.rerun()

        # -------------------------
        # 👇 Show Preview
        # -------------------------
        msgs = st.session_state.get(state_key)
        #print("Preview messages to display", msgs)
        if msgs:
            st.write(msgs)
        if demo:
            st.info("Demo Mode: Showing completed campaign flow")
            #for m in msgs:
            #    with st.expander(f"{m.get('lead')} - {m.get('company')}"):
            #        st.write(m.get("message"))
        # 👁 Preview
        #if col4.button("Preview Campaign Message", key=f"preview_{row['id']}"):
            #msgs = requests.post(
            #    f"{API_URL}/reachouts/campaign/{row['id']}/generate"
            #).json()

            #st.session_state[f"preview_{row['id']}"] = msgs
        #    st.session_state[f"preview_{row['id']}"] = row.get("preview_messages", [])

        # ▶ Run
        #disabled = (row.get("status") == "COMPLETED" or row.get("status") == "completed")

        #if col5.button("Run", key=f"run_{row['id']}", disabled=disabled):
        #    requests.post(f"{API_URL}/campaigns/{row['id']}/start")
        #    st.success("Campaign started")
        #    st.rerun()

        # 👇 Show preview below row
       # if st.session_state.get(f"preview_{row['id']}"):

       #     for m in st.session_state[f"preview_{row['id']}"]:
       #         with st.expander(f"{m['lead']} - {m['company']}"):
       #             st.write(m["message"])

    #campaign_id = None

    #if not df.empty:

    #    campaign_options = {
    #        row["name"]: row["id"]
    #        for _, row in df.iterrows()
    #    }

    #    selected_campaign = st.selectbox(
    #        "Campaigns",
    #        list(campaign_options.keys())
    #    )

    #    campaign_id = campaign_options[selected_campaign]

    #else:
    #    st.warning("No campaigns available")


    # ---------------------------------------
    # START CAMPAIGN
    # ---------------------------------------

    #if campaign_id and st.button("Start Campaign"):

    #    requests.post(f"{API_URL}/campaigns/{campaign_id}/start")

    #    st.success("Campaign executed, Reachouts Generated")


    # ---------------------------------------
    # PREVIEW MESSAGES
    # ---------------------------------------

    #if campaign_id and st.button("Preview Campaign Messages"):

    #    resp = requests.post(
    #        f"{API_URL}/reachouts/campaign/{campaign_id}/generate"
    #    )

    #    if resp.status_code == 200:

    #        msgs = resp.json()

    #        df_msgs = pd.DataFrame(msgs)

    #        st.dataframe(df_msgs)

    #        for m in msgs:

    #            with st.expander(f"{m['lead']} - {m['company']}"):
    #                st.write(m["message"])

    #    else:
    #        st.error("Message generation failed")