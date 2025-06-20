import streamlit as st
import pandas as pd
import plotly.express as px

def display_result(response):
    st.markdown("##  Here's What the Data Says")
    st.success(f"Based on your inputs, your estimated risk appears to be: **{response['risk_estimate']}**")

    st.markdown("###  Some context")
    st.markdown(f"> _{response['context']}_")

    st.divider()

    st.markdown("###  Why this matters")
    st.write("Breast cancer risk varies depending on genetics, age, hormones, and environment. The data helps us understand population trends — but it doesn't define your story. This is not a diagnosis.")

    if "chart_data" in response:
        st.markdown("### 📊 Age-wise incidence comparison")
        df = pd.DataFrame(response["chart_data"])
        fig = px.bar(
            df,
            x="age_group",
            y="incidence_rate",
            labels={"incidence_rate": "Cases per 100,000"},
            title="Estimated Incidence Rate by Age Group",
            color_discrete_sequence=["#ff7f0e"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info("If something doesn't feel right, it's always okay to talk to a doctor — even just to calm your mind. You deserve peace of mind.")

