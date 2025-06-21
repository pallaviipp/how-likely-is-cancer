import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime

# -------------------------------------------------------------------
# 1️⃣  Backend Communication
# -------------------------------------------------------------------
BACKEND_URL = "https://how-likely-is-cancer.onrender.com/score"

def fetch_risk_estimate(payload: dict) -> dict | None:
    try:
        res = requests.post(BACKEND_URL, json=payload, timeout=20)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Could not reach the backend: {e}")
        return None

# -------------------------------------------------------------------
# 2️⃣  Visualization Components
# -------------------------------------------------------------------
def _create_risk_gauge(risk_percent: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percent,
        number={'suffix': "%"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 5], 'color': "green"},
                {'range': [5, 12], 'color': "lightgreen"},
                {'range': [12, 20], 'color': "yellow"},
                {'range': [20, 30], 'color': "orange"},
                {'range': [30, 100], 'color': "red"}
            ]
        }
    ))
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=300)
    return fig

def _create_factor_breakdown(factors: dict) -> go.Figure:
    df = pd.DataFrame({
        'factor': list(factors.keys()),
        'multiplier': list(factors.values())
    }).sort_values('multiplier')
    fig = px.bar(df, x='multiplier', y='factor', orientation='h',
                 color='multiplier', color_continuous_scale='RdYlGn_r',
                 title="Risk Factor Multipliers")
    fig.update_layout(xaxis_title="Risk Multiplier", yaxis_title="Factor", coloraxis_showscale=False)
    return fig

def _create_age_comparison_chart(chart_data: dict) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    fig.add_trace(go.Scatter(
        x=chart_data['age_groups'],
        y=[x * 100 for x in chart_data['ethnicity_rates']],
        name="Your Ethnicity",
        line=dict(color="blue")
    ))
    fig.add_trace(go.Scatter(
        x=chart_data['age_groups'],
        y=[x * 100 for x in chart_data['average_rates']],
        name="Population Average",
        line=dict(color="gray", dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=[chart_data['user_age']],
        y=[chart_data['user_risk'] * 100],
        name="You",
        mode='markers',
        marker=dict(size=12, color="red")
    ))
    fig.update_layout(title="Risk Comparison by Age", xaxis_title="Age", yaxis_title="Estimated Risk (%)")
    return fig

# -------------------------------------------------------------------
# 3️⃣  Main Rendering Function
# -------------------------------------------------------------------
def render_result(response: dict) -> None:
    if not response:
        st.warning("No data to display.")
        return

    st.set_page_config(layout="wide")
    st.markdown("## 📋 Personalized Breast Cancer Risk Assessment")

    risk_percent = response.get("risk_percentage", 0)
    risk_label = response.get("risk_estimate", "Unknown")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.plotly_chart(_create_risk_gauge(risk_percent), use_container_width=True)

    with col2:
        st.metric("Risk Level", risk_label)
        st.metric("Risk %", f"{risk_percent:.1f}%")
        if 'timestamp' in response:
            st.caption(f"Generated: {response['timestamp']}")

    with col3:
        recs = response.get("recommendations", [])
        st.markdown("#### Recommendations")
        if recs:
            for r in recs[:2]:
                st.markdown(f"- {r}")
            if len(recs) > 2:
                with st.expander("See more"):
                    for r in recs[2:]:
                        st.markdown(f"- {r}")
        else:
            st.info("No specific recommendations provided.")

    st.divider()

    with st.expander("📊 Risk Details", expanded=True):
        tab1, tab2, tab3 = st.tabs(["Breakdown", "Age Comparison", "Raw Data"])

        with tab1:
            if 'factor_breakdown' in response:
                st.plotly_chart(_create_factor_breakdown(response['factor_breakdown']), use_container_width=True)
            else:
                st.warning("No factor data")

        with tab2:
            if 'chart_data' in response:
                st.plotly_chart(_create_age_comparison_chart(response['chart_data']), use_container_width=True)
            else:
                st.warning("No chart data")

        with tab3:
            st.json(response, expanded=False)

    if "contextual_reasons" in response:
        with st.expander("ℹ️ Why this result?"):
            for reason in response["contextual_reasons"]:
                st.markdown(f"- {reason}")

    st.divider()
    st.warning(
        "**Disclaimer**: This is a data-backed estimate, not a diagnosis. Always consult medical professionals."
    )

    if st.button("📥 Download Report"):
        st.info("PDF report generation coming soon!")

# -------------------------------------------------------------------
# 4️⃣  Example Usage (optional local test)
# -------------------------------------------------------------------
if __name__ == "__main__":
    render_result({
        "risk_estimate": "Moderate",
        "risk_percentage": 17.8,
        "timestamp": datetime.now().isoformat(),
        "factor_breakdown": {
            "baseline": 0.012,
            "genetic": 1.8,
            "hormonal": 1.25,
            "lifestyle": 1.15,
            "breast_health": 1.2
        },
        "recommendations": [
            "Consider more frequent screening.",
            "Reduce alcohol intake.",
            "Maintain regular exercise."
        ],
        "contextual_reasons": [
            "You have 1 close relative with breast cancer",
            "Hormonal history increases risk",
            "Your baseline demographic risk is 1.2%"
        ],
        "chart_data": {
            "age_groups": list(range(20, 80)),
            "ethnicity_rates": [0.01 + 0.0005 * i for i in range(60)],
            "average_rates": [0.008 + 0.0004 * i for i in range(60)],
            "user_age": 45,
            "user_risk": 0.0178
        },
        "user_summary": {
            "age": 45,
            "ethnicity": "White",
            "relatives_with_cancer": 1,
            "anxiety_level": "High"
        }
    })
