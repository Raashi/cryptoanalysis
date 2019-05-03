from random import randint
from math import sqrt


def euclid(a, b):
    r = a % b
    while r != 0:
        a, b = b, r
        r = a % b
    return b


def legendre(a, n):
    a %= n
    if a == 0:
        return 0
    elif a == 1:
        return 1
    return pow(a, (n - 1) // 2, n)


def fac2k(a):
    k = 0
    while a & 1 == 0:
        a >>= 1
        k += 1
    return a, k


def miller_rabin(n):
    r, s = fac2k(n - 1)
    a = randint(2, n - 2)
    y = pow(a, r, n)

    if y != 1 and y != n - 1:
        j = 1
        while j <= s - 1 and y != n - 1:
            y = (y * y) % n
            if y == 1:
                return False
            j += 1
        if y != n - 1:
            return False
    return True


def is_prime(n, rounds=10):
    if n > 5:
        for _ in range(rounds):
            if not miller_rabin(n):
                return False
        return True
    return n in [2, 3, 5]


def gen_primes(count):
    container = []
    a = 2
    while len(container) < count:
        if is_prime(a):
            container.append(a)
        a += 1
    return container


def gen_chain_fraction(p, q):
    a = int(p / q)
    yield a

    while p != q:
        p, q = q, p - q * a
        a = int(p / q)
        yield a


def gen_square_chain_fraction(n):
    a0 = sqrt(n)
    r0 = int(a0)
    yield r0
    ratio0 = 1
    numenator0 = 0

    while True:
        numenator1 = r0 * ratio0 - numenator0
        ratio1 = (n - numenator1 * numenator1) // ratio0
        if ratio1 == 0:
            raise ValueError('Число является полным квадратом')
        r1 = int((a0 + numenator1) / ratio1)

        yield r1
        r0, ratio0, numenator0 = r1, ratio1, numenator1


def gen_convergent(generator):
    p0, p1 = 0, 1
    q0, q1 = 1, 0

    while True:
        ai = next(generator)
        pi = ai * p1 + p0
        qi = ai * q1 + q0
        yield pi, qi
        p0, p1, q0, q1 = p1, pi, q1, qi


def gaussian(mat):
    pass


if __name__ == '__main__':
    from sys import argv
    _count = int(argv[1]) if len(argv) > 1 else 100
    _primes = gen_primes(_count)
    with open('p.txt', 'w') as f:
        f.write('\n'.join(map(str, _primes)))
