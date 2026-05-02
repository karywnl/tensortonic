import pandas as pd

def inspect_dataframe(data):
    """
    Returns: dict with 'rows', 'cols' (ints), 'columns' (list),
    'dtypes' (dict), 'total_values' (int)
    """
    df = pd.DataFrame(data)
    n_rows = df.shape[0]
    n_cols = df.shape[1]
    cols = df.columns.tolist()
    dtypes = {col : str(dtype) for col, dtype in df.dtypes.items()}
    n_val = n_rows * n_cols
    
    return { 
        "rows" : n_rows,
        "cols" : n_cols,
        "columns" : cols,
        "dtypes" : dtypes,
        "total_values" : n_val
    }