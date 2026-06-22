import pandas as pd

def apply_transform(data, column, operation):
    """
    Returns: dict with original columns plus column_transformed
    """
    df = pd.DataFrame(data)

    def transform(s):
        if operation == "normalize":
            return round((s - df[column].min())/(df[column].max() - df[column].min()), 4)
        elif operation == "rank":
            lst = df[column].tolist()
            lst.sort()
            return lst.index(s) + 1

    col_name = f'{column}_transformed'
    if operation == "cumsum":
        df[col_name] = df[column].cumsum()
    elif operation == "double":
        df[col_name] = df[column]*2
    else:
        df[col_name] = df[column].apply(transform)

    return df.to_dict('list')