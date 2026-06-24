import numpy as np
from collections import Counter

def mean_median_mode(x):
    """
    Returns: dict with 'mean', 'median', 'mode' as floats.
    """
    mean = np.mean(x)
    median = np.median(x)
    cnt = Counter(x)   
    return {
        "mean" : mean,
        "median" : median,
        "mode" : float(cnt.most_common(1)[0][0])
    }