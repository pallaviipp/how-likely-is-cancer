import sqlite3
import os
import pandas as pd
from typing import Dict, Any
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_missing_columns(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> None:
    """
    Check and add missing columns in SQLite table based on DataFrame columns.
    """
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    existing_columns = {row[1] for row in cursor.fetchall()}

    for col in df.columns:
        if col not in existing_columns:
            # Infer SQLite type from pandas dtype (basic heuristic)
            if pd.api.types.is_integer_dtype(df[col]):
                col_type = 'INTEGER'
            elif pd.api.types.is_float_dtype(df[col]):
                col_type = 'REAL'
            else:
                col_type = 'TEXT'

            sql = f'ALTER TABLE {table_name} ADD COLUMN {col} {col_type};'
            conn.execute(sql)
            logger.info(f"Added missing column '{col}' with type '{col_type}' to {table_name}")

def load_to_sqlite(df: pd.DataFrame, db_path: str = "breast_cancer_data.db") -> None:
    """
    Load transformed data into SQLite database with proper schema.
    
    Args:
        df: Transformed DataFrame
        db_path: Path to SQLite database file
        
    Raises:
        RuntimeError: If database operations fail
    """
    try:
        # Ensure directory exists for db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        with sqlite3.connect(db_path) as conn:
            # Create tables matching our data model
            conn.execute('''
                CREATE TABLE IF NOT EXISTS risk_factors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    age INTEGER,
                    gender TEXT,
                    ethnicity TEXT,
                    age_menarche INTEGER,
                    menopause TEXT,
                    age_menopause INTEGER,
                    pregnancy TEXT,
                    pregnancy_age INTEGER,
                    breastfeeding TEXT,
                    hormonal_use TEXT,
                    relatives_with_cancer INTEGER,
                    brca_known TEXT,
                    breast_density TEXT,
                    cases INTEGER,
                    raw_data TEXT
                )
            ''')
            
            # Create analysis tables
            conn.execute('''
                CREATE TABLE IF NOT EXISTS risk_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factor_id INTEGER,
                    risk_score INTEGER,
                    risk_level TEXT,
                    analysis_date TEXT,
                    FOREIGN KEY(factor_id) REFERENCES risk_factors(id)
                )
            ''')

            # Add any missing columns from the DataFrame dynamically
            add_missing_columns(conn, 'risk_factors', df)

            # Insert data
            df.to_sql(
                'risk_factors',
                conn,
                if_exists='append',
                index=False,
                dtype={
                    'age': 'INTEGER',
                    'age_menarche': 'INTEGER',
                    'relatives_with_cancer': 'INTEGER',
                    'cases': 'INTEGER'
                }
            )
            
        logger.info(f"Successfully loaded {len(df)} records to {db_path}")
        
    except sqlite3.Error as e:
        raise RuntimeError(f"Database operation failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during load: {e}")


def create_analysis_tables(conn: sqlite3.Connection) -> None:
    """
    Create additional tables for analysis results.
    """
    conn.execute('''
        CREATE TABLE IF NOT EXISTS risk_cohorts (
            cohort_id INTEGER PRIMARY KEY,
            age_range TEXT,
            ethnicity TEXT,
            risk_factors TEXT,
            base_risk REAL,
            adjusted_risk REAL,
            sample_size INTEGER
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS risk_comparisons (
            comparison_id INTEGER PRIMARY KEY,
            factor TEXT,
            positive_cases INTEGER,
            negative_cases INTEGER,
            relative_risk REAL,
            confidence_interval TEXT
        )
    ''')
