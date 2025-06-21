from pathlib import Path
from typing import List, Dict, Optional, Any
import logging
import os
import sys
from backend.etl.extract import extract_csv_data, validate_extracted_data
from backend.etl.transform import clean_and_transform, validate_transformed_data
from backend.etl.load import load_to_sqlite

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_data_files(raw_data_dir: str) -> List[str]:
    """Get list of data files to process"""
    return [
        os.path.join(raw_data_dir, f"breast_cancer_risk_data{i if i > 0 else ''}.csv")
        for i in range(3)  # For files 0, 1, and 2
    ]

def run_etl_pipeline(config: Dict[str, Any]) -> None:
    """
    Run complete ETL pipeline with multiple input files of identical structure.
    """
    try:
        logger.info("Starting ETL pipeline for multiple CSV files")
        
        # Get list of files to process
        data_files = get_data_files(config['raw_data_dir'])
        logger.info(f"Processing files: {', '.join(data_files)}")
        
        # Extract from all files
        logger.info("Extracting and combining data")
        raw_data = extract_csv_data(data_files)
        validate_extracted_data(raw_data)
        
        # Optionally sample data for testing
        if config.get('sample_size', 0) > 0:
            raw_data = raw_data.sample(
                min(config['sample_size'], len(raw_data))
            )
            logger.info(f"Sampled {len(raw_data)} records")
        
        # Transform
        logger.info("Transforming data")
        transformed_data = clean_and_transform(raw_data)
        validate_transformed_data(transformed_data)
        
        # Load
        logger.info(f"Loading data to {config['db_path']}")
        load_to_sqlite(transformed_data, config['db_path'])
        
        logger.info(f"ETL pipeline completed successfully. Processed {len(transformed_data)} records.")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise RuntimeError(f"ETL pipeline failed: {e}")


if __name__ == "__main__":
    config = {
        'raw_data_dir': 'backend/data/raw',
        'db_path': 'backend/data/processed/breast_cancer_risk.db',
        'sample_size': 0  # 0 for all records
    }
    
    # Ensure output directory exists
    Path(config['db_path']).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        run_etl_pipeline(config)
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise
