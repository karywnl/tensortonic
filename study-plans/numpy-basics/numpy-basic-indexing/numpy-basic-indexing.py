import numpy as np

def extract_subarray(arr, row_start, row_stop, col_start, col_stop):
    """
    Returns: 2D ndarray of float64
    """
    arr = np.array(arr, dtype='float64')
    return arr[row_start:row_stop, col_start:col_stop]