import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components

from users_ui import show_users
from admin_ui import show_admin
from dashboard_ui import show_pipeline
from campaigns_ui import show_campaingns
from collaterals_ui import show_collaterals
from leads_ui import show_leads
from opportunities_ui import show_opportunties
from proposals_ui import show_proposals
from reachouts_ui import show_reachouts
from templates_ui import show_templates


import os
API_URL = os.getenv("API_URL")
 
def headers():
        return {
            "Authorization": f"Bearer {st.session_state.token}"
        }


# ------------------------------
# Helpers
# ------------------------------

def render_pipeline(stage):
    stages = ["REACHOUT", "open", "OPPORTUNITY", "PROPOSAL", "NEGOTIATION", "SOW", "CLOSED"]
    cols = st.columns(len(stages))
    for i, s in enumerate(stages):
        if s == stage:
            cols[i].success(s)
        elif stages.index(s) < stages.index(stage):
            cols[i].info(s)
        else:
            cols[i].write(s)


def badge(status):
    if status in ["APPROVED", "CLOSED"]:
        st.success(status)
    elif status in ["PENDING", "IN_PROGRESS"]:
        st.warning(status)
    elif status in ["REJECTED"]:
        st.error(status)
    else:
        st.info(status)


def show_login():

    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        res = requests.post(
            f"{API_URL}/auth/login",
            json={"email": email, "password": password}
        )

        if res.status_code != 200:
            st.error("Invalid login")
            return

        data = res.json()

        print("Login response:", data)

        st.session_state.token = data["access_token"]
        st.session_state.user = data["user"]
        st.session_state.tenant_id = data["tenant_id"]
        st.session_state.tenant_name = data["tenant_name"]
        st.session_state.plan = data["plan"]

        user = requests.get(
            f"{API_URL}/users/by-email/{email}"
        ).json()

        st.session_state.role = user["role"]

        st.success("Logged in")

        st.rerun()
def show_register():


        st.title("Register")

        company = st.text_input("Company Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            res = requests.post(f"{API_URL}/auth/register", json={
                "company_name": company,
                "email": email,
                "password": password
            })
            if res.status_code == 200:
                try:
                    st.json(res.json())
                except:
                    st.write(res.text)
            else:
                st.error(f"Error {res.status_code}")
                st.write(res.text)
            st.success(res.json())

def preview_personalize(text, user_name):

    replacements = {
        "{{first_name}}": "there",
        "{{company}}": "your organization",
        "{{industry}}": "your industry",
        "{{title}}": "your role",
        "{{solution_area}}": "your solution area",
        "{{sender_name}}": "Agent",
        "{{your_name}}": user_name
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text
def to_unicode_bold(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    return text.translate(str.maketrans(normal, bold))


def apply_to_lines(text, start_line, end_line, func):
    lines = text.split("\n")

    for i in range(start_line-1, end_line):
        if i < len(lines):
            lines[i] = func(lines[i])

    return "\n".join(lines)


def add_bullet(line):
    if line.strip():
        return f"• {line}"
    return line


def add_emoji(line):
    if line.strip():
        return f"🚀 {line}"
    return line
def show_main_app():

    # ------------------------
    # SESSION STATE
    # ------------------------

    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = None

    # ------------------------
    # AUTH GUARD
    # ------------------------

    if not st.session_state.token:

        menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

        if menu == "Login":
            show_login()   # move login code into a function

        elif menu == "Register":
            show_register()

        st.stop()   # 🚨 THIS IS THE KEY
    
    col1, col2 = st.columns([8, 2])

    with col1:
        st.markdown("## 🚀 Agentic Presales")

    with col2:
        st.markdown(f"👤 {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    st.divider()

    role = st.session_state.get("role")
    email = st.session_state.get("user")


    # ------------------------
    # AUTH
    # ------------------------
    with st.sidebar:

        st.markdown("## Navigation")

        section = st.radio(
            "Go to",
            ["Sales", "Presales Engagement", "Admin", "Dashboard"]
        )

        if section == "Dashboard":
            menu = "Dashboard"

        elif section == "Sales":
            menu = st.radio(
                "Sales",
                ["Leads", "Campaigns", "ReachOut" ]
            )

        elif section == "Presales Engagement":
            menu = st.radio(
                "Presale Engagement",
                ["Opportunities", "Proposals & SoW"]
            )

        elif section == "Admin":
            if role in ["admin", "sales"]:
                menu = st.radio(
                    "Admin",
                    ["Templates", "Collaterals", "Users", "SystemConfig"]
                )
            else:
                menu = st.radio(
                    "Admin",
                    ["Templates", "Collaterals", "SystemConfig"]
                )

    if menu == "Logout":
        st.session_state.token = None
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

    elif menu == "Users": 
        show_users()

    # ------------------------
    # DASHBOARD
    # ------------------------
    elif menu == "Dashboard":
        st.title("Revenue Dashboard")
        show_pipeline()
    # ------------------------
    # LEADS
    # ------------------------
    elif menu == "Leads":
        show_leads()
    # ------------------------
    # LEADS
    # ------------------------
    elif menu == "Collaterals":
        show_collaterals()
    # ------------------------
    # CAMPAIGNS
    # ------------------------
    elif menu == "Campaigns":
        show_campaingns()
    # ------------------------
    # LEADS
    # ------------------------
    elif menu == "Templates":
        show_templates()
    # ------------------------
    # LEADS
    # ------------------------
    elif menu == "ReachOut":
        show_reachouts()
    # ------------------------
    # LEADS
    # ------------------------
    elif menu == "Approvals":
        st.title("Approve Proposal")

        res = requests.get(f"{API_URL}/approvals/pending")

        proposals = res.json()

        for p in proposals:

            st.write(p["title"])

            col1, col2 = st.columns(2)

            if col1.button("Approve", key=f"a{p['id']}"):
                requests.post(f"{API_URL}/approvals/{p['id']}/approve")

            if col2.button("Reject", key=f"r{p['id']}"):
                requests.post(f"{API_URL}/approvals/{p['id']}/reject")

        #approval_id = st.number_input("Approval ID", value=1)

        #col1, col2 = st.columns(2)

        #with col1:
        #    if st.button("Approve"):
        #        res = requests.post(
        #            f"{API_URL}/approvals/{approval_id}/approve",
        #            headers=headers()
        #        )
        #        st.json(res.json())

        #with col2:
        #    if st.button("Reject"):
        #        res = requests.post(
        #            f"{API_URL}/approvals/{approval_id}/reject",
        #            headers=headers()
        #        )
        #        st.json(res.json())
    # ------------------------
    # LEADS
    # ------------------------
    elif menu == "SystemConfig":
        show_admin()
    # ------------------------
    # LEADS
    # ------------------------
    elif menu == "Opportunities":
        show_opportunties()
    # ==============================
    # PROPOSALS
    # ==============================
    elif menu == "Proposals & SoW":
        show_proposals()