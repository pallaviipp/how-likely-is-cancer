import sqlite3
import pandas as pd
import os

DB_PATH = "backend/data/processed/breast_cancer_risk.db"

def build_risk_baseline():
    conn = sqlite3.connect("backend/data/processed/breast_cancer_risk.db")

    # Load the risk_factors table
    df = pd.read_sql_query("SELECT age, ethnicity, cases FROM risk_factors", conn)

    # Drop rows with missing values
    df = df.dropna(subset=["age", "ethnicity", "cases"])

    # Group by age and ethnicity
    baseline = (
        df.groupby(["age", "ethnicity"])
        .agg(
            total_cases=("cases", "sum"),
            total_records=("cases", "count")
        )
        .reset_index()
    )

    # Calculate risk rate
    baseline["risk_rate"] = baseline["total_cases"] / baseline["total_records"]

    # Save to SQLite table
    baseline.to_sql("risk_baseline", conn, if_exists="replace", index=False)

    print("Risk baseline table created successfully.")

    conn.close()

if __name__ == "__main__":
    build_risk_baseline()

