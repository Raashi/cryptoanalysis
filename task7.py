from itertools import product

from utils import *
from cyphers import Vigenere as Vig, get_freqs, write_freqs, read_freqs, Replacement as Rep, exec_freqs


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

    k0s = Rep.attack_shift(freqs, get_freqs(ys[0], alph), alph, 3)[1:]
    keys = []
    for k0 in k0s:
        k0 = int(k0)
        for comb in product(*good_deltas):
            keys.append(alph[k0] + ''.join(map(lambda x: alph[(k0 + alph.index(x)) % len(alph)], comb)))
    return keys


def main():
    if op == 'enc':
        Vig.exec_encrypt()
    elif op == 'dec':
        Vig.exec_decrypt()
    elif op == 'freq':
        exec_freqs()
    elif op == 'attack':
        enc = read(argv[2])
        alph = read(argv[3])
        freqs = read_freqs(argv[4])
        length = int(argv[5])
        keys = attack(enc, freqs, alph, length)
        write('keys.txt', '\n'.join(keys))
    elif op == 'brute':
        Vig.exec_brute()
    else:
        print_wrong_op()


if __name__ == '__main__':
    main()
