import numpy as np

def cosine_similarity(a, b):
    """
    Returns: float in [-1, 1], cosine similarity between a and b.
    """
    a = np.array(a)
    b = np.array(b)

    if np.linalg.norm(a) == 0.0 or np.linalg.norm(b) == 0.0:
        return 0.0

    return (np.dot(a, b))/(np.linalg.norm(a) * np.linalg.norm(b))