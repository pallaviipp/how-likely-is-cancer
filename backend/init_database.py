import sqlite3
import pandas as pd
from pathlib import Path
import sys
from build_baseline import build_risk_baseline

def initialize_database():
    print("Initializing database...")
    
    # Setup paths
    raw_dir = Path("backend/data/raw")
    processed_dir = Path("backend/data/processed")
    db_path = processed_dir / "breast_cancer_risk.db"
    
    # Ensure directories exist
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove old database if exists
    if db_path.exists():
        db_path.unlink()
    
    try:
        # Connect to new database
        conn = sqlite3.connect(db_path)
        
        # Load and combine all CSV files
        dfs = []
        for csv_file in raw_dir.glob("breast_cancer_risk_data*.csv"):
            print(f"Processing {csv_file.name}...")
            df = pd.read_csv(csv_file)
            dfs.append(df)
        
        if not dfs:
            raise ValueError("No CSV files found in backend/data/raw/")
        
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Save to SQLite
        combined_df.to_sql("risk_data", conn, index=False, if_exists="replace")
        print("Base data loaded successfully.")
        
        # Build baseline tables
        build_risk_baseline()
        
        print(f"Database initialized at {db_path}")
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        if db_path.exists():
            db_path.unlink()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)
