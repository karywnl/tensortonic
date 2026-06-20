import pandas as pd

def multi_groupby(data, group_cols, value_col, aggfunc):
    """
    Returns: dict of lists (flat table with group columns + value column)
    """
    df = pd.DataFrame(data)
    df = df.groupby(group_cols)[value_col].agg(aggfunc)
    return df.reset_index().to_dict('list')