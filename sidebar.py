import streamlit as st

def get_menu_for_role(role):

    if role == "sales":
        return {
            "sales":{
                "Leads": "Leads",
                "Reachouts": "Reachouts",
                "Campaigns": "Campaigns",
                "Opportunities": "Opportunities",
                "Proposals": "Proposals",
                "Collaterals": "Collaterals",
                "Templates": "Templates",
                "Admin": "Admin",
                "Users": "Users"
            }}
    elif role == "presales":
        return {"presales": {
            "Leads": "Leads",
            "Reachouts": "Reachouts",
            "Campaigns": "Campaigns",
            "Opportunities": "Opportunities",
            "Proposals": "Proposals",
            "Collaterals": "Collaterals",
            "Templates": "Templates"
        }},
    else :
        return {"admin": {
            "Leads": "Leads",
            "Reachouts": "Reachouts",
            "Opportunities": "Opportunities",
            "Proposals": "Proposals",
            "Campaigns": "Campaigns"
        }}
    #}.get(role, {})


def render_sidebar():

    user = st.session_state.get("user", "Guest")
    role = st.session_state.get("role", "Sales")

    st.sidebar.title(f"👤 {user}")
    st.sidebar.caption(f"Role: {role}")

    menu = get_menu_for_role(role)

    selected_page = None

    for group, items in menu.items():
        st.sidebar.markdown(f"### {group}")
        #print("items",items)
        for label, page in items.items():
            if st.sidebar.button(label):
                selected_page = page

    return selected_page