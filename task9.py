from operator import mul
from functools import reduce

from utils import *


def gen_base(primes, t):
    base = []
    for start in range(len(primes) // t):
        cur_base = primes[start * t: (start + 1) * t]
        base.append((reduce(mul, cur_base), cur_base))
    return base


def trial_division(n, pb):
    divisors = {}
    for item_1 in pb:
        item = item_1[0]
        d = gcd(n, item)
        if d > 1:
            true_divisors = list(filter(lambda x: d % x == 0, item_1[1]))
            for td in true_divisors:
                while n % td == 0:
                    n //= td
                    divisors[td] = divisors.get(td, 0) + 1
        if n == 1:
            break
    if n > 1:
        divisors[n] = 1
    return divisors


def main():
    if op == 'gen':
        primes = read_ints_list(argv[2])
        t = int(argv[3])
        write('pb.txt', '\n'.join(map(lambda x: '{}:{}'.format(x[0], x[1]), gen_base(primes, t))))
    elif op == 'div':
        pb = read(argv[2]).split('\n')
        pb = map(lambda x: x.split(':'), pb)
        pb = list(map(lambda x: (int(x[0]), eval(x[1])), pb))
        n = int(argv[3]) if len(argv) > 3 else int(input('Введите n = '))
        divisors = trial_division(n, pb)
        divisors_str = '\n'.join(map(str, sorted(divisors.items())))
        write('divs.txt', divisors_str)
    else:
        print_wrong_op()


if __name__ == '__main__':
    main()
