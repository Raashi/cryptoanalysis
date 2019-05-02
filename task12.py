from math import sqrt, gcd
from prime import factorize


def good_sqrt(x):
    return int(sqrt(x)) ** 2 == x


def fermat(n, k, iters):
    s = int(sqrt(k * n))
    idx = 1
    while True:
        s_new = s + idx
        t2 = (s_new * s_new) - (k * n)
        if good_sqrt(t2):
            d = gcd(k * n, s_new - int(sqrt(t2)))
            return d
        if idx % iters == 0 and idx > 0:
            ans = input('Прошло {} итераций. Продолжать? Y/N: '.format(idx))
            if ans != 'Y' and ans != 'y':
                return -1
        idx += 1


def main():
    n = int(input('Введите n = '))
    k = int(input('Введите k = '))
    iters = int(input('Введите l = '))

    factors = factorize(n, fermat, k, iters)
    print('\n'.join(map(str, factors.items())))


if __name__ == '__main__':
    main()
