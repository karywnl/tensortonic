import pandas as pd

def reset_index_demo(data, index_col):
    """
    Returns: list [columns_before_reset, columns_after_reset]
    """
    df = pd.DataFrame(data)
    df = df.set_index(index_col)
    columns_before = list(df.columns)
    df = df.reset_index()
    columns_after = list(df.columns)
    return [columns_before, columns_after]