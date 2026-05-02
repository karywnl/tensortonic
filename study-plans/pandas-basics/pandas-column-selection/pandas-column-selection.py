import pandas as pd

def select_column(data, column):
    """
    Returns: dict with 'values' (list) and 'length' (int)
    """
    df = pd.DataFrame(data)
    values = list(df[column])
    length = len(df[column])
    return {
        "values" : values,
        "length" : length
    }