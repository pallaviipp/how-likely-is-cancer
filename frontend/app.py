import streamlit as st
from components.input_form import user_input_form
from components.risk_summary import display_result

def mock_backend_logic(user_data):
    """
    Temporary backend logic for breast cancer risk estimation.
    Replace this with actual ETL + ML risk scoring pipeline later.
    """
    # Simplified mock logic for demo purposes
    risk_level = "Low"
    reasons = []

    if user_data["relatives_with_cancer"] >= 2 or user_data["brca_known"] == "Yes":
        risk_level = "High"
        reasons.append("You reported a strong family history of breast cancer.")
    elif user_data["menopause"] == "Yes" and user_data["age_menopause"] and user_data["age_menopause"] > 55:
        risk_level = "Moderate"
        reasons.append("Later menopause increases lifetime estrogen exposure.")
    elif user_data["age"] > 45:
        risk_level = "Moderate"
        reasons.append("Breast cancer risk increases with age.")

    if user_data["anxiety_level"] in ["High", "Debilitating"]:
        reasons.append("Your anxiety level is high. Please remember, this tool is supportive, not diagnostic.")

    return {
        "risk_estimate": risk_level,
        "contextual_reasons": reasons,
        "chart_data": {
            "age_group": ["20–24", "25–29", "30–34", "35–39", "40–44", "45–49", "50+"],
            "incidence_rate": [2.1, 5.7, 11.2, 18.4, 32.5, 48.1, 69.2]
        },
        "user_summary": user_data
    }

def main():
    st.set_page_config(
        page_title="How Likely Is It Really?",
        layout="centered",
        page_icon="🩺"
    )

    st.title(" How Likely Is It Really?")
    st.caption("A data-informed companion for moments of health anxiety.")

    user_input = user_input_form()
    if user_input:
        result = mock_backend_logic(user_input)
        display_result(result)

if __name__ == "__main__":
    main()


