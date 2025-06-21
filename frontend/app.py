import streamlit as st
from components.input_form import user_input_form
from components.risk_summary import fetch_risk_estimate, render_result

API_URL = "https://how-likely-is-cancer.onrender.com/score"

def call_backend_api(user_data):
    """Wrapper for backend API call with better error handling"""
    try:
        response = requests.post(API_URL,
                              json=user_data,
                              timeout=60,
                              headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="How Likely Is It Really?",
        layout="centered",
        page_icon="🩺"
    )

    st.title("How Likely Is Breast Cancer Really?")
    st.caption("A data-informed companion for moments of health anxiety.")

    user_input = user_input_form()
    
    if user_input:
        with st.spinner("Calculating your risk assessment..."):
            response = call_backend_api(user_input)
            if response:
                render_result(response)
            else:
                st.error("Failed to get results. Please try again later.")

if __name__ == "__main__":
    import requests  # Moved here to avoid shadowing the imported requests
    main()
