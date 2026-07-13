import numpy as np

def filter_and_extract(data, row_start, row_stop, threshold):
    """
    Returns: 1D ndarray of float64
    """
    arr = np.array(data, dtype='float64')
    block = arr[row_start : row_stop, :]
    mask = block > threshold
    return block[mask]