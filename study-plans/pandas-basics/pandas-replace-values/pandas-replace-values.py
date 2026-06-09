import pandas as pd

def replace_values(data, column, old_val, new_val):
    """
    Returns: dict with 'data' (dict) and 'count' (int)
    """
    df = pd.DataFrame(data)
    if old_val in df[column].to_list():
        cnt = df[column].value_counts().loc[old_val]
    else:
        cnt = 0
    df[column] = df[column].replace(old_val, new_val)

    return {
        "data" : df.to_dict('list'),
        "count" : cnt
    }
    