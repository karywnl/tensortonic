import numpy as np

def cosine_similarity(a, b):
    """
    Returns: float in [-1, 1], cosine similarity between a and b.
    """
    a = np.array(a)
    b = np.array(b)

    res = (np.dot(a, b))/(np.linalg.norm(a) * np.linalg.norm(b))

    if np.isnan(res):
        return 0
    else:
        return res