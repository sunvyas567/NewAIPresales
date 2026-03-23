import streamlit as st

from modules.dashboard import render_dashboard
from modules.leads import render_leads
from modules.opportunities import render_opportunities
from modules.proposals import render_proposals
from modules.approval import render_approval
from modules.agents import render_agents
from modules.email import render_email
from modules.linkedin import render_linkedin
from modules.crm import render_crm
from modules.collateral import render_collateral


st.set_page_config(layout="wide")
st.title("🚀 GTM Revenue Console")

tabs = st.tabs([
    "📊 Dashboard",
    "🧲 Leads",
    "💼 Opportunities",
    "📑 Proposals",
    "✅ Approval",
    "🤖 Agents",
    "📧 Email",
    "🔗 LinkedIn",
    "⚙ CRM",
    "📚 Collateral"
])

with tabs[0]:
    render_dashboard()

with tabs[1]:
    render_leads()

with tabs[2]:
    render_opportunities()

with tabs[3]:
    render_proposals()

with tabs[4]:
    render_approval()

with tabs[5]:
    render_agents()

with tabs[6]:
    render_email()

with tabs[7]:
    render_linkedin()

with tabs[8]:
    render_crm()

with tabs[9]:
    render_collateral()
