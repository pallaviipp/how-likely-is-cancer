import sqlite3
import pandas as pd
from typing import List, Dict, Any
import numpy as np
from backend.models import RiskForm

# Database path
DB_PATH = "backend/data/processed/breast_cancer_risk.db"

def get_baseline_risk(age: int, ethnicity: str) -> float:
    try:
        with sqlite3.connect("backend/data/processed/breast_cancer_risk.db") as conn:
            query = """
                SELECT risk_rate 
                FROM risk_baseline
                WHERE ethnicity = ? 
                ORDER BY ABS(age - ?)
                LIMIT 1
            """
            result = pd.read_sql_query(query, conn, params=(ethnicity, age))
            if not result.empty:
                return result.iloc[0]['risk_rate']

            # Fallback if no exact match
            query = "SELECT AVG(risk_rate) as avg_risk FROM risk_baseline"
            result = pd.read_sql_query(query, conn)
            return result.iloc[0]['avg_risk'] or 0.01
    except Exception as e:
        print(f"Error accessing baseline risk: {e}")
        return 0.01

def calculate_risk_adjustment_factors(user_data: Dict[str, Any]) -> Dict[str, float]:
    factors = {
        'genetic': 1.0,
        'hormonal': 1.0,
        'lifestyle': 1.0,
        'breast_health': 1.0
    }

    # Genetic factors
    if user_data["relatives_with_cancer"] >= 2:
        factors['genetic'] *= 3.0
    elif user_data["relatives_with_cancer"] == 1:
        factors['genetic'] *= 1.8

    if user_data["brca_known"] == "Yes":
        factors['genetic'] *= 4.0
    elif user_data["brca_known"] == "Not tested / Not sure":
        factors['genetic'] *= 1.2

    # Hormonal
    if user_data["age_menarche"] <= 11:
        factors['hormonal'] *= 1.3

    if user_data["menopause"] == "Yes" and user_data.get("age_menopause", 0) > 55:
        factors['hormonal'] *= 1.4
    elif user_data["menopause"] == "No" and user_data["age"] > 55:
        factors['hormonal'] *= 1.2

    if user_data["hormonal_use"] == "Yes":
        factors['hormonal'] *= 1.25

    if user_data["pregnancy"] == "Yes" and user_data.get("pregnancy_age", 0) >= 30:
        factors['hormonal'] *= 1.15
    elif user_data["pregnancy"] == "No":
        factors['hormonal'] *= 1.1

    if user_data["breastfeeding"] == "Yes":
        factors['hormonal'] *= 0.9

    if user_data["pcos"] == "Yes":
        factors['hormonal'] *= 1.2

    # Lifestyle
    if user_data["smoking"] == "Yes":
        factors['lifestyle'] *= 1.3
    if user_data["alcohol"] == "Yes":
        factors['lifestyle'] *= 1.2

    if user_data["exercise"] in ["Rarely", "1–2x/week"]:
        factors['lifestyle'] *= 1.15
    elif user_data["exercise"] == "Daily":
        factors['lifestyle'] *= 0.9

    # Breast Health
    if user_data["breast_density"] == "Yes":
        factors['breast_health'] *= 1.4
    if user_data["benign_lumps"] == "Yes":
        factors['breast_health'] *= 1.3
    if user_data["had_mammo"] == "Yes":
        factors['breast_health'] *= 0.8

    return factors

def generate_contextual_reasons(factors: Dict[str, float], baseline: float, user_data: Dict[str, Any]) -> List[str]:
    reasons = [f"Baseline risk for your demographic: {baseline*100:.1f}%"]

    if factors['genetic'] > 1.5:
        if factors['genetic'] >= 3.0:
            reasons.append("Strong family history significantly increases risk")
        else:
            reasons.append("Family history moderately increases risk")

    if factors['hormonal'] >= 1.2:
        reasons.append("Hormonal history indicates elevated lifetime exposure")

    if factors['lifestyle'] >= 1.2:
        reasons.append("Lifestyle factors (smoking/alcohol/inactivity) increase risk")
    elif factors['lifestyle'] <= 0.9:
        reasons.append("Healthy lifestyle choices provide some protection")

    if factors['breast_health'] >= 1.3:
        reasons.append("Breast health history (density, benign lumps) may increase risk")

    if user_data.get("anxiety_level") in ["High", "Debilitating"]:
        reasons.append("You're feeling very anxious – consider consulting a healthcare professional")

    return reasons

def generate_recommendations(factors: Dict[str, float], risk_level: str) -> List[str]:
    recs = []
    if risk_level in ["Moderate", "High", "Very High"]:
        recs.append("Consider regular breast exams and screenings")
        recs.append("Consult with a healthcare provider for a personalized plan")
    if factors['lifestyle'] > 1.1:
        recs.append("Improve lifestyle: quit smoking, reduce alcohol, and exercise")
    if factors['hormonal'] > 1.2:
        recs.append("Discuss hormone-related medical history with your doctor")
    return recs

def categorize_risk_level(risk_percentage: float) -> str:
    if risk_percentage < 5:
        return "Very Low"
    elif 5 <= risk_percentage < 10:
        return "Low"
    elif 10 <= risk_percentage < 20:
        return "Moderate"
    elif 20 <= risk_percentage < 30:
        return "High"
    else:
        return "Very High"

def get_age_ethnicity_comparison_data(age: int, ethnicity: str) -> Dict[str, Any]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT age, risk_rate 
                FROM risk_baseline
                WHERE ethnicity = ?
                ORDER BY age
            """
            ethnic_data = pd.read_sql_query(query, conn, params=(ethnicity,))
            
            query_avg = """
                SELECT age, AVG(risk_rate) as risk_rate
                FROM risk_baseline
                GROUP BY age
                ORDER BY age
            """
            avg_data = pd.read_sql_query(query_avg, conn)
            
            user_risk = get_baseline_risk(age, ethnicity)
            
            return {
                "age_groups": ethnic_data['age'].tolist() if not ethnic_data.empty else [],
                "ethnicity_rates": ethnic_data['risk_rate'].tolist() if not ethnic_data.empty else [],
                "average_rates": avg_data['risk_rate'].tolist() if not avg_data.empty else [],
                "user_age": age,
                "user_risk": user_risk
            }
    except Exception as e:
        print(f"Error getting comparison data: {e}")
        return {
            "age_groups": [],
            "ethnicity_rates": [],
            "average_rates": [],
            "user_age": age,
            "user_risk": 0.0
        }

def calculate_risk_score(user_data: Dict[str, Any]) -> Dict[str, Any]:
    baseline = get_baseline_risk(user_data["age"], user_data["ethnicity"])
    factors = calculate_risk_adjustment_factors(user_data)
    adjusted_risk = baseline * np.prod(list(factors.values()))
    risk_percentage = min(100, max(0, adjusted_risk * 100))
    risk_level = categorize_risk_level(risk_percentage)

    return {
        "risk_estimate": risk_level,
        "risk_percentage": round(risk_percentage, 1),
        "timestamp": pd.Timestamp.now().isoformat(),
        "factor_breakdown": {k: round(v, 2) for k, v in factors.items()},
        "recommendations": generate_recommendations(factors, risk_level),
        "contextual_reasons": generate_contextual_reasons(factors, baseline, user_data),
        "chart_data": get_age_ethnicity_comparison_data(user_data["age"], user_data["ethnicity"]),
        "user_summary": user_data
    }
