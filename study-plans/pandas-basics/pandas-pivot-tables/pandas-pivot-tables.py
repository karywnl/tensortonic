import pandas as pd

def create_pivot(data, index, columns, values, aggfunc):
    """
    Returns: nested dict {column_value: {index_value: agg_result}}
    """
    df = pd.DataFrame(data)
    pivot_df = pd.pivot_table(df, 
                             index=index,
                             columns=columns,
                             values=values,
                             aggfunc=aggfunc,
                             fill_value=0)

    return pivot_df.to_dict()