import pandas as pd

def select_column(data, column):
    """
    Returns: dict with 'values' (list) and 'length' (int)
    """
    df = pd.DataFrame(data)
    values = df[column].to_list()
    length = len(df[column])
    return {
        "values" : values,
        "length" : length
    }