"""
usage:
%user%:> python kasiski.py gen 4
%user%:> python kasiski.py enc test.txt 2,4,1,3
%user%:> python kasiski.py dec enc.txt 2,4,1,3
%user%:> python kasiski.py kas enc.txt
"""
from sys import argv, exit
from random import choice

from utils import read_text, write_text, alph_rus, gcd, write, read


def str_key(key):
    return ','.join(map(lambda el: str(el + 1), key))


def check_mono_key(key):
    idx, start, cycle = 0, 0, 1
    while key[idx] != start:
        idx, cycle = key[idx], cycle + 1
    res = cycle == len(key)
    if not res:
        print('ОШИБКА: сгенерированный ключ не моноцикличен:', str_key(key))
    return res


def read_key(skey):
    return list(map(lambda el: int(el) - 1, skey.split(',')))


def generate_key(length: int):
    key = [None] * length
    free = [idx for idx in range(1, length)]

    start = idx = 0
    while len(free):
        idx_next = choice(free)
        free.remove(idx_next)
        key[idx] = idx_next
        idx = idx_next
    # noinspection PyTypeChecker
    key[idx] = start

    if not check_mono_key(key):
        exit(1)
    print('Сгенерирован ключ длины {}:'.format(length), str_key(key))
    write('key.txt', str_key(key))
    return key


def encrypt(msg: str, key: list):
    if not check_mono_key(key):
        exit(1)

    length = len(key)
    while len(msg) % length:
        msg += choice(alph_rus)

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


def get_seqs(enc, length) -> dict:
    seqs = {}
    for idx in range(len(enc) - length):
        seq = enc[idx: idx + length]
        if seq not in seqs:
            seqs[seq] = []
        seqs[seq].append(idx)
    return {key: gcd(seqs[key]) for key in seqs if len(seqs[key]) > 1}


def _kasiski(enc, length):
    seqs = get_seqs(enc, length)
    # словарь: возможная длиная ключа -> число последовательностей, которые ее дают
    possible = {}
    for (seq, seq_gcd) in seqs.items():
        if seq_gcd not in possible:
            possible[seq_gcd] = 0
        possible[seq_gcd] += 1
    possible = [(seq_gcd, seq_gcd_count) for (seq_gcd, seq_gcd_count) in possible.items() if seq_gcd_count > 1]
    possible.sort(key=lambda el: el[1])
    return possible


def kasiski(enc, start, end):
    results = [_kasiski(enc, length) for length in range(start, end + 1)]
    for idx, possible in zip(range(start, end + 1), results):
        print('Длина: {:>3} | Возможные длины ключей: {}'.format(idx, list(map(lambda el: el[0], possible))))


def _brute(length, container: list, idx_cur):
    free = [idx for idx in range(length) if idx not in container + [idx_cur, 0]]
    for idx_next in free:
        container[idx_cur] = idx_next
        if container.count(None) > 1:
            yield from _brute(length, container, idx_next)
        else:
            container[idx_next] = 0
            if not check_mono_key(container):
                print('ОШИБКА: неверно сгенерирован ключ длины {}: {}'.format(length, str_key(container)))
            yield container
            container[idx_next] = None
    container[idx_cur] = None


def brute(enc):
    length = kasiski(enc)
    if length == 1:
        print('Текст не зашифрован')
        exit(0)
    container = [None] * length
    for key in _brute(length, container, 0):
        print(str_key(key) + '\r', end='')
        dec = decrypt(enc, key)
        if kasiski(dec) < 3:
            print('\nКлюч расшифрования: {}'.format(str_key(key)))
            return key, dec
    print('Невозможно расшифровать')
    return None, None


def main():
    op = argv[1]

    if op == 'gen':
        length = int(argv[2])
        generate_key(length)
    elif op == 'enc':
        msg = read(argv[2])
        key = read_key(read(argv[3]))
        enc = encrypt(msg, key)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2])
        key = read_key(read(argv[3]))
        dec = decrypt(enc, key)
        write('dec.txt', dec)
    elif op == 'kas':
        enc, _ = read_text(argv[2])
        print('Количество символов: {}'.format(len(enc)))
        start, end = int(argv[3]), int(argv[4])
        kasiski(enc, start, end)
    elif op == 'brute':
        enc, symbols = read_text(argv[2])
        _, dec = brute(enc)
        if dec is not None:
            write_text('bruted.txt', dec, symbols)
    else:
        print('ОШИБКА: неверная операция')


if __name__ == '__main__':
    main()
