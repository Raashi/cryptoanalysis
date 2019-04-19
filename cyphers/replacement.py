from random import shuffle
from itertools import permutations

from utils import argv, read, write

PRECISION = 3


def gen(alph):
    key = list(alph)
    shuffle(key)
    return ''.join(key)


def handle_key(key, alph):
    try:
        key = int(key)
        key = alph[key:] + alph[:key]
    except ValueError:
        pass
    return key


def encrypt(msg, key, alph):
    key = handle_key(key, alph)
    return ''.join(map(lambda c: key[alph.index(c)] if c in alph else c, msg))


def decrypt(enc, key, alph):
    key = handle_key(key, alph)
    return ''.join(map(lambda c: alph[key.index(c)] if c in alph else c, enc))


def attack_shift(freq_true, freq_enc, alph, precision):
    keys = images(freq_true, freq_enc, precision)
    shifts = {}
    for key in keys:
        key = ''.join(sorted(key, key=lambda x: alph.index(freq_true[key.index(x)][0])))
        for idx, letter in enumerate(key):
            shift = (alph.index(letter) - idx) % len(alph)
            shifts[shift] = shifts.get(shift, 0) + 1
    # берем только самые большие по количеству смещения
    min_count, max_count = min(shifts.values()), max(shifts.values())
    border_value = min_count + (max_count - min_count) * 0.5
    shifts = {shift: count for shift, count in shifts.items() if count > border_value}
    shifts = list(sorted(shifts.keys(), key=lambda x: shifts[x], reverse=True))
    return [alph] + list(map(str, shifts[:3]))


def brute(groups, idx, cont):
    if idx == len(groups):
        yield cont
        return
    for perm in permutations(groups[idx]):
        cont.extend(perm)
        yield from brute(groups, idx + 1, cont)
        for _ in range(len(perm)):
            cont.pop()


def images(freq_true, freq_enc, precision):
    freq_true = ''.join(map(lambda pair: pair[0], freq_true))

    for idx, (letter, freq) in enumerate(freq_enc):
        freq_new = freq[:2] + freq[2:2 + precision + 1]
        freq_enc[idx] = (letter, freq_new)

    groups = []
    while len(freq_enc):
        groups.append([freq_enc[0][0]])
        value = freq_enc[0][1]
        freq_enc = freq_enc[1:]
        while len(freq_enc) and freq_enc[0][1] == value and float(value) > 0:
            groups[-1].append(freq_enc[0][0])
            freq_enc = freq_enc[1:]

    res = [''.join(map(lambda pair: pair[0], freq_true))]
    for key in brute(groups, 0, []):
        res.append(''.join(key))
        if len(res) > 1000:
            break
    return res


def exec_encrypt():
    msg = read(argv[2]).lower()
    alph, key = read(argv[3]).split('\n')
    enc = encrypt(msg, key, alph)
    write('enc.txt', enc)


def exec_decrypt():
    enc = read(argv[2]).lower()
    alph, key = read(argv[3]).split('\n')
    dec = decrypt(enc, key, alph)
    write('dec.txt', dec)
