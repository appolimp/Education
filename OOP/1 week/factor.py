def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    if isinstance(x, float) or isinstance(x, str) or x < 0:
        raise ValueError

    if x in [0, 1]:
        return x,