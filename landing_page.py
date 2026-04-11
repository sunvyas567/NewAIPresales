import streamlit as st


def show_landing_page():

    #st.set_page_config(layout="wide")

    st.title("🚀 AI Assisted Agentic Presales" )
    st.subheader("AI-Powered Presales Automation Platform")

    st.write(
        """
        Convert **Leads → Opportunities → Proposals** faster using automation and AI.
        """
    )

    col1, col2 = st.columns([1,1])

    with col1:

        st.markdown("### What Agentic Presales Does")

        st.write("• Lead Processing & outreach automation")
        st.write("• Campaign management (LinkedIn, Email)")
        st.write("• Opportunity tracking")
        st.write("• CRM synchronization (Odoo, Salesforce)")
        st.write("• AI proposal generation ( Proposal & SoW drafting)")

    with col2:

       # st.image(
       #     "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
       #     use_column_width=True
       # )
        st.markdown("### Workflow")

        st.write(
            """
            Lead Processing  
            ↓  
            Campaign Outreach
            (LinkedIn, Email)  
            ↓  
            Opportunity Creation  
            ↓  
            CRM Sync
            (Odoo, Salesforce)  
            ↓  
            Proposal Generation
            (PPT.PDF)  
            ↓  
            SoW Generation
            (PDF, Word)  
            ↓  
            Dashboard & Analytics
            """
        )



    st.markdown("---")
    col1, col2 = st.columns([1,1])

    with col1:
        if st.button("🎯 Try Demo"):
            st.session_state.mode = "demo"
            st.rerun()
    with col2:
        if st.button("🔑 Enter Application"):
            st.session_state.mode = "app"
            st.rerun()

    st.markdown("---")

    st.markdown("### Built for Sales & Presales Teams")

    col1, col2, col3 = st.columns(3)

    col1.metric("Faster Proposals", "10x")
    col2.metric("Campaign Automation", "Yes")
    col3.metric("AI Assistance", "Optional")