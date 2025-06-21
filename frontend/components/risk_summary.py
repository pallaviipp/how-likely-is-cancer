import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime
from typing import Dict, Optional, List

# Configuration
RISK_COLORS = {
    "Very Low": "#2ecc71",
    "Low": "#3498db",
    "Moderate": "#f39c12",
    "High": "#e74c3c",
    "Very High": "#c0392b"
}

def fetch_risk_estimate(payload: dict) -> Optional[Dict]:
    """Fetch risk estimate from backend API"""
    try:
        response = requests.post(
            "https://how-likely-is-cancer.onrender.com/score",
            json=payload,
            timeout=20
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Could not reach the backend: {e}")
        return None

def create_risk_gauge(risk_percent: float, risk_level: str) -> go.Figure:
    """Create interactive risk gauge visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_percent,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Risk Level: {risk_level}"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': RISK_COLORS.get(risk_level, "gray")},
            'steps': [
                {'range': [0, 5], 'color': "#2ecc71"},
                {'range': [5, 12], 'color': "#3498db"},
                {'range': [12, 20], 'color': "#f1c40f"},
                {'range': [20, 30], 'color': "#e67e22"},
                {'range': [30, 100], 'color': "#e74c3c"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': risk_percent
            }
        }
    ))
    fig.update_layout(
        height=300,
        margin=dict(t=50, b=10, l=20, r=20)
    )
    return fig

def create_factor_barchart(factors: Dict[str, float]) -> go.Figure:
    """Create horizontal bar chart of risk factors"""
    df = pd.DataFrame({
        'Factor': factors.keys(),
        'Impact': factors.values()
    }).sort_values('Impact', ascending=True)
    
    fig = px.bar(
        df,
        x='Impact',
        y='Factor',
        orientation='h',
        color='Impact',
        color_continuous_scale='RdYlGn_r',
        title="Risk Factor Contributions"
    )
    fig.update_layout(
        xaxis_title="Risk Multiplier",
        yaxis_title="",
        coloraxis_showscale=False
    )
    return fig

def render_result(response: Dict) -> None:
    """Main rendering function with all original visualizations"""
    if not response:
        st.warning("No data to display.")
        return

    # Set up page layout
    st.set_page_config(layout="wide")
    st.markdown("## 📋 Your Personalized Risk Assessment")

    # Extract key metrics
    risk_percent = response.get("risk_percentage", 0)
    risk_level = response.get("risk_estimate", "Unknown")
    factors = response.get("factor_breakdown", {})
    recommendations = response.get("recommendations", [])
    chart_data = response.get("chart_data", {})

    # Main dashboard layout
    col1, col2, col3 = st.columns([3, 1, 2])

    with col1:
        st.plotly_chart(
            create_risk_gauge(risk_percent, risk_level),
            use_container_width=True
        )

    with col2:
        st.metric("Risk Category", risk_level)
        st.metric("Risk Score", f"{risk_percent:.1f}%")
        if 'timestamp' in response:
            st.caption(f"Generated: {response['timestamp']}")

    with col3:
        st.markdown("#### Recommendations")
        if recommendations:
            for rec in recommendations[:3]:
                st.markdown(f"- {rec}")
            if len(recommendations) > 3:
                with st.expander("See all recommendations"):
                    for rec in recommendations[3:]:
                        st.markdown(f"- {rec}")
        else:
            st.info("No specific recommendations")

    st.divider()

    # Detailed analysis section
    with st.expander("🔍 Detailed Analysis", expanded=True):
        tab1, tab2 = st.tabs(["Risk Factors", "Population Comparison"])

        with tab1:
            if factors:
                st.plotly_chart(
                    create_factor_barchart(factors),
                    use_container_width=True
                )
                st.caption("Values >1 increase risk, <1 decrease risk")
            else:
                st.warning("No factor data available")

        with tab2:
            if chart_data and all(k in chart_data for k in ['age_groups', 'ethnicity_rates']):
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=chart_data['age_groups'],
                    y=[x*100 for x in chart_data['ethnicity_rates']],
                    name="Your Ethnicity Average"
                ))
                fig.add_trace(go.Scatter(
                    x=chart_data['age_groups'],
                    y=[x*100 for x in chart_data.get('average_rates', [])],
                    name="General Population",
                    line=dict(dash='dash')
                ))
                if 'user_age' in chart_data and 'user_risk' in chart_data:
                    fig.add_trace(go.Scatter(
                        x=[chart_data['user_age']],
                        y=[chart_data['user_risk']*100],
                        mode='markers',
                        name="Your Risk",
                        marker=dict(size=12, color='red')
                    ))
                fig.update_layout(
                    title="Risk Comparison by Age",
                    xaxis_title="Age",
                    yaxis_title="Risk Percentage (%)"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Incomplete comparison data")

    # Context and disclaimer
    if "contextual_reasons" in response:
        with st.expander("ℹ️ About These Results"):
            for reason in response["contextual_reasons"]:
                st.markdown(f"- {reason}")

    st.divider()
    st.warning("""
    **Disclaimer**: This tool provides estimates only, not a diagnosis. 
    Always consult with healthcare professionals for medical advice.
    Results are based on statistical models and may not reflect individual risk.
    """)

# Example test data
if __name__ == "__main__":
    test_data = {
        "risk_estimate": "Moderate",
        "risk_percentage": 18.7,
        "timestamp": datetime.now().isoformat(),
        "factor_breakdown": {
            "Age": 1.5,
            "Family History": 1.8,
            "Genetics": 1.0,
            "Hormonal": 1.2,
            "Lifestyle": 1.3
        },
        "recommendations": [
            "Consider annual mammograms",
            "Discuss family history with your doctor",
            "Limit alcohol consumption"
        ],
        "contextual_reasons": [
            "Age (45) increases risk compared to younger women",
            "Family history (1 relative) moderately increases risk",
            "No protective factors identified"
        ],
        "chart_data": {
            "age_groups": list(range(20, 80, 5)),
            "ethnicity_rates": [0.01 + 0.0005*i for i in range(12)],
            "average_rates": [0.008 + 0.0004*i for i in range(12)],
            "user_age": 45,
            "user_risk": 0.0187
        }
    }
    render_result(test_data)
