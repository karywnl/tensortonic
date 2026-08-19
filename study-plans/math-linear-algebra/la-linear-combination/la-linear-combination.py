import numpy as np

def linear_combination(vectors, coefficients):
    """
    Returns: float64 array, the weighted sum of vectors.
    """
    vectors = np.array(vectors)
    coefficients = np.array(coefficients)

    # res = np.zeros(len(vectors[0]))

    # for i in range(len(vectors)):
    #     res += coefficients[i] * vectors[i]

    # return res

    return vectors.T @ coefficients.T