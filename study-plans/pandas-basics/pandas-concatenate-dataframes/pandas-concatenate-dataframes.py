import pandas as pd

def concat_dataframes(dfs):
    """
    Returns: list [shape, data] where shape is [rows, cols]
    """
    dfs_list = []
    for df in dfs:
        dfs_list.append(pd.DataFrame(df))

    concat_df = pd.concat(dfs_list)
    return [list(concat_df.shape), concat_df.to_dict('list')]
    