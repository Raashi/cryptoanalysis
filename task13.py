from sys import argv
from random import randint
from math import sqrt, log, exp
from functools import reduce
from operator import add

from mutils import legendre, gen_convergent, gen_square_chain_fraction, \
    euclid
from gaussian import gen_gaussian


def is_b_smooth(p, base):
    alpha = []
    for bi in base:
        k = 0
        while p % bi == 0 and not bi < 0 < p and p != 1:
            p //= bi
            k += 1
        alpha.append(k)
    return p == 1, alpha, [al % 2 for al in alpha]


def check_bi(n, base, ps, alphas, es):
    ks = next(gen_gaussian(es))
    s = 1
    for k in ks:
        s = (s * ps[k]) % n
    t = 1
    for b_idx, b in enumerate(base):
        t = (t * pow(b, reduce(add, (alphas[k][b_idx] for k in ks)) // 2, n)) % n
    # проверка, что ks - не решение системы
    assert pow(s, 2, n) == pow(t, 2, n)

    if s != t and s != n - t:
        p = euclid((s - t) % n, n)
        return p
    return -1


def dixon_chain(n, primes):
    base = dixon_base(n, primes)
    h = len(base)

    ps, alphas, es = [], [], []
    convergent = gen_convergent(gen_square_chain_fraction(n))
    while len(ps) < h + 1:
        try:
            pi, qi = next(convergent)
        except ValueError:
            return -1

        pi2 = pi ** 2 % n
        if n - pi2 < pi2:
            pi2 = -(n - pi2)
        smooth, alpha, e = is_b_smooth(pi2, base)
        if smooth:
            ps.append(pi)
            alphas.append(alpha)
            es.append(e)

    p = check_bi(n, base, ps, alphas, es)
    if p != -1:
        return p


def dixon_usual(n, primes):
    base = dixon_base(n, primes)
    h = len(base)

    while True:
        ps, alphas, es = [], [], []
        while len(ps) < h + 1:
            b = randint(int(sqrt(n)), n)
            a = pow(b, 2, n)
            smooth, alpha, e = is_b_smooth(a, base)
            if smooth:
                ps.append(b)
                alphas.append(alpha)
                es.append(e)

        p = check_bi(n, base, ps, alphas, es)
        if p != -1:
            return p


def dixon_base(n, primes):
    base_size = int(sqrt(exp(sqrt(log(n) * log(log(n))))))
    return primes[:base_size]


def main():
    n = int(argv[1])  # 49201699  # 1045421989  # 10250071841  # int(argv[1])
    with open('p.txt') as f:
        primes_data = f.read()
    primes = list(map(int, primes_data.split('\n')))
    p = dixon_usual(n, primes)
    print('Алгоритм Диксона:', p)
    p = dixon_chain(n, primes)
    print('С использованием цепных дробей:', p)


if __name__ == '__main__':
    main()
