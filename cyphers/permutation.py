from random import choice

from utils import argv, read, write


def read_key(skey):
    return list(map(lambda el: int(el) - 1, skey.split(',')))


def str_key(key):
    return ','.join(map(lambda el: str(el + 1), key))


def is_monocycle_key(key):
    idx, start, cycle = 0, 0, 1
    while key[idx] != start:
        idx, cycle = key[idx], cycle + 1
    res = cycle == len(key)
    if not res:
        print('ОШИБКА: сгенерированный ключ не моноцикличен:', str_key(key))
    return res


def gen_monocycle_key(length):
    key = [None] * length
    free = [idx for idx in range(1, length)]

    start = idx = 0
    while len(free):
        idx_next = choice(free)
        free.remove(idx_next)
        key[idx] = idx_next
        idx = idx_next
    key[idx] = start

    if not is_monocycle_key(key):
        exit(1)
    print('Сгенерирован ключ длины {}:'.format(length), str_key(key))
    return key


def encrypt(msg, key):
    length = len(key)

    alph_from_msg = list({char for char in msg if char.isalpha()})
    alph_from_msg = alph_from_msg if len(alph_from_msg) else list({char for char in msg})
    while len(msg) % length:
        msg += choice(alph_from_msg)

    enc = ''
    for b in range(len(msg) // length):
        block = msg[b * length: (b + 1) * length]
        enc += ''.join(block[key.index(idx)] for idx in range(length))
    return enc


def decrypt(enc, key):
    length = len(key)

    dec = ''
    for b in range(len(enc) // length):
        block = enc[b * length: (b + 1) * length]
        dec += ''.join(block[el] for el in key)
    return dec


def exec_gen_mono_key():
    length = int(argv[2])
    key = gen_monocycle_key(length)
    write('key.txt', str_key(key))


def exec_encrypt():
    msg = read(argv[2])
    key = read_key(read(argv[3]))
    enc = encrypt(msg, key)
    write('enc.txt', enc)


def exec_decrypt():
    enc = read(argv[2])
    key = read_key(read(argv[3]))
    dec = decrypt(enc, key)
    write('dec.txt', dec)
