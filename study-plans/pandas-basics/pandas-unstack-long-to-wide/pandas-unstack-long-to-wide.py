import pandas as pd

def unstack_to_wide(data, index_col, columns_col, values_col):
    """
    Returns: dict with index_col plus one key per unique value in columns_col
    """
    df = pd.DataFrame(data)
    g = df.groupby([index_col, columns_col])[values_col].sum()
    res = g.unstack(columns_col).reset_index(index_col)
    return res.to_dict('list')