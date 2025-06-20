import sqlite3
from datetime import datetime

DB_NAME = "submissions.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
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
                full_data TEXT
            )
        ''')
        conn.commit()
        
def get_all_submissions():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM risk_submissions ORDER BY timestamp DESC")
        rows = cursor.fetchall()

        # Return as list of dicts
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]


def save_submission(data, risk_estimate):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO risk_submissions (
                timestamp, age, gender, symptom, location,
                relatives_with_cancer, brca_known, anxiety_level,
                risk_estimate, full_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.utcnow().isoformat(),
            data.get("age"),
            data.get("gender"),
            data.get("symptom"),
            data.get("location"),
            data.get("relatives_with_cancer"),
            data.get("brca_known"),
            data.get("anxiety_level"),
            risk_estimate,
            str(data)
        ))
        conn.commit()

