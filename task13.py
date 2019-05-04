from sys import argv
from random import randint
from math import sqrt, log, exp
from functools import reduce
from operator import add

from mutils import legendre, gen_convergent, gen_square_chain_fraction, \
    euclid, is_prime
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
    for idx, ks in enumerate(gaussian(es)):
        s = 1
        for k in ks:
            s = (s * ps[k]) % n
        t = 1
        for b_idx, b in enumerate(base):
            t = (t * pow(b, reduce(add, (alphas[k][b_idx] for k in ks)) // 2, n)) % n

        if s != t and s != n - t:
            p = euclid((s - t) % n, n)
            return p
        if idx > SOLUTIONS_TO_CHECK:
            break
    return -1


def dixon_chain(n, primes):
    base = [-1] + dixon_base(n, primes, check_legendre=True)
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


def dixon_modified(n, primes):
    base = [-1] + dixon_base(n, primes)
    h = len(base)

    idx = 0
    while True:
        ps, alphas, es = [], [], []
        while len(ps) < h + 1:
            b = randint(int(sqrt(n)), n)
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


def dixon_usual(n, primes):
    base = dixon_base(n, primes)
    h = len(base)

    idx = 0
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
        if prime > base_max:
            break
        if check_legendre and legendre(n, prime) != 1:
            continue
        base.append(prime)
    return base


def main():
    n = int(argv[1])

    if is_prime(n, 25):
        print('{} - простое'.format(n))
        return

    with open('p.txt') as f:
        primes_data = f.read()
    primes = list(map(int, primes_data.split('\n')))

    print('Размер базы = {}'.format(len(dixon_base(n, primes))))

    if '-u' in argv:
        p = dixon_usual(n, primes)
        print('Стандартный алгоритм:\n{}'.format(p))
    elif '-m' in argv:
        p = dixon_modified(n, primes)
        print('С добавлением -1 и выбором наименьшего а:\n{}'.format(p))
    elif '-c' in argv:
        p = dixon_chain(n, primes)
        print('С использованием цепных дробей:\n{}'.format(p))
    else:
        print('Неизвестный алгоритм')


if __name__ == '__main__':
    main()
