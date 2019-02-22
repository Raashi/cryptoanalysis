"""
usage:
%user%:> python kasiski.py gen 4
%user%:> python kasiski.py enc test.txt 2,4,1,3
%user%:> python kasiski.py dec enc.txt 2,4,1,3
%user%:> python kasiski.py kas enc.txt
"""
from sys import argv, exit
from random import choice

from utils import read_text, write_text, alph_rus, gcd


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


def find_seqs(enc, length) -> list:
    seqs = {}
    for idx in range(len(enc) - length):
        seq = enc[idx: idx + length]
        if seq not in seqs:
            seqs[seq] = []
        seqs[seq].append(idx)
    # отсекаем единичные вхождения, считаем нод
    res = [(key, seqs[key], gcd(seqs[key])) for key in filter(lambda k: len(seqs[k]) > 1, seqs)]
    # отсекаем НОД == 1
    res = list(filter(lambda el: el[2] != 1, res))
    if not len(res):
        return []
    # находим максимальное количество вхождений
    max_entry = max(map(lambda el: len(el[1]), res))
    # отсекаем строки, которые входили более чем max_entry/2 раз
    res = list(filter(lambda el: len(el[1]) > max_entry // 2, res))
    # сортируем по числу вхождений
    res.sort(key=lambda el: len(el[1]), reverse=True)
    return res


def _kasiski(enc, length):
    seqs = find_seqs(enc, length)
    if not seqs:
        return 1
    # словарь: возможная длиная ключа -> число последовательностей, которые ее дают | число вхождений, которые ее дают
    possible = {}
    for (key, seq, seq_gcd) in reversed(seqs):
        if seq_gcd not in possible:
            possible[seq_gcd] = [0, 0]
        possible[seq_gcd][0] += 1
        possible[seq_gcd][1] += len(seq)
    if argv[1] == 'kas' and '-v' in argv:
        print('Анализ для последовательностей длины {}'.format(length))
        for (entry, (seq_count, seq_amount)) in sorted(possible.items(), key=lambda el: el[0]):
            print('Длина: {:>3} | Число строк: {:>3} | Число вхождений: {}'.format(entry, seq_count, seq_amount))
    max_entries = max(map(lambda el: el[1], possible.values()))
    for entry in possible:
        if possible[entry][1] == max_entries:
            return entry


def kasiski(enc):
    start = 3
    end = 10
    results = [_kasiski(enc, length) for length in range(start, end + 1)]
    # возможная длина ключа | количество длин последовательностей, дающих такую длину
    entries = [(length, results.count(length)) for length in set(results)]
    entries.sort(reverse=True, key=lambda el: el[1])
    return entries[0][0]


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
    if length < 3:
        print('Текст не зашифрован, либо зашиифрован тривиальным ключом 2,1. Смотри bruted.txt')
        return [1, 0], decrypt(enc, [1, 0])
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
        print('Количество символов: {}'.format(len(enc)))
        length = kasiski(enc)
        print('Длина ключа: {}'.format(length))
    elif op == 'brute':
        enc, symbols = read_text(argv[2])
        _, dec = brute(enc)
        if dec is not None:
            write_text('bruted.txt', dec, symbols)
    else:
        print('ОШИБКА: неверная операция')


if __name__ == '__main__':
    main()
