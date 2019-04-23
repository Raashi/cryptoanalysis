from operator import mul
from functools import reduce

from utils import *


def gen_base(primes, t):
    base = []
    for start in range(len(primes) // t):
        base.append(reduce(mul, primes[start * t: (start + 1) * t]))
    return base


def trial_division(n, pb):
    divisors = []
    for item in pb:
        d = gcd(n, item)
        while d > 1:
            divisors.append(d)
            n //= gcd(n, item)
            d = gcd(n, item)
        if n == 1:
            break
    if n > 1:
        divisors.append(n)
    return divisors


def main():
    if op == 'gen':
        primes = read_ints_list(argv[2])
        t = int(argv[3])
        write('pb.txt', '\n'.join(map(str, gen_base(primes, t))))
    elif op == 'div':
        pb = read_ints_list(argv[2])
        n = int(argv[3]) if len(argv) > 3 else int(input('Введите n = '))
        divisors = trial_division(n, pb)
        write_ints_list('divs.txt', divisors)
    else:
        print_wrong_op()


if __name__ == '__main__':
    main()
