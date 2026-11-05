def polynomial_features(values: list, degree: int) -> list:
    """
    Returns powers from zero through degree for every value.
    """
    # Write code here
    res = []
    for i in range(len(values)):
        curr = []
        for j in range(degree + 1):
            curr.append(values[i] ** j)
        res.append(curr)

    return res