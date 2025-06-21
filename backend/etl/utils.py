import os

def get_data_path(filename: str) -> str:
    """
    Generate full path to a data file within the project.
    """
    return os.path.join(os.path.dirname(__file__), '../data', filename)
