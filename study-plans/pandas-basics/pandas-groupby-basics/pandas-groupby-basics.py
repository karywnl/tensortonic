import pandas as pd

def groupby_basics(data, group_col, value_col):
    """
    Returns: dict with 'sum', 'mean', 'count' (each a dict)
    """
    df = pd.DataFrame(data)
    grouped = df.groupby(group_col)[value_col]
    return {
        "sum": grouped.sum().to_dict(),
        "mean": grouped.mean().to_dict(),
        "count": grouped.count().to_dict()
    }