import pandas as pd
from typing import Dict, Any
from backend.models import RiskForm  # Import your Pydantic model for reference
import logging

logger = logging.getLogger(__name__)

def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform raw data to match application data model.
    
    Args:
        df: Raw DataFrame from extract step
        
    Returns:
        pd.DataFrame: Transformed data matching RiskForm structure
    """
    # Replace common missing values
    df.replace(9, pd.NA, inplace=True)

    # Define mappings to match frontend options
    mappings = {
        'race_eth': {
            1: "White",
            2: "Black",
            3: "Hispanic",
            4: "Asian or Pacific Islander",
            5: "Native American",
            6: "Other",
            9: pd.NA
        },
        'BIRADS_breast_density': {
            1: "No",
            2: "No",
            3: "Yes",
            4: "Yes",
            9: "Don't know"
        },
        'current_hrt': {
            1: "No",
            2: "Yes",
            9: "Not sure"
        },
        'menopaus': {
            1: "No",
            2: "Yes",
            3: "Not sure",
            9: "Not sure"
        },
        'bmi_group': {
            1: "<18.5",
            2: "18.5–24.9",
            3: "25–29.9",
            4: "30+",
            9: pd.NA
        }
    }

    # Apply mappings
    for col, mapping in mappings.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    # Rename columns to match RiskForm model
    column_renames = {
        'race_eth': 'ethnicity',
        'BIRADS_breast_density': 'breast_density',
        'current_hrt': 'hormonal_use',
        'menopaus': 'menopause',
        'first_degree_hx': 'relatives_with_cancer',
        'age_first_birth': 'pregnancy_age',
        'count': 'cases'
    }
    df = df.rename(columns=column_renames)

    # Add derived field
    df['pregnancy'] = df['pregnancy_age'].apply(
        lambda x: "No" if pd.isna(x) else "Yes"
    )

    # Add derived age field
    if 'age_group_5_years' in df.columns:
        df['age'] = df['age_group_5_years'].apply(
            lambda x: (x * 5) + 17
        )

    # Fill missing RiskForm fields with NA
    risk_form_fields = set(RiskForm.__fields__.keys())
    for field in risk_form_fields:
        if field not in df.columns:
            df[field] = pd.NA

    # Ensure only relevant fields are kept
    return df[list(risk_form_fields) + ['cases']]


def validate_transformed_data(df: pd.DataFrame) -> bool:
    """
    Validate transformed data matches expected schema.
    
    Args:
        df: Transformed DataFrame
        
    Returns:
        bool: True if validation passes
        
    Raises:
        ValueError: If data doesn't match expected schema
    """
    required_fields = set(RiskForm.__fields__.keys())
    missing = required_fields - set(df.columns)
    
    if missing:
        raise ValueError(f"Transformed data missing required fields: {missing}")

    validations = {
        'ethnicity': [
            "White", "Black", "Hispanic", "Asian or Pacific Islander",
            "Native American", "Other"
        ],
        'breast_density': ["No", "Yes", "Don't know"],
        'menopause': ["No", "Yes", "Not sure"],
        'hormonal_use': ["No", "Yes", "Not sure"]
    }

    for field, allowed_values in validations.items():
        if field in df.columns:
            # Only check non-null entries
            invalid = ~df[field].isin(allowed_values) & df[field].notna()
            if invalid.any():
                raise ValueError(
                    f"Invalid values in {field}: {df[field][invalid].unique()}"
                )

    logger.info("Data validation passed")
    return True
