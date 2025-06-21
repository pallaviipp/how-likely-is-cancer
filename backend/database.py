import sqlite3
import json
from datetime import datetime

DB_PATH = "backend/data/processed/breast_cancer_risk.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                age INTEGER,
                gender TEXT,
                symptom TEXT,
                location TEXT,
                relatives_with_cancer INTEGER,
                brca_known TEXT,
                anxiety_level TEXT,
                risk_estimate TEXT,
                risk_percentage REAL,
                recommendations TEXT,
                contextual_reasons TEXT,
                raw_factors TEXT,
                user_summary TEXT
            )
        ''')
        conn.commit()

def get_all_submissions():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM risk_submissions ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

def save_submission(data: dict, result: dict):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO risk_submissions (
                symptom, age, gender, location,
                relatives_with_cancer, brca_known, anxiety_level,
                risk_estimate, risk_percentage,
                recommendations, contextual_reasons,
                raw_factors, user_summary, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get("symptom"),
            data.get("age"),
            data.get("gender"),
            data.get("location"),
            data.get("relatives_with_cancer"),
            data.get("brca_known"),
            data.get("anxiety_level"),
            result.get("risk_estimate"),
            result.get("risk_percentage"),
            json.dumps(result.get("recommendations", [])),
            json.dumps(result.get("contextual_reasons", [])),
            json.dumps(result.get("factor_breakdown", {})),
            json.dumps(result.get("user_summary", {})),
            result.get("timestamp")
        ))
        conn.commit()
