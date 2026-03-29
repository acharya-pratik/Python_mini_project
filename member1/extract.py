import pandas as pd
from pathlib import Path

def extract_data(path):
    """Load CSV, JSON, Excel, or XML file into pandas DataFrame"""
    
    ext = Path(path).suffix.lower()
    
    if ext == '.csv':
        return pd.read_csv(path)
    
    elif ext == '.json':
        return pd.read_json(path)
    
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(path)
    
    elif ext == '.xml':
        return pd.read_xml(path)
    
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .csv, .json, .xlsx, .xls, or .xml")
