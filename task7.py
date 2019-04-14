from itertools import product

from utils import *
from cyphers import Vigenere as Vig, get_freqs, str_freqs, read_freqs, Replacement as Rep


def _get_meindex(seq1, seq2, alph):
    seq1 = ''.join(filter(lambda x: x in alph, seq1))
    seq2 = ''.join(filter(lambda x: x in alph, seq2))
    meindex = sum(seq1.count(letter) * seq2.count(letter) for letter in alph) / len(seq1) / len(seq2)
    return meindex * 100


def attack(enc, freqs, alph, length):
    ys = [[enc[i] for i in range(len(enc)) if i % length == idx and enc[i] in alph] for idx in range(length)]
    ys = [''.join(yi) for yi in ys]

    good_deltas = []
    for idx_delta in range(1, length):
        deltas = [Vig.decrypt(ys[idx_delta], alph, letter) for letter in alph]
        meindices = [_get_meindex(ys[0], delta, alph) for delta in deltas]
        max_meindex, min_meindex = max(meindices), min(meindices)
        lower_meindex = min_meindex + (max_meindex - min_meindex) * 0.75
        candidates = [idx for idx, meindex in enumerate(meindices) if meindex >= lower_meindex]
        good_deltas.append(''.join(map(lambda x: alph[x], candidates)))

    k0s = Rep.attack_shift(freqs, read_freqs(str_freqs(get_freqs(ys[0], alph))), alph, 3)[1:]
    keys = []
    for k0 in k0s:
        k0 = int(k0)
        for comb in product(*good_deltas):
            keys.append(alph[k0] + ''.join(map(lambda x: alph[(k0 + alph.index(x)) % len(alph)], comb)))
    return keys


def main():
    op = argv[1]

    if op == 'enc':
        msg = read(argv[2]).lower()
        key = read_text(argv[3])[0]
        alph = read(argv[4])
        enc = Vig.encrypt(msg.lower(), alph, key)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2])
        key = read(argv[3])
        alph = read(argv[4])
        dec = Vig.decrypt(enc, alph, key)
        write('dec.txt', dec)
    elif op == 'freq':
        text = read(argv[2]).lower()
        alph = read(argv[3])
        write(argv[4], str_freqs(get_freqs(text, alph)))
    elif op == 'attack':
        enc = read(argv[2])
        alph = read(argv[3])
        freqs = read_freqs(read(argv[4]))
        length = int(argv[5])
        keys = attack(enc, freqs, alph, length)
        write('keys.txt', '\n'.join(keys))
    elif op == 'brute':
        enc = read(argv[2])
        keys = read(argv[3]).split('\n')
        alph = read(argv[4])
        f = get_file_write('bruted.txt')
        for key in keys:
            f.write('КЛЮЧ : {}\n{}\n\n'.format(key, Vig.decrypt(enc, alph, key)))
            f.write('-------------------------------\n')
        f.close()
    else:
        print('ОШИБКА: неверный код операции')


if __name__ == '__main__':
    main()
