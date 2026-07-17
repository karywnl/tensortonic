import numpy as np

def original_and_clipped(data, row_idx, lo, hi):
    """
    Returns: 2D ndarray of float64 with shape (2, ncols)
    """
    arr = np.array(data, dtype='float64')

    row = arr[row_idx]
    clip_row = np.clip(row, lo, hi)

    return [row, clip_row]