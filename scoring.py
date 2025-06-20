def calculate_risk_score(user_data):
    """
    Risk estimation logic (mock version).
    placeholder — eventually replace with statistical or ETL model.
    """

    # Default values
    risk_score = 0
    reasons = []

    # ---------------------------- Genetic & Family History ----------------------------
    if user_data["relatives_with_cancer"] >= 2:
        risk_score += 3
        reasons.append("Multiple first-degree relatives have had breast cancer.")
    
    if user_data["brca_known"] == "Yes":
        risk_score += 4
        reasons.append("Known BRCA mutation significantly increases risk.")

    # ---------------------------- Hormonal History ----------------------------
    if user_data["age_menarche"] <= 11:
        risk_score += 1
        reasons.append("Early onset of menstruation increases lifetime estrogen exposure.")

    if user_data["menopause"] == "Yes" and user_data["age_menopause"] and user_data["age_menopause"] > 55:
        risk_score += 1
        reasons.append("Late menopause increases lifetime hormonal exposure.")

    if user_data["hormonal_use"] == "Yes":
        risk_score += 1
        reasons.append("Long-term hormonal therapy or birth control use may influence risk.")

    if user_data["pregnancy"] == "Yes" and user_data["pregnancy_age"] and user_data["pregnancy_age"] >= 30:
        risk_score += 1
        reasons.append("Late first pregnancy (after 30) is a mild risk enhancer.")
    elif user_data["pregnancy"] == "No":
        risk_score += 1
        reasons.append("Never being pregnant slightly increases risk.")

    if user_data["breastfeeding"] == "Yes":
        risk_score -= 1
        reasons.append("Breastfeeding offers slight protection.")

    # ---------------------------- Lifestyle Factors ----------------------------
    if user_data["smoking"] == "Yes":
        risk_score += 1
        reasons.append("Smoking is a general health and cancer risk factor.")

    if user_data["alcohol"] == "Yes":
        risk_score += 1
        reasons.append("Regular alcohol consumption can increase breast cancer risk.")

    if user_data["exercise"] in ["Rarely", "1–2x/week"]:
        risk_score += 1
        reasons.append("Low physical activity is a slight risk factor.")

    # ---------------------------- Breast History ----------------------------
    if user_data["breast_density"] == "Yes":
        risk_score += 1
        reasons.append("Dense breast tissue makes detection harder and is mildly associated with risk.")

    if user_data["benign_lumps"] == "Yes":
        risk_score += 1
        reasons.append("History of benign lumps may slightly increase risk.")

    # ---------------------------- Age-Based Risk ----------------------------
    if user_data["age"] >= 50:
        risk_score += 2
        reasons.append("Your age group naturally has higher breast cancer incidence.")

    # ---------------------------- Emotional Context ----------------------------
    if user_data["anxiety_level"] in ["High", "Debilitating"]:
        reasons.append("You’re feeling very anxious — this tool is designed to guide and support, not diagnose.")

    # ---------------------------- Risk Level Decision ----------------------------
    if risk_score >= 6:
        risk_level = "Moderate to High"
    elif 3 <= risk_score < 6:
        risk_level = "Slightly Elevated"
    else:
        risk_level = "Low"

    return {
        "risk_estimate": risk_level,
        "contextual_reasons": reasons,
        "chart_data": {
            "age_group": ["20–24", "25–29", "30–34", "35–39", "40–44", "45–49", "50+"],
            "incidence_rate": [2.1, 5.7, 11.2, 18.4, 32.5, 48.1, 69.2]
        },
        "user_summary": user_data
    }

