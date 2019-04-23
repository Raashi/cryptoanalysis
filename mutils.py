from random import randint


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


if __name__ == '__main__':
    from sys import argv
    _count = int(argv[1]) if len(argv) > 1 else 100
    _primes = gen_primes(_count)
    with open('p.txt', 'w') as f:
        f.write('\n'.join(map(str, _primes)))
