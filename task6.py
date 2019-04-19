from math import sqrt

from utils import *
from cyphers import get_freqs, write_freqs, read_freqs
import cyphers.vigenere as vig


def get_h0(text, alph):
    m = len(alph)
    freqs = get_freqs(text, alph)
    freqs = [(char, float(value)) for char, value in freqs]
    h0 = [[letter, 0] for letter in alph]
    for i in range(m):
        for k in range(m):
            j = (i - k) % m
            h0[j][1] += freqs[i][1] * freqs[k][1]
    h0 = [(char, '{:.5f}'.format(freq)) for char, freq in h0]
    return freqs, h0


def get_hd(enc, alph, d):
    n = len(enc)
    while n % d:
        n -= 1
    t, r = n // d, (len(enc)) - n

    z = ''
    for idx in range((t - 1) * d + r):
        idx_next = idx + d
        if enc[idx] in alph and enc[idx_next] in alph:
            letter = alph[(alph.index(enc[idx]) - alph.index(enc[idx_next])) % len(alph)]
            z += letter
    hd = [(letter, z.count(letter) / len(z)) for letter in alph]
    return hd


def get_norm(x):
    return sqrt(sum(map(lambda xi: xi ** 2, x)))


def get_distance(x, y):
    return get_norm([yi - xi for xi, yi in zip(x, y)])


def main():
    if op == 'enc':
        vig.exec_encrypt()
    elif op == 'dec':
        vig.exec_decrypt()
    elif op == 'h0':
        text = read(argv[2]).lower()
        alph = read(argv[3])
        freqs, h0 = get_h0(text, alph)
        write_freqs('f.txt', freqs)
        write_freqs('h0.txt', h0)
    elif op == 'hd':
        enc = read(argv[2])
        h0 = read_freqs(argv[3])
        alph = ''.join(map(lambda h0i: h0i[0], h0))
        n1 = int(argv[4])
        n2 = int(argv[5])

        hds = [get_hd(enc, alph, d) for d in range(n1, n2 + 1)]
        n_min, dist_min = None, 1
        for idx, hd in enumerate(hds):
            dist = get_distance(
                list(map(lambda xi: float(xi[1]), h0)),
                list(map(lambda yi: yi[1], hd)))
            if dist < dist_min:
                n_min, dist_min = n1 + idx, dist
            print(n1 + idx, ':', dist)
        print('Наименьшее расстояние до H0 при d =', n_min)
    else:
        print_wrong_op()


if __name__ == '__main__':
    main()
