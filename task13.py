from sys import argv
from random import randint
from math import sqrt, log, exp
from functools import reduce
from operator import add

from mutils import legendre, gen_convergent, gen_square_chain_fraction, \
    euclid, is_prime, isqrt
from gaussian import gaussian


MAX_ITERATIONS_DIXON = 10
SOLUTIONS_TO_CHECK = 100


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
    for ks in gaussian(es):
        s = 1
        for k in ks:
            s = (s * ps[k]) % n
        t = 1
        for b_idx, b in enumerate(base):
            t = (t * pow(b, reduce(add, (alphas[k][b_idx] for k in ks)) // 2, n))
        assert pow(s, 2, n) == pow(t, 2, n)

        if s != t % n and s != (-t) % n:
            p = euclid(s + t, n)
            return p
    return -1


def dixon_chain(n, base):
    h = len(base)

    ps, alphas, es = [], [], []
    convergent = gen_convergent(gen_square_chain_fraction(n))
    while len(ps) < h + 1:
        try:
            pi, _ = next(convergent)
        except ValueError:
            return -1

        pi2 = pow(pi, 2, n)
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
    return -1


def dixon_modified(n, base):
    h = len(base)

    idx = 0
    while True:
        ps, alphas, es = [], [], []
        while len(ps) < h + 1:
            b = randint(isqrt(n), n)
            a = pow(b, 2, n)
            if a > n - a:
                a = -(n - a)
            smooth, alpha, e = is_b_smooth(a, base)
            if smooth:
                ps.append(b)
                alphas.append(alpha)
                es.append(e)

        p = check_bi(n, base, ps, alphas, es)
        if p != -1:
            return p

        idx += 1
        if idx % MAX_ITERATIONS_DIXON == 0:
            ans = input('Прошло {} итераций алгоритма. Продолжать? (y/n) '.format(idx))
            if ans.lower() != 'y':
                return -1


def dixon_usual(n, base):
    h = len(base)

    idx = 0
    while True:
        ps, alphas, es = [], [], []

        while len(ps) < h + 1:
            b = randint(isqrt(n), n)
            if b in ps:
                continue
            a = pow(b, 2, n)
            smooth, alpha, e = is_b_smooth(a, base)
            if smooth:
                ps.append(b)
                alphas.append(alpha)
                es.append(e)

        p = check_bi(n, base, ps, alphas, es)
        if p != -1:
            return p

        idx += 1
        if idx % MAX_ITERATIONS_DIXON == 0:
            ans = input('Прошло {} итераций алгоритма. Продолжать? (y/n) '.format(idx))
            if ans.lower() != 'y':
                return -1


def dixon_base(n, primes, check_legendre=False):
    base_max = int(sqrt(exp(sqrt(log(n) * log(log(n))))))
    idx = 0
    base = []
    while idx < len(primes):
        prime = primes[idx]
        idx += 1
        if prime > base_max and len(base) > 2:
            break
        if check_legendre and legendre(n, prime) != 1:
            continue
        base.append(prime)
    return base


def dixon(n, primes, func):
    check_legendre = func == dixon_chain
    base = ([] if func == dixon_usual else [-1]) + dixon_base(n, primes, check_legendre=check_legendre)
    start_len = max(1, len(base) - 10)

    p = func(n, base)
    while (p == 1 or p == -1) and len(base) > start_len:
        # print(base)
        base = base[:-1]
        p = func(n, base)
    if p != 1 and p != -1:
        return p

    base = ([] if func == dixon_usual else [-1]) + dixon_base(n, primes, check_legendre=check_legendre)
    idx_prime_last = 0
    while base[-1] != primes[idx_prime_last]:
        idx_prime_last += 1
    idx_prime_last += 1
    start_len = len(base) + 5
    p = func(n, base)
    while (p == 1 or p == -1) and len(base) <= start_len:
        # print(base)
        if not check_legendre:
            base.append(primes[idx_prime_last])
            idx_prime_last += 1
        else:
            while idx_prime_last < len(primes):
                prime = primes[idx_prime_last]
                idx_prime_last += 1
                if legendre(n, prime) == 1:
                    base.append(prime)
                    break
        p = func(n, base)
    return p


def main():
    n = int(argv[1])

    if is_prime(n, 25):
        print('{} - простое'.format(n))
        return

    with open('p.txt') as f:
        primes_data = f.read()
    primes = list(map(int, primes_data.split('\n')))

    if '-u' in argv:
        p = dixon(n, primes, dixon_usual)
        assert n % p == 0
        print('Стандартный алгоритм:\n{} * {}'.format(p, n // p)) \
            if p != -1 else print('Делитель не найден')
    if '-m' in argv:
        p = dixon(n, primes, dixon_modified)
        assert n % p == 0
        print('С добавлением -1 и выбором наименьшего а:\n{} * {}'.format(p, n // p)) \
            if p != -1 else print('Делитель не найден')
    if '-c' in argv:
        p = dixon(n, primes, dixon_chain)
        assert n % p == 0
        print('С использованием цепных дробей:\n{} * {}'.format(p, n // p)) \
            if p != -1 else print('Делитель не найден')


if __name__ == '__main__':
    main()
