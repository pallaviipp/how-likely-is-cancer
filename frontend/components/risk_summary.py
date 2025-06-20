import streamlit as st
import pandas as pd
import plotly.express as px

def display_result(response):
    st.markdown("## 📋 Your Personalized Risk Insight")

    st.success(f"**Estimated Risk Level:** {response['risk_estimate']}", icon="🔍")

    if response["contextual_reasons"]:
        st.markdown("### 🧠 Why this result?")
        for reason in response["contextual_reasons"]:
            st.markdown(f"- {reason}")

    st.divider()

    st.markdown("### 📊 Context: Breast Cancer by Age Group")
    df = pd.DataFrame(response["chart_data"])
    fig = px.bar(
        df,
        x="age_group",
        y="incidence_rate",
        labels={"age_group": "Age Group", "incidence_rate": "Cases per 100,000"},
        title="Estimated Incidence by Age Group (World Data)",
        color_discrete_sequence=["#ff7f0e"]
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🤍 Reminder")
    st.info(
        "This tool is a contextual guide, not a diagnosis. "
        "It uses general data patterns to ease anxiety and encourage informed action. "
        "You are always encouraged to speak to a healthcare provider if something feels wrong."
    )

    st.caption("Built with love, logic, and compassion.")
