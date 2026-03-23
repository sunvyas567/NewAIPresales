import streamlit as st


def show_landing_page():

    #st.set_page_config(layout="wide")

    st.title("🚀 AgenticAI")
    st.subheader("AI-Powered Presales Automation Platform")

    st.write(
        """
        Convert **Leads → Opportunities → Proposals** faster using automation and AI.
        """
    )

    col1, col2 = st.columns([1,1])

    with col1:

        st.markdown("### What AgenticAI Does")

        st.write("• Lead outreach automation")
        st.write("• Campaign management")
        st.write("• Opportunity tracking")
        st.write("• CRM synchronization")
        st.write("• AI proposal generation")

    with col2:

       # st.image(
       #     "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
       #     use_column_width=True
       # )
        st.markdown("### Workflow")

        st.write(
            """
            Lead  
            ↓  
            Campaign Outreach  
            ↓  
            Opportunity Creation  
            ↓  
            CRM Sync  
            ↓  
            Proposal Generation
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

    st.markdown("### Built for Presales Teams")

    col1, col2, col3 = st.columns(3)

    col1.metric("Faster Proposals", "10x")
    col2.metric("Campaign Automation", "Yes")
    col3.metric("AI Assistance", "Optional")