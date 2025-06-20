import streamlit as st

def user_input_form():
    st.header("How Likely Is It Really?")
    st.subheader("Answer a few questions to put things into data-backed context")

    symptom = st.text_input("What symptom are you worried about?", placeholder="e.g. breast lump")
    age = st.slider("Your age", 10, 100, 22)
    gender = st.selectbox("Your gender identity", ["Female", "Male", "Other"])
    location = st.text_input("Where are you located?", placeholder="e.g. Nepal")

    st.markdown("### Your Body & History")
    age_menarche = st.slider("At what age did you get your first period?", 8, 20, 12)
    age_thelarche = st.slider("When did your breasts start developing?", 8, 20, 12)

    relatives_with_cancer = st.number_input(
        "How many close blood relatives (mother, sister, daughter) have had breast cancer?",
        min_value=0, max_value=10, value=0
    )

    hormonal_use = st.selectbox(
        "Have you used hormonal birth control or hormone therapy for more than 5 years?",
        ["No", "Yes", "Not sure"]
    )

    pregnancy_history = st.selectbox("Have you ever been pregnant?", ["No", "Yes", "Prefer not to say"])

    breast_density = st.selectbox(
        "Has a doctor ever told you that you have dense breast tissue?",
        ["No", "Yes", "Don't know"]
    )

    benign_lumps = st.selectbox("Have you had a benign (non-cancerous) lump diagnosed before?", ["No", "Yes"])

    st.markdown("###  Lifestyle")

    smoking = st.selectbox("Do you smoke or vape regularly?", ["No", "Yes"])
    alcohol = st.selectbox("Do you consume alcohol weekly?", ["No", "Yes"])

    if st.button("What are my odds?"):
        return {
            "symptom": symptom.strip(),
            "age": age,
            "gender": gender,
            "location": location.strip(),
            "age_menarche": age_menarche,
            "age_thelarche": age_thelarche,
            "relatives_with_cancer": relatives_with_cancer,
            "hormonal_use": hormonal_use,
            "pregnancy_history": pregnancy_history,
            "breast_density": breast_density,
            "benign_lumps": benign_lumps,
            "smoking": smoking,
            "alcohol": alcohol,
        }

    return None

