import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# -------------------------------------------------------------------
# 1️⃣  Call the backend and return the parsed JSON (or None on error)
# -------------------------------------------------------------------
BACKEND_URL = "https://how-likely-is-cancer.onrender.com/score"

def fetch_risk_estimate(payload: dict) -> dict | None:
    """Send POST request to backend and return JSON dict on success."""
    try:
        res = requests.post(BACKEND_URL, json=payload, timeout=20)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Could not reach the backend: {e}")
        return None

# -------------------------------------------------------------------
# 2️⃣  Render the result in Streamlit
# -------------------------------------------------------------------
def render_result(response: dict) -> None:
    """Pretty‑print the response returned by fetch_risk_estimate()."""
    if not response:
        st.warning("No data to display.")
        return

    # ----- Safety: be sure keys exist -----
    if "risk_estimate" not in response:
        st.error("Backend response missing ‘risk_estimate’. Full payload shown below ⤵︎")
        st.json(response)
        return

    # ----- Main card -----
    st.markdown("## 📋 Your Personalized Risk Insight")
    st.success(f"**Estimated Risk Level:** {response['risk_estimate']}", icon="🔍")

    # ----- Reasons -----
    if response.get("contextual_reasons"):
        st.markdown("### 🧠 Why this result?")
        for reason in response["contextual_reasons"]:
            st.markdown(f"- {reason}")

    st.divider()

    # ----- Chart -----
    if "chart_data" in response:
        df = pd.DataFrame(response["chart_data"])
        fig = px.bar(
            df,
            x="age_group",
            y="incidence_rate",
            labels={"age_group": "Age Group",
                    "incidence_rate": "Cases per 100 000"},
            title="Estimated Incidence by Age Group (Global)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # ----- Footer -----
    st.info(
        "This tool is a contextual guide, not a diagnosis. "
        "If something feels wrong, always consult a healthcare professional."
    )


