from sys import argv
from random import randint
from math import gcd, log

from prime import factorize

DEFAULT_S = 10


def p1_pollard(n, primes, s):
    base = primes[:s]

    a = randint(2, n - 2)
    d = gcd(a, n)
    if d >= 2:
        return d
    for i in range(s):
        power = int(log(n) / log(base[i]))
        a = (a * pow(a, pow(base[i], power), n)) % n
    d = gcd(a - 1, n)
    return d if 1 < d < n else -1


def main():
    n = int(argv[1])
    with open('p.txt') as f:
        primes = list(map(int, f.read().split('\n')))
    s = DEFAULT_S if len(argv) < 3 else int(argv[2])

    factors = factorize(n, p1_pollard, primes, s)
    print('\n'.join(map(str, factors.items())))


if __name__ == '__main__':
    main()
