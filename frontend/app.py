import streamlit as st
from components.input_form import user_input_form
from components.risk_summary import display_result

def mock_backend_logic(user_data):
    # This is where your future ML/ETL backend will hook in
    risk = "Low"
    context = (
        f"Statistically, among people with your profile, the likelihood of breast cancer at your age is quite low. "
        f"Most similar cases do not lead to cancer. Early menarche and family history do contribute slightly, "
        f"but the numbers remain reassuringly low for someone your age."
    )
    return {
        **user_data,
        "risk_estimate": risk,
        "context": context,
        "chart_data": {
            "age_group": ["20-24", "25-29", "30-34", "35-39"],
            "incidence_rate": [2.1, 5.7, 11.2, 18.4]
        }
    }

def main():
    st.set_page_config(
        page_title="How Likely Is It Really?",
        layout="centered",
        page_icon="🩺"
    )
    st.title("How Likely Is It Really?")
    st.caption("A data-informed companion for moments of health anxiety.")

    user_input = user_input_form()
    if user_input:
        result = mock_backend_logic(user_input)
        display_result(result)

if __name__ == "__main__":
    main()

