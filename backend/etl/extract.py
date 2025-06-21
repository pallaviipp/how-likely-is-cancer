import pandas as pd

def extract_csv_data(filepath: str) -> pd.DataFrame:
    """
    Extracts raw breast cancer dataset from a CSV file.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to extract data: {e}")
#import pandas as pd
#import os
#import shutil
#def extract_csv(file_path: str, save_dir="data/raw/"):
#    os.makedirs(save_dir, exist_ok=True)
#    filename = os.path.basename(file_path)
#    raw_path = os.path.join(save_dir, filename)
#    shutil.copy(file_path, raw_path)
#    df = pd.read_csv(file_path)
#    return df
