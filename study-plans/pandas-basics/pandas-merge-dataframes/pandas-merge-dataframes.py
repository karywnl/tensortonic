import pandas as pd

def merge_dataframes(left, right, on, how):
    """
    Returns: dict of column to value lists
    """
    df_left = pd.DataFrame(left)
    df_right = pd.DataFrame(right)
    df = pd.merge(df_left, df_right, on=on, how=how)
    return df.to_dict('list')