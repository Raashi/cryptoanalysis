from math import gcd as _gcd


def gcd(a, *other):
    if hasattr(a, '__iter__') or hasattr(a, '__next__'):
        container = list(a)
    else:
        container = [a] + list(other)
    res = container[0]
    for b in container[1:]:
        res = _gcd(res, b)
    return res
