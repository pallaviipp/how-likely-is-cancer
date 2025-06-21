# etl/load.py
import pandas as pd
import sqlite3
import os

def load_to_sqlite(df: pd.DataFrame, db_path="data/processed/breast_cancer_data.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("cancer_risk_table", conn, if_exists="replace", index=False)
    conn.close()

