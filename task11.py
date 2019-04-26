from sys import argv
from random import randint
from math import gcd, log

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
    with open(argv[2]) as f:
        primes = list(map(int, f.read().split('\n')))
    s = DEFAULT_S if len(argv) < 4 else int(argv[3])
    p = p1_pollard(n, primes, s)
    if p == -1:
        print('Делитель не найден')
    else:
        print('Найден делитель p =', p)


if __name__ == '__main__':
    main()
