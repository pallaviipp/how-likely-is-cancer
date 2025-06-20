import streamlit as st
import pycountry

def user_input_form():
    st.header("Is it serious or are you anxious?")
    st.subheader("Answer a few questions to put your concern into data-backed context")

    symptom = st.text_input("What symptom are you worried about?", placeholder="e.g. breast lump")
        # -------------------------  Section 2: Context -------------------------
    age = st.slider(" Your current age", 10, 100, 22)
    gender = st.selectbox(" Your gender identity", ["Female", "Male", "Other"])

    country_list = sorted([country.name for country in pycountry.countries])
    location = st.selectbox(" Where are you currently located?", country_list, index=country_list.index("Nepal"))

    access_healthcare = st.selectbox(" Do you have access to basic healthcare services nearby?", ["Yes", "No", "Sometimes"])

    # -------------------------  Section 3: Hormonal Life Events -------------------------
    st.markdown("###  Hormonal History")
    age_menarche = st.slider("At what age did your periods start?", 8, 20, 12)
    age_thelarche = st.slider("At what age did your breasts begin developing?", 8, 20, 12)

    menopause = st.selectbox("Have you gone through menopause?", ["No", "Yes", "Not sure"])
    age_menopause = None
    if menopause == "Yes":
        age_menopause = st.slider("At what age did menopause begin?", 35, 60, 48)

    pregnancy = st.selectbox("Have you ever had a full-term pregnancy?", ["No", "Yes", "Prefer not to say"])
    pregnancy_age = None
    if pregnancy == "Yes":
        pregnancy_age = st.slider("How old were you at your first full-term pregnancy?", 13, 50, 24)

    breastfeeding = st.selectbox("Have you breastfed any children?", ["No", "Yes", "Prefer not to say"])
    pcos = st.selectbox("Have you been diagnosed with PCOS or irregular cycles?", ["No", "Yes", "Not sure"])

    hormonal_use = st.selectbox(
        "Have you taken hormonal birth control or HRT for more than 5 years?",
        ["No", "Yes", "Not sure"]
    )

    # -------------------------  Section 4: Family & Genetics -------------------------
    st.markdown("### 🧬 Family & Genetics")
    relatives_with_cancer = st.number_input(
        "How many close blood relatives (mother, sister, daughter) have had breast cancer?",
        min_value=0, max_value=10, value=0
    )

    brca_known = st.selectbox("Have you tested positive for a BRCA mutation?", ["No", "Yes", "Not tested / Not sure"])
    ethnicity = st.selectbox(
        "Which ethnic group do you most closely identify with?",
        ["Asian", "White", "Black", "Latina", "Mixed", "Middle Eastern", "Jewish (Ashkenazi)", "Other", "Prefer not to say"]
    )

    # -------------------------  Section 5: Prior Screening -------------------------
    st.markdown("### 🩻 Prior Breast Screenings")
    had_mammo = st.selectbox("Have you ever had a mammogram or breast ultrasound?", ["No", "Yes"])
    breast_density = st.selectbox("Have you been told you have dense breasts?", ["No", "Yes", "Don't know"])
    benign_lumps = st.selectbox("Have you ever been diagnosed with a benign breast lump?", ["No", "Yes"])

    # -------------------------  Section 6: Lifestyle -------------------------
    st.markdown("### 🌿 Lifestyle")
    smoking = st.selectbox("Do you smoke or vape regularly?", ["No", "Yes"])
    alcohol = st.selectbox("Do you consume alcohol weekly or more?", ["No", "Yes"])
    exercise = st.selectbox("How often do you engage in physical activity?", ["Rarely", "1–2x/week", "3–5x/week", "Daily"])
    anxiety_level = st.selectbox("How anxious are you feeling about your symptom?", ["Mild", "Manageable", "High", "Debilitating"])

    # -------------------------  Submit -------------------------
    if st.button("What are the odds?"):


        return {
            "symptom": symptom.strip(),
            "age": age,
            "gender": gender,
            "location": location,
            "access_healthcare": access_healthcare,
            "age_menarche": age_menarche,
            "age_thelarche": age_thelarche,
            "menopause": menopause,
            "age_menopause": age_menopause,
            "pregnancy": pregnancy,
            "pregnancy_age": pregnancy_age,
            "breastfeeding": breastfeeding,
            "pcos": pcos,
            "hormonal_use": hormonal_use,
            "relatives_with_cancer": relatives_with_cancer,
            "brca_known": brca_known,
            "ethnicity": ethnicity,
            "had_mammo": had_mammo,
            "breast_density": breast_density,
            "benign_lumps": benign_lumps,
            "smoking": smoking,
            "alcohol": alcohol,
            "exercise": exercise,
            "anxiety_level": anxiety_level
        }

    return None
