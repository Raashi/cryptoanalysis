from math import sqrt

from random import randint
from mutils import euclid, get_inverse, fac2k

from utils import *
from prime import gen_prime


def square_root(n):
    x1 = n
    x2 = int((x1 + (n / x1)) / 2)
    while x2 < x1:
        x1, x2 = x2, int((x2 + (n / x2)) / 2)
    return x1


def gen_params(bit_count):
    p = gen_prime(bit_count)
    q = gen_prime(bit_count)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = randint(2, phi - 1)
    while euclid(e, phi) > 1:
        e = randint(2, phi - 1)

    d = get_inverse(e, phi)

    write('pq.txt', '{}\n{}'.format(p, q))
    write('open.txt', '{}\n{}'.format(n, e))
    write('secret.txt', str(d))


def attack_by_phi(n, phi):
    discr = (n - phi + 1) ** 2 - (4 * n)
    sqrt_discr = round(sqrt(discr))
    assert discr == sqrt_discr ** 2

    p = (n - phi + 1 + sqrt_discr) // 2
    q = (n - phi + 1 - sqrt_discr) // 2
    print(p)
    print(q)
    assert n == p * q


def attack_by_params(n, e, d):
    s, f = fac2k(e * d - 1)
    while True:
        a = randint(2, n - 2)
        u = pow(a, s, n)
        v = pow(u, 2, n)
        while v != 1:
            u = v
            v = pow(u, 2, n)
        if u == -1:
            continue
        p = euclid(u - 1, n)
        q = euclid(u + 1, n)
        print(p)
        print(q)
        return


def main():
    if op == 'gen':
        bit_count = int(argv[2])
        gen_params(bit_count)
    elif op == 'phi':
        if argv[2] == 'file':
            n, phi = tuple(map(int, read(argv[3]).split('\n')))
        else:
            n = int(argv[2])
            phi = int(argv[3])
        attack_by_phi(n, phi)
    elif op == 'par':
        n, e = tuple(map(int, read(argv[2]).split('\n')))
        d = int(read(argv[3]))
        attack_by_params(n, e, d)
    elif op == 'mf':
        n, _ = tuple(map(int, read(argv[2]).split('\n')))
        p, q = tuple(map(int, read(argv[3]).split('\n')))
        write('in.txt', '{}\n{}'.format(n, (p - 1) * (q - 1)))
    else:
        print_wrong_op()


if __name__ == '__main__':
    main()
