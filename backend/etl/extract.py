import pandas as pd
import os
from typing import List, Dict
import logging

def extract_csv_data(filepaths: List[str]) -> pd.DataFrame:
    """
    Extract and concatenate multiple CSV files with identical structure.
    
    Args:
        filepaths: List of paths to CSV files
        
    Returns:
        pd.DataFrame: Combined DataFrame from all files
        
    Raises:
        RuntimeError: If extraction fails for any file
    """
    dfs = []
    
    try:
        for filepath in filepaths:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Data file not found: {filepath}")
                
            df = pd.read_csv(filepath)
            dfs.append(df)
            
        combined = pd.concat(dfs, ignore_index=True)
        
        # Basic validation
        if combined.empty:
            raise ValueError("Combined data is empty")
            
        return combined
        
    except pd.errors.EmptyDataError:
        raise ValueError("One or more CSV files appear to be empty")
    except pd.errors.ParserError:
        raise ValueError("Failed to parse CSV file - may be malformed")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during extraction: {e}")


def validate_extracted_data(df: pd.DataFrame) -> bool:
    """
    Validate that extracted data contains required columns.
    """
    required_columns = {
        'age_group_5_years', 'race_eth', 'age_menarche',
        'age_first_birth', 'BIRADS_breast_density',
        'current_hrt', 'menopaus', 'bmi_group',
        'first_degree_hx', 'count'
    }
    
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in raw data: {missing}")
        
    return True
