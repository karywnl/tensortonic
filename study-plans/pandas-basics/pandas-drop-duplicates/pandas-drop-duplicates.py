import pandas as pd

def drop_duplicates(data):
    """
    Returns: list [rows_before, rows_after, cleaned_data]
    """
    df = pd.DataFrame(data)
    dedup_df = df[~df.duplicated()]
    return [
        df.shape[0],
        dedup_df.shape[0],
        dedup_df.to_dict('list')
    ]