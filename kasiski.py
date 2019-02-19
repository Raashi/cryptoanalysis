from sys import argv, exit
from random import choice

from utils import read_text, write_text, rus_alph
from mutils import gcd


def str_key(key):
    return str([el + 1 for el in key])


def check_mono_key(key):
    idx, start, cycle = 0, 0, 1
    while key[idx] != start:
        idx, cycle = key[idx], cycle + 1
    res = cycle == len(key)
    if not res:
        print('ОШИБКА: сгенерированный ключ не моноцикличен:', str_key(key))
    return res


def generate_key(length):
    key = [None] * length
    free = [idx for idx in range(1, length)]

    start = idx = 0
    while len(free):
        idx_next = choice(free)
        free.remove(idx_next)
        key[idx] = idx_next
        idx = idx_next
    key[idx] = start

    if not check_mono_key(key):
        exit(1)
    print('Сгенерирован ключ длины {}:'.format(length), str_key(key))
    return key


def encrypt(msg: str, key: list):
    if not check_mono_key(key):
        exit(1)

    length = len(key)
    while len(msg) % length:
        msg += choice(rus_alph)

    enc = ''
    for b in range(len(msg) // length):
        block = msg[b * length: (b + 1) * length]
        enc += ''.join(block[el] for el in key)
    return enc


def decrypt(enc, key):
    length = len(key)

    dec = ''
    for b in range(len(enc) // length):
        block = enc[b * length: (b + 1) * length]
        dec += ''.join(block[key.index(idx)] for idx in range(length))
    return dec


def find_seqs(enc, length) -> list:
    seqs = {}
    for idx in range(len(enc) - length):
        seq = enc[idx: idx + length]
        if seq not in seqs:
            seqs[seq] = []
        seqs[seq].append(idx)
    return [(key, seqs[key]) for key in filter(lambda k: len(seqs[k]) > 1, seqs)]


def kasiski(enc):
    seqs = find_seqs(enc, 4)
    seqs.sort(key=lambda el: len(el[1]), reverse=True)
    dists = []
    for (key, seq) in seqs:
        ds = []
        for seq_l, seq_n in zip(seq[:-1], seq[1:]):
            ds.append(seq_n - seq_l)
        seq_gcd = gcd(ds)
        if seq_gcd > 1:
            dists.append((key, ds, seq_gcd))
            print('SEQ: {} | GCD: {}'.format(key, seq_gcd))
    res = gcd(map(lambda triple: triple[2], dists))
    return res


def main():
    op = argv[1]

    if op == 'gk':
        length = int(argv[2])
        generate_key(length)
    elif op == 'enc':
        msg, next_lines = read_text(argv[2])
        if ',' in argv[3]:
            key = [int(el) - 1 for el in argv[3].split(',')]
        else:
            key = generate_key(int(argv[3]))

        enc = encrypt(msg, key)
        write_text('enc.txt', enc, next_lines)

    elif op == 'dec':
        enc, next_lines = read_text(argv[2])
        key = [int(el) - 1 for el in argv[3].split(',')]

        dec = decrypt(enc, key)
        write_text('dec.txt', dec, next_lines)
    elif op == 'kas':
        enc, _ = read_text(argv[2])
        length = kasiski(enc)
        print('Предполагаемая длина ключа: {}'.format(length))
    else:
        print('ОШИБКА: неверная операция')


if __name__ == '__main__':
    main()
