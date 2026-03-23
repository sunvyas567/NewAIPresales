from dashboard_ui import show_pipeline
import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components

API_URL = "http://localhost:8001"

#st.set_page_config(page_title="PreSales CRM", layout="wide")


        
def headers():
        return {
            "Authorization": f"Bearer {st.session_state.token}"
        }

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

        st.session_state.token = data["access_token"]
        st.session_state.user = email

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

    #if "token" not in st.session_state:
    #    st.warning("Please login")
    #    st.session_state.mode = "landing"
    #   st.rerun()
    #   return
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
        st.markdown("## 🚀 AgenticAI")

    with col2:
        st.markdown(f"👤 {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    st.divider()
    #st.set_page_config(
    #    page_title="AgenticAI",
    #    page_icon="🚀",
    #    layout="wide"
    #)
    role = st.session_state.get("role")
    email = st.session_state.get("user")

    #menu1 = [
    #        "Dashboard",
    #        "Leads",
    #        "Collaterals",
    #        "Campaigns",
    #       "Templates",
    #        "ReachOut",
    #        "Opportunities",
    #        "Proposals",
    #        "Approvals",
    #        "SystemConfig",
    #        "Logout"
    #        ]

 
    #col1, col2 = st.columns([8,1])

    #with col2:

    #    if st.button("🏠 Home"):
    #        st.session_state.mode = "landing"
    #        st.rerun()

    #    if role in ["admin", "sales"]:
    #        menu1.append("Users")

    #    menu = st.sidebar.radio("Menu", menu1)

    #    st.sidebar.markdown("---")
    #    st.sidebar.markdown(f"👤 Role - {role}")
    #    st.sidebar.markdown(f"Id: **{email}**")


    # ------------------------
    # AUTH
    # ------------------------
    with st.sidebar:

        st.markdown("## Navigation")

        section = st.radio(
            "Go to",
            ["Dashboard", "Sales", "Engagement", "Admin"]
        )

        if section == "Dashboard":
            menu = "Dashboard"

        elif section == "Sales":
            menu = st.radio(
                "Sales",
                ["Leads", "Opportunities", "Proposals"]
            )

        elif section == "Engagement":
            menu = st.radio(
                "Engagement",
                ["Campaigns", "ReachOut"]
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
        from users_ui import show_users
        show_users()

    # ------------------------
    # DASHBOARD
    # ------------------------

    elif menu == "Dashboard":
        st.title("Revenue Dashboard")
        #from dashboard_ui import show_pipeline

        show_pipeline()

        #company_id = st.number_input("Company ID", value=1)

        #if st.button("Load Dashboard"):
        #    res = requests.get(
        #        f"{API_URL}/dashboard/{company_id}",
        #        headers=headers()
           # )
        #    data = res.json()
        #    st.metric("Total Pipeline", data.get("total_pipeline", 0))
        #    st.metric("Weighted Pipeline", data.get("weighted_pipeline", 0))


    # ------------------------
    # LEADS
    # ------------------------

    elif menu == "Leads":

        st.header("Leads")

        #st.header("Leads")

        tab1, tab2 = st.tabs(["Upload Leads", "View Leads"])

        ###################################
        # Upload Leads
        ###################################

        with tab1:

            uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

            if uploaded_file:

                files = {"file": uploaded_file.getvalue()}

                res = requests.post(
                    f"{API_URL}/leads/upload",
                    headers=headers(),
                    files={"file": uploaded_file}
                )

                st.write(res.json())


        ###################################
        # View Leads
        ###################################

        with tab2:

            res = requests.get(
                f"{API_URL}/leads",
                headers=headers()
            )

            leads = res.json()

            if leads:

                #import pandas as pd

                df = pd.DataFrame(leads)

                st.subheader("Filters")

                col1, col2, col3 = st.columns(3)

                with col1:
                    industry_filter = st.selectbox(
                        "Industry",
                        ["All"] + sorted(df["industry"].dropna().unique().tolist())
                    )

                with col2:
                    country_filter = st.selectbox(
                        "Country",
                        ["All"] + sorted(df["country"].dropna().unique().tolist())
                    )

                with col3:
                    source_filter = st.selectbox(
                        "Source",
                        ["All"] + sorted(df["source"].dropna().unique().tolist())
                    )

                if industry_filter != "All":
                    df = df[df["industry"] == industry_filter]

                if country_filter != "All":
                    df = df[df["country"] == country_filter]

                if source_filter != "All":
                    df = df[df["source"] == source_filter]

                st.subheader("Lead List")

                st.dataframe(df)

        #uploaded_file = st.file_uploader(
        #    "Upload Leads CSV/Excel",
        #    type=["csv", "xlsx"]
        #)

        #if uploaded_file:

        #    files = {"file": uploaded_file}

        #    res = requests.post(
        #        f"{API_URL}/leads/upload",
        #        files=files
        #    )

        #    if res.status_code == 200:
        #        data = res.json()
        #        st.success(f"{data['inserted']} leads inserted")
        #        st.warning(f"{data['skipped_duplicates']} duplicates skipped")
        #        st.json(res.json())
        #if st.button("Refresh Leads"):

        #    res = requests.get(f"{API_URL}/leads")

        #    leads = res.json()

        #    df = pd.DataFrame(leads)

        #    st.dataframe(df)
        
        st.title("Create Lead")

        company_id = st.number_input("Company ID", value=1)
        name = st.text_input("Name")
        email = st.text_input("Email")
        linkedin = st.text_input("LinkedIn URL")

        if st.button("Create Lead"):
            res = requests.post(
                f"{API_URL}/leads/{company_id}",
                headers=headers(),
                json={
                    "name": name,
                    "email": email,
                    "linkedin_url": linkedin
                }
            )
            st.json(res.json())

    elif menu == "Collaterals":

        st.header("Collateral Library")

        tab1, tab2 = st.tabs(["Upload", "Library"])

        with tab1:

            st.subheader("Upload Collateral")

            title = st.text_input("Title")

            type = st.selectbox(
                "Type",
                [
                    "corporate",
                    "solution",
                    "case_study",
                    "brochure",
                    "demo"
                ]
            )

            solution_area = st.selectbox(
                "Solution Area",
                [
                    "Generic",
                    "AI",
                    "Automation",
                    "Cloud",
                    "Infra",
                    "Data"
                ]
            )

            industry = st.selectbox(
                "Industry",
                [
                    "Generic",
                    "BFSI",
                    "Healthcare",
                    "Retail",
                    "Manufacturing"
                ]
            )

            description = st.text_area("Description")

            file = st.file_uploader("Upload File", type=["pdf","ppt","pptx"])

            if st.button("Upload"):

                files = {"file": file}

                data = {
                    "title": title,
                    "type": type,
                    "solution_area": solution_area,
                    "industry": industry,
                    "description": description
                }

                res = requests.post(
                    f"{API_URL}/collaterals/upload",
                    files=files,
                    data=data
                )

                st.success("Collateral uploaded")

        st.subheader("Add Demo Link")

        link = st.text_input("Demo Link")

        if st.button("Add Link"):

            payload = {
                "title": title,
                "type": type,
                "solution_area": solution_area,
                "industry": industry,
                "description": description,
                "link": link
            }

            requests.post(
                f"{API_URL}/collaterals/link",
                json=payload
            )

            st.success("Link added")
        
        with tab2:

            res = requests.get(f"{API_URL}/collaterals")

            if res.status_code == 200:
                try:
                    st.json(res.json())
                    data = res.json()

                    if data:

                        #import pandas as pd

                        df = pd.DataFrame(data)

                        st.dataframe(
                            df[
                                [
                                    "title",
                                    "type",
                                    "solution_area",
                                    "industry",
                                    "file_url",
                                    "link_url"
                                ]
                            ]
                        )
                except:
                    st.write(res.text)
            else:
                st.error(f"Error {res.status_code}")
                st.write(res.text)
                
    # ------------------------
    # CAMPAIGNS
    # ------------------------

    elif menu == "Campaigns":

        st.title("Create Campaign")

        name = st.text_input("Campaign Name")

        campaign_type = st.selectbox(
            "Campaign Type",
            ["email", "linkedin", "event"]
        )

        # ---------- Leads (skip for linkedin) ----------

        lead_ids = []

        if campaign_type != "linkedin":

            leads = requests.get(f"{API_URL}/leads").json()
            df_leads = pd.DataFrame(leads)

            selected_leads = st.multiselect(
                "Select Leads",
                df_leads["name"]
            )

            lead_ids = df_leads[
                df_leads["name"].isin(selected_leads)
            ]["id"].tolist()

        else:

            st.info("LinkedIn campaigns do not require lead selection.")


        # ---------- Collaterals ----------

        coll = requests.get(f"{API_URL}/collaterals").json()
        df_coll = pd.DataFrame(coll)

        selected_coll = st.multiselect(
            "Attach Collaterals",
            df_coll["title"]
        )

        coll_ids = df_coll[
            df_coll["title"].isin(selected_coll)
        ]["id"].tolist()


        # ---------- Templates ----------

        templates = requests.get(
            f"{API_URL}/templates/type/{campaign_type}"
        ).json()

        df_temp = pd.DataFrame(templates)

        template_id = None

        if not df_temp.empty:

            template_options = {
                row["name"]: row["id"]
                for _, row in df_temp.iterrows()
            }

            template = st.selectbox(
                "Template",
                list(template_options.keys())
            )

            template_id = template_options[template]

            print("Selected template ID:", template_id)

        else:

            st.warning("No templates available")


        # ---------- LinkedIn Content Preview ----------

        if campaign_type == "linkedin":

            

            preview = requests.get(
                f"{API_URL}/templates/{template_id}",
                timeout=5
            ).json()

            if preview and isinstance(preview, list):
                default_text = preview[0].get("body", "")
            else:
                default_text = ""

            if "linkedin_msg" not in st.session_state:
                st.session_state.linkedin_msg = default_text

            # 👇 APPLY PERSONALIZATION HERE
            display_text = preview_personalize(
                st.session_state.linkedin_msg,
                st.session_state.get("user", "Your Name")
            )
            print("LinkedIn Display text:", display_text)
            st.markdown(
                """
                <div style="
                border:1px solid #e5e7eb;
                border-radius:12px;
                padding:20px;
                background:white;
                box-shadow:0 1px 3px rgba(0,0,0,0.08);
                margin-bottom:20px;
                ">
                """,
                unsafe_allow_html=True
                )

            st.subheader("LinkedIn Message Builder")
            st.caption("Edit message and preview how it appears on LinkedIn")
            st.info("Use emojis (🚀, 👉) and bullets (•) and Bold options for better engagement. LinkedIn does not support rich text formatting.")

            col1, col2, col3 = st.columns([1,1,2])

            with col1:
                action = st.selectbox(
                    "Format",
                    ["Bold", "Bullets", "Emoji"]
                )

            with col2:
                mode = st.radio(
                    "Apply to",
                    ["All", "Lines"]
                )

            with col3:
                start_line = st.number_input("Start Line", min_value=1, value=1)
                end_line = st.number_input("End Line", min_value=1, value=1)
        
            col1, col2 = st.columns([1,1])

            # ----------------------
            # MESSAGE EDITOR
            # ----------------------

            with col1:

                st.markdown("### LinkedIn Message")

                linkedin_message = st.text_area(
                    "Edit LinkedIn Message",
                    value=display_text,
                    height=350
                )

            # ----------------------
            # LINKEDIN PREVIEW
            # ----------------------
            
            with col2:

                st.markdown("### LinkedIn Preview")

                preview_text = linkedin_message

                preview_html = f"""
            <div style="
                height:350px;
                overflow-y:auto;
                background:#f3f2ef;
                padding:20px;
                border-radius:10px;
                border:1px solid #ddd;
            ">

                <div style="
                    border:1px solid #d9d9d9;
                    border-radius:12px;
                    background:white;
                    padding:16px;
                    max-width:420px;
                    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;
                    box-shadow:0 1px 2px rgba(0,0,0,0.08);
                ">

                    <div style="display:flex;align-items:center;margin-bottom:10px;">
                        
                        <img src="https://static.licdn.com/sc/h/8s162nmbcnfkg7a0k8nq9wwqo"
                        width="40"
                        style="border-radius:50%;margin-right:10px;">

                        <div>
                            <div style="font-weight:600;font-size:14px;">
                                Your Name
                            </div>

                            <div style="color:#666;font-size:12px;">
                                AI Sales Specialist • 1st
                            </div>
                        </div>
                    </div>

                    <div style="
                        font-size:14px;
                        line-height:1.6;
                        white-space:pre-wrap;
                        color:#1d2226;
                    ">
                        {preview_text}
                    </div>

                    <div style="
                        margin-top:15px;
                        font-size:12px;
                        color:#666;
                        border-top:1px solid #eee;
                        padding-top:10px;
                    ">
                        👍 Like &nbsp;&nbsp; 💬 Comment &nbsp;&nbsp; 🔁 Repost &nbsp;&nbsp; ✉ Send
                    </div>

                </div>

            </div>
            """

                #st.markdown(preview_html, unsafe_allow_html=True)
                components.html(preview_html, height=380, scrolling=True)
            

            if st.button("Apply Formatting"):

                text = st.session_state.linkedin_msg

                if action == "Bold":
                    func = to_unicode_bold
                elif action == "Bullets":
                    func = add_bullet
                else:
                    func = add_emoji

                if mode == "All":
                    new_text = func(text)
                else:
                    new_text = apply_to_lines(text, start_line, end_line, func)

                st.session_state.linkedin_msg = new_text
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        # ---------- Create Campaign ----------

        if st.button("Create Campaign"):

            payload = {
                "name": name,
                "campaign_type": campaign_type,
                "template_id": int(template_id) if template_id else None,
                "lead_ids": lead_ids,
                "collateral_ids": coll_ids,
                "description": preview_text if campaign_type == "linkedin" else ""
            }

            requests.post(
                f"{API_URL}/campaigns/create",
                json=payload
            )

            st.success("Campaign Created")

            
        st.divider()

        st.subheader("Run Campaign")

        campaigns = requests.get(f"{API_URL}/campaigns").json()

        df = pd.DataFrame(campaigns)

        st.dataframe(df)


        if not df.empty:

            campaign_options = {
                row["name"]: row["id"]
                for _, row in df.iterrows()
            }

            template = st.selectbox(
                "Campiagns",
                list(campaign_options.keys())
            )

            campaign_id = campaign_options[template]

        else:

            st.warning("No campaigns available")

        #campaign_id = st.number_input("Campaign ID")
        print("Selected campaign ID:", campaign_id)
        if st.button("Start Campaign"):

            requests.post(f"{API_URL}/campaigns/{int(campaign_id)}/run")

            st.success("Campaign executed , Reachouts Generated")


        if st.button("Preview Campaign Messages"):

            resp = requests.post(
                f"{API_URL}/reachouts/campaign/{int(campaign_id)}/generate"
            )

            if resp.status_code == 200:

                msgs = resp.json()

                df_msgs = pd.DataFrame(msgs)

                st.dataframe(df_msgs)

                for m in msgs:

                    with st.expander(f"{m['lead']} - {m['company']}"):

                        st.write(m["message"])

            else:

                st.error("Message generation failed")

    elif menu == "Campaignsold":
        st.title("Create Campaign")

        name = st.text_input("Campaign Name")

        campaign_type = st.selectbox(
            "Type",
            ["email", "linkedin", "event"]
        )

        leads = requests.get(f"{API_URL}/leads").json()
        df_leads = pd.DataFrame(leads)

        lead_ids = st.multiselect(
            "Select Leads",
            df_leads["name"]
        )

        coll = requests.get(f"{API_URL}/collaterals").json()
        df_coll = pd.DataFrame(coll)

        coll_ids = st.multiselect(
            "Select Collaterals",
            df_coll["title"]
        )

        #templates = requests.get(f"{API_URL}/templates").json()
        templates = requests.get(
            f"{API_URL}/templates/type/{campaign_type}"
        ).json()
        df_temp = pd.DataFrame(templates)

        #if not df_temp.empty and "name" in df_temp.columns:
            #template = st.selectbox("Template", df_temp["name"])
        #    template = st.selectbox(
        #        "Template",
        #        df_temp.apply(
        #            lambda x: f"{x['name']} ({x['target_role']})",
        #            axis=1
        #        )
        #    )
        #else:
        #    st.warning("No templates available for this campaign type.")

        #template = st.selectbox("Template", df_temp["name"])

        #template_id = df_temp[df_temp["name"] == template]["id"].values[0]

        template_options = {
            row["name"]: row["id"]
            for _, row in df_temp.iterrows()
        }

        if template_options:
            
            #template = st.selectbox(
            #    "Template",
            #    df_temp.apply(
            #        lambda x: f"{x['name']} ({x['target_role']})",
            #        axis=1
            #    )
            #)
            template = st.selectbox(
                "Template",
                list(template_options.keys())
            )

            template_id = template_options[template]

        else:

            st.warning("No templates available")
            template_id = None

        if st.button("Create Campaign"):

            payload = {
                "name": name,
                "campaign_type": campaign_type,
                "template_id": int(template_id),
                "lead_ids": df_leads[df_leads["name"].isin(lead_ids)]["id"].tolist(),
                "collateral_ids": df_coll[df_coll["title"].isin(coll_ids)]["id"].tolist()
            }

            requests.post(f"{API_URL}/campaigns/create", json=payload)

            st.success("Campaign Created")

        st.divider()

        st.subheader("Run Campaign")

        campaigns = requests.get(f"{API_URL}/campaigns").json()

        df = pd.DataFrame(campaigns)

        st.dataframe(df)

        campaign_id = st.number_input("Campaign ID")

        if st.button("Run Campaign"):

            requests.post(f"{API_URL}/campaigns/{int(campaign_id)}/run")

            st.success("Campaign executed , Reachouts Generated")


        if st.button("Generate Campaign Messages"):

            resp = requests.post(
                f"{API_URL}/reachouts/campaign/{int(campaign_id)}/generate"
            )

            if resp.status_code == 200:

                msgs = resp.json()

                df_msgs = pd.DataFrame(msgs)

                st.dataframe(df_msgs)

                for m in msgs:

                    with st.expander(f"{m['lead']} - {m['company']}"):

                        st.write(m["message"])

            else:

                st.error("Message generation failed")
        
    elif menu == "Templates":
        st.header("Templates")

        tab1, tab2 = st.tabs(["Create Template", "Template Library"])

        with tab1:

            name = st.text_input("Template Name")

            campaign_type = st.selectbox(
                "Campaign Type",
                ["email", "linkedin", "event"]
            )

            target_role = st.selectbox(
                "Target Role",
                ["generic", "CTO", "CDO", "VP", "Director"]
            )

            subject = ""

            if campaign_type == "email":

                subject = st.text_input("Email Subject")

            body = st.text_area(
                "Template Body",
                height=250
            )

            if st.button("Create Template"):

                payload = {
                    "name": name,
                    "campaign_type": campaign_type,
                    "target_role": target_role,
                    "subject": subject,
                    "body": body
                }

                requests.post(
                    f"{API_URL}/templates/create",
                    json=payload
                )

                st.success("Template Created")

        with tab2:

            res = requests.get(f"{API_URL}/templates")

            templates = res.json()

            if templates:

                df = pd.DataFrame(templates)

                st.dataframe(
                    df[
                        [
                            "id",
                            "name",
                            "campaign_type",
                            "target_role",
                            "is_default"
                        ]
                    ]
                )
                template_id = st.number_input("Template ID to duplicate")

                if st.button("Duplicate Template"):

                    requests.post(
                        f"{API_URL}/templates/{template_id}/duplicate"
                    )

                    st.success("Template duplicated")
    # ------------------------
    # OPPORTUNITIES
    # ------------------------
    elif menu == "ReachOut":

        st.header("Reachouts")

        res = requests.get(f"{API_URL}/reachouts")

        reachouts = res.json()

        if reachouts:

            df = pd.DataFrame(reachouts)

            st.dataframe(df)

            reachout_id = st.selectbox(
                "Select Reachout",
                df["id"]
            )

            row = df[df["id"] == reachout_id].iloc[0]

            if st.button("Generate Message"):

                res = requests.post(
                    f"{API_URL}/reachouts/{reachout_id}/render"
                )

                data = res.json()

                st.session_state["msg"] = data["message"]

            if "msg" in st.session_state:

                st.session_state["msg"] = st.text_area(
                    "Preview/Edit Message",
                    st.session_state["msg"],
                    height=250
                )

            if row["channel"] == "email":

                email = st.text_input("Lead Email")

                if st.button("Send Email"):

                    requests.post(
                        f"{API_URL}/reachouts/{reachout_id}/send",
                        json={"lead_email": email}
                    )

                    st.success("Email sent")

            if row["channel"] == "linkedin":

                if st.button("Post to LinkedIn"):

                    requests.post(
                        f"{API_URL}/reachouts/{reachout_id}/send"
                    )

                    st.success("Posted")
    elif menu == "Opportunities":

        st.title("Opportunities")

        # ---------------------------------------------------
        # Section 1 : Reachouts → Convert to Opportunity
        # ---------------------------------------------------

        st.subheader("Convert Reachouts to Opportunities")

        reachouts = requests.get(
            f"{API_URL}/reachouts",
            headers=headers()
        ).json()

        # show only replied reachouts
        reachouts = [r for r in reachouts if r["status"] == "sent"]

        if len(reachouts) == 0:
            st.info("No replied reachouts available for conversion")

        else:

            for r in reachouts:

                col1, col2, col3, col4 = st.columns([3,2,2,2])

                with col1:
                    st.write(f"Reachout #{r['id']}")

                with col2:
                    st.write(r["channel"])

                with col3:
                    st.write(r["status"])

                with col4:

                    key = f"opp_created_{r['id']}"

                    if key not in st.session_state:
                        st.session_state[key] = False

                    if st.session_state[key]:
                        st.button(
                            "Opportunity Created",
                            disabled=True,
                            key=f"disabled_{r['id']}"
                        )

                    else:

                        if st.button(
                            "Create Opportunity",
                            key=f"create_{r['id']}"
                        ):
                            st.session_state["selected_reachout"] = r
                            st.rerun()

        st.divider()

        # ---------------------------------------------------
        # Section 2 : Opportunity Form
        # ---------------------------------------------------

        st.subheader("Opportunity Details")

        selected = st.session_state.get("selected_reachout")

        if selected:

            st.success(
                f"Creating opportunity from Reachout #{selected['id']} ({selected['channel']})"
            )

            lead_id = selected["lead_id"]
            default_title = f"Opportunity from Reachout #{selected['id']}"

        else:

            lead_id = st.number_input("Lead ID", value=1)
            default_title = "New Sales Opportunity"

        company_id = st.number_input("Company ID", value=1)

        stage_id = st.number_input("Stage ID", value=1)

        title = st.text_input(
            "Title",
            value=default_title
        )

        value = st.number_input(
            "Value",
            value=10000
        )

        probability = st.slider(
            "Probability",
            0.0,
            1.0,
            0.5
        )

        colA, colB = st.columns(2)

        with colA:

            if st.button("Create Opportunity"):

                res = requests.post(
                    f"{API_URL}/opportunities/{company_id}",
                    headers=headers(),
                    json={
                        "lead_id": lead_id,
                        "stage_id": stage_id,
                        "title": title,
                        "value": value,
                        "probability": probability
                    }
                )

                if res.status_code == 200:

                    st.success("Opportunity Created Successfully")

                    if selected:
                        st.session_state[f"opp_created_{selected['id']}"] = True

                    st.session_state["selected_reachout"] = None

                    st.rerun()

                else:
                    st.error("Error creating opportunity")

        with colB:

            if st.button("Create Fresh Opportunity"):

                st.session_state["selected_reachout"] = None
                st.rerun()

        st.divider()

        # ---------------------------------------------------
        # Section 3 : Existing Opportunities
        # ---------------------------------------------------

        st.subheader("Existing Opportunities")

        opps = requests.get(
            f"{API_URL}/opportunities",
            headers=headers()
        ).json()

        if len(opps) == 0:
            st.info("No opportunities created yet")

        else:

            for opp in opps:

                col1, col2, col3, col4, col5 = st.columns([2,3,2,2,2])

                with col1:
                    st.write(f"Opp #{opp['id']}")

                with col2:
                    st.write(opp["title"])

                with col3:
                    st.write(f"${opp['value']}")

                with col4:

                    crm_id = opp.get("crm_id")

                    if crm_id:
                        st.success(f"CRM ID: {crm_id}")
                    else:
                        st.warning("Not Synced")

                with col5:

                    if st.button(
                        "AI Solution",
                        key=f"ai_btn_{opp['id']}"
                    ):

                        res = requests.get(
                            f"{API_URL}/opportunities/{opp['id']}/analyze",
                            headers=headers()
                        )

                        data = res.json()

                        # Ensure we always store a dictionary
                        if isinstance(data, dict):
                            st.session_state[f"ai_result_{opp['id']}"] = data
                        else:
                            st.session_state[f"ai_result_{opp['id']}"] = None

                        #st.session_state[f"ai_{opp['id']}"] = res.json()

                if f"ai_{opp['id']}" in st.session_state:

                    ai = st.session_state[f"ai_result_{opp['id']}"]
                    if ai:

                        st.info(
                            f"""
                Solution Area: {ai.get('solution_area','N/A')}

                Template: {ai.get('recommended_template','N/A')}

                Collaterals:
                {", ".join(ai.get('recommended_collaterals', []))}
                """
                        )

                    else:

                        st.warning("AI could not determine a solution for this opportunity.")

                #with col5:

                #    if opp.get("crm_id"):

                #        st.button(
                #            "Synced",
                #            disabled=True,
                #            key=f"sync_done_{opp['id']}"
                #        )

                #    else:

                #        if st.button(
                #            "Sync to CRM",
                #            key=f"sync_{opp['id']}"
                #        ):

                #            res = requests.post(
                #                f"{API_URL}/opportunities/{opp['id']}/sync-crm",
                #                headers=headers()
                #            )

                #            if res.status_code == 200:

                #                st.success("Synced to CRM")
                #                st.rerun()

                #            else:
                #                st.error("CRM sync failed")

    # ------------------------
    # PROPOSALS
    # ------------------------

    elif menu == "Proposals":
        st.header("📄 Proposal Management")

        # -------------------------------------------------
        # Load Opportunities
        # -------------------------------------------------

        opp_res = requests.get(
            f"{API_URL}/opportunities",
            headers=headers()
        )

        if opp_res.status_code != 200:
            st.error("Unable to load opportunities")
            st.stop()

        opps = opp_res.json()

        opp_map = {o["title"]: o["id"] for o in opps}

        opp_name = st.selectbox(
            "Select Opportunity",
            list(opp_map.keys())
        )

        opp_id = opp_map[opp_name]


        # -------------------------------------------------
        # Load Templates
        # -------------------------------------------------

        temp_res = requests.get(
            f"{API_URL}/templates?type=proposal",
            headers=headers()
        )

        templates = temp_res.json()

        template_map = {t["name"]: t["id"] for t in templates}

        template_name = st.selectbox(
            "Select Proposal Template",
            list(template_map.keys())
        )

        template_id = template_map[template_name]


        # -------------------------------------------------
        # AI Toggle
        # -------------------------------------------------

        use_ai = st.toggle("Use AI Generation")


        st.divider()


        # -------------------------------------------------
        # Create Proposal
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if st.button("Create Proposal"):

                res = requests.post(
                    f"{API_URL}/proposals/create",
                    json={
                        "opportunity_id": opp_id
                    },
                    headers=headers()
                )

                if res.status_code == 200:

                    data = res.json()

                    st.success(f"Proposal created: ID {data['id']}")

                else:
                    st.error(res.text)


        # -------------------------------------------------
        # Load Proposals for Opportunity
        # -------------------------------------------------

        prop_res = requests.get(
            f"{API_URL}/proposals?opportunity_id={opp_id}",
            headers=headers()
        )

        proposals = []

        if prop_res.status_code == 200:
            proposals = prop_res.json()


        if proposals:

            proposal_map = {
                f"{p['title']} (ID {p['id']})": p["id"]
                for p in proposals
            }

            proposal_name = st.selectbox(
                "Select Proposal",
                list(proposal_map.keys())
            )

            proposal_id = proposal_map[proposal_name]

        else:

            st.info("No proposals created yet")
            proposal_id = None


        # -------------------------------------------------
        # Generate Proposal Content
        # -------------------------------------------------

        with col2:

            if st.button("Generate Proposal Content"):

                if proposal_id is None:
                    st.warning("Create proposal first")
                else:

                    res = requests.post(
                        f"{API_URL}/proposals/{proposal_id}/generate",
                        params={
                            "template_id": template_id,
                            "use_ai": use_ai
                        },
                        headers=headers()
                    )

                    if res.status_code == 200:

                        data = res.json()

                        st.success(
                            f"Proposal generated. Version {data['version']}"
                        )

                    else:
                        st.error(res.text)


        st.divider()


        # -------------------------------------------------
        # Proposal Versions
        # -------------------------------------------------

        if proposal_id:

            st.subheader("Proposal Versions")

            ver_res = requests.get(
                f"{API_URL}/proposals/{proposal_id}/versions",
                headers=headers()
            )

            if ver_res.status_code == 200:

                versions = ver_res.json()

                for v in versions:

                    with st.expander(
                        f"Version {v['version_number']}"
                    ):

                        st.write(v["content"])

            else:
                st.info("No versions yet")

        if st.button("Preview Proposal"):

            res = requests.post(
                f"{API_URL}/proposals/{proposal_id}/preview",
                params={"template_id": template_id},
                headers=headers()
            )

            preview = res.json()["preview"]

            st.text_area("Preview", preview, height=400)

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "Download PDF",
                f"{API_URL}/proposals/{proposal_id}/download/pdf"
            )

        with col2:

            st.link_button(
                "Download PPT",
                f"{API_URL}/proposals/{proposal_id}/download/ppt"
            )     
                
    # ------------------------
    # APPROVALS (ADMIN)
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

    elif menu == "SystemConfig":

        st.header("System Configuration")

        resp = requests.get(f"{API_URL}/config")

        cfg = resp.json()

        st.subheader("SMTP")

        st.text_input("Host", cfg["smtp_host"], disabled=True)
        st.text_input("User", cfg["smtp_user"], disabled=True)
        st.text_input("Password", cfg["smtp_password"], disabled=True)

        st.subheader("LinkedIn")

        st.text_input("Org URN", cfg["linkedin_org"], disabled=True)
        st.text_input("Token", cfg["linkedin_token"], disabled=True)

        st.subheader("CRM (Odoo)")

        st.text_input("URL", cfg["odoo_url"], disabled=True)
        st.text_input("DB", cfg["odoo_db"], disabled=True)
        st.text_input("Odoo User", cfg["odoo_user"], disabled=True)
        st.text_input("Password", cfg["odoo_password"], disabled=True)