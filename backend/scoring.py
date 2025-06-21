import sqlite3
import pandas as pd
from typing import Dict, Any
import numpy as np
from backend.models import RiskForm

# Database configuration
DB_PATH = "backend/data/processed/breast_cancer_risk.db"

def get_baseline_risk(age: int, ethnicity: str) -> float:
    """
    Get baseline risk from the risk_baseline table.
    
    Args:
        age: Patient's age
        ethnicity: Patient's ethnicity
        
    Returns:
        float: Baseline risk rate (cases per record)
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Find closest age group (since we may not have exact age matches)
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
            
            # Fallback to overall average if no match found
            query = "SELECT AVG(risk_rate) as avg_risk FROM risk_baseline"
            result = pd.read_sql_query(query, conn)
            return result.iloc[0]['avg_risk'] or 0.01  # Default to 1% if no data
            
    except Exception as e:
        print(f"Error accessing baseline risk: {e}")
        return 0.01  # Fallback baseline risk


def calculate_risk_adjustment_factors(user_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate multiplicative risk adjustment factors based on user profile.
    
    Returns:
        Dict with factor names and their values
    """
    factors = {
        'baseline': 1.0,  # Will be replaced with actual baseline
        'genetic': 1.0,
        'hormonal': 1.0,
        'lifestyle': 1.0,
        'breast_health': 1.0
    }
    
    # ---------------------------- Genetic & Family History ----------------------------
    if user_data["relatives_with_cancer"] >= 2:
        factors['genetic'] *= 3.0
    elif user_data["relatives_with_cancer"] == 1:
        factors['genetic'] *= 1.8
    
    if user_data["brca_known"] == "Yes":
        factors['genetic'] *= 4.0
    elif user_data["brca_known"] == "Not tested / Not sure":
        factors['genetic'] *= 1.2  # Slight increase for uncertainty

    # ---------------------------- Hormonal History ----------------------------
    if user_data["age_menarche"] <= 11:
        factors['hormonal'] *= 1.3
    
    if user_data["menopause"] == "Yes" and user_data.get("age_menopause", 0) > 55:
        factors['hormonal'] *= 1.4
    elif user_data["menopause"] == "No" and user_data["age"] > 55:
        factors['hormonal'] *= 1.2  # Late menopause implied by age

    if user_data["hormonal_use"] == "Yes":
        factors['hormonal'] *= 1.25

    if user_data["pregnancy"] == "Yes" and user_data.get("pregnancy_age", 0) >= 30:
        factors['hormonal'] *= 1.15
    elif user_data["pregnancy"] == "No":
        factors['hormonal'] *= 1.1

    if user_data["breastfeeding"] == "Yes":
        factors['hormonal'] *= 0.9  # Protective factor

    if user_data["pcos"] == "Yes":
        factors['hormonal'] *= 1.2

    # ---------------------------- Lifestyle Factors ----------------------------
    if user_data["smoking"] == "Yes":
        factors['lifestyle'] *= 1.3
    
    if user_data["alcohol"] == "Yes":
        factors['lifestyle'] *= 1.2

    if user_data["exercise"] in ["Rarely", "1–2x/week"]:
        factors['lifestyle'] *= 1.15
    elif user_data["exercise"] == "Daily":
        factors['lifestyle'] *= 0.9  # Protective factor

    # ---------------------------- Breast Health ----------------------------
    if user_data["breast_density"] == "Yes":
        factors['breast_health'] *= 1.4
    
    if user_data["benign_lumps"] == "Yes":
        factors['breast_health'] *= 1.3

    if user_data["had_mammo"] == "Yes":
        factors['breast_health'] *= 0.8  # Screening is protective
    
    return factors


def calculate_risk_score(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive risk estimation combining baseline rates and adjustment factors.
    
    Returns:
        Dict with risk estimate, reasons, and metadata
    """
    # Get baseline risk for this demographic
    baseline_risk = get_baseline_risk(user_data["age"], user_data["ethnicity"])
    
    # Calculate all adjustment factors
    factors = calculate_risk_adjustment_factors(user_data)
    factors['baseline'] = baseline_risk
    
    # Calculate final risk estimate (baseline * product of factors)
    adjusted_risk = baseline_risk * np.prod(list(factors.values()))
    
    # Convert to percentage (0-100 scale)
    risk_percentage = min(100, max(0, adjusted_risk * 100))
    
    # Generate contextual reasons
    reasons = generate_contextual_reasons(factors, baseline_risk)
    
    # Determine risk level category
    risk_level = categorize_risk_level(risk_percentage)
    
    return {
        "risk_estimate": risk_level,
        "risk_percentage": round(risk_percentage, 1),
        "contextual_reasons": reasons,
        "factor_breakdown": {k: round(v, 2) for k, v in factors.items()},
        "chart_data": get_age_ethnicity_comparison_data(user_data["age"], user_data["ethnicity"]),
        "user_summary": user_data
    }


def generate_contextual_reasons(factors: Dict[str, float], baseline: float) -> List[str]:
    """Generate human-readable explanations for the risk factors"""
    reasons = []
    
    # Baseline explanation
    reasons.append(
        f"Baseline risk for your demographic: {baseline*100:.1f}%"
    )
    
    # Genetic factors
    if factors['genetic'] > 1.5:
        if factors['genetic'] >= 3.0:
            reasons.append("Strong family history significantly increases risk")
        else:
            reasons.append("Family history moderately increases risk")
    
    # Hormonal factors
    hormonal_factors = [
        ("Early menstruation (before 11)", factors['hormonal'] >= 1.3),
        ("Late/no menopause", factors['hormonal'] >= 1.2 and factors['hormonal'] < 1.3),
        ("Hormone use", factors['hormonal'] >= 1.25),
        ("Late/no pregnancies", factors['hormonal'] >= 1.1)
    ]
    
    for desc, condition in hormonal_factors:
        if condition:
            reasons.append(f"{desc} increases hormonal risk factors")
    
    # Lifestyle factors
    if factors['lifestyle'] >= 1.2:
        reasons.append("Lifestyle choices (smoking/alcohol/inactivity) increase risk")
    elif factors['lifestyle'] <= 0.9:
        reasons.append("Healthy lifestyle choices provide some protection")
    
    # Breast health factors
    if factors['breast_health'] >= 1.3:
        reasons.append("Breast health history indicates elevated risk")
    
    # Anxiety level message
    if "anxiety_level" in factors.get("user_summary", {}):
        if factors["user_summary"]["anxiety_level"] in ["High", "Debilitating"]:
            reasons.append(
                "You're feeling very anxious - please consult a healthcare professional for evaluation"
            )
    
    return reasons


def categorize_risk_level(risk_percentage: float) -> str:
    """Convert numerical risk to categorical level"""
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
    """Get comparison data for visualization"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Get data for this ethnicity
            query = """
                SELECT age, risk_rate 
                FROM risk_baseline
                WHERE ethnicity = ?
                ORDER BY age
            """
            ethnic_data = pd.read_sql_query(query, conn, params=(ethnicity,))
            
            # Get average across all ethnicities
            query = """
                SELECT age, AVG(risk_rate) as risk_rate
                FROM risk_baseline
                GROUP BY age
                ORDER BY age
            """
            avg_data = pd.read_sql_query(query, conn)
            
            # Get user's specific age/ethnicity risk
            user_risk = get_baseline_risk(age, ethnicity)
            
            return {
                "age_groups": ethnic_data['age'].tolist(),
                "ethnicity_rates": ethnic_data['risk_rate'].tolist(),
                "average_rates": avg_data['risk_rate'].tolist(),
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
            "user_risk": 0
        }
