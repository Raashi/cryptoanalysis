from random import randint

from utils import *
from cyphers import Replacement as Rep, frequencies, read_frequencies, str_frequencies


def main():
    op = argv[1]

    if op == 'genp':
        alph = read(argv[2])
        write('key.txt', alph + '\n' + Rep.gen(alph))
    elif op == 'gens':
        alph = read(argv[2])
        write('key.txt', alph + '\n' + str(randint(1, len(alph) - 1)))
    elif op == 'enc':
        msg = read(argv[2]).lower()
        alph, key = read(argv[3]).split('\n')
        enc = Rep.encrypt(msg, key, alph)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2]).lower()
        alph, key = read(argv[3]).split('\n')
        dec = Rep.decrypt(enc, key, alph)
        write('dec.txt', dec)
    elif op == 'freq':
        text = read(argv[2]).lower()
        alph = read(argv[3])
        freqs = frequencies(text, alph)
        write(argv[4], str_frequencies(freqs))
    elif op == 'a-perm':
        freq_true = read_frequencies(read(argv[2]))
        freq_enc = read_frequencies(read(argv[3]))
        precision = int(argv[4]) if len(argv) > 4 else 3

        res = Rep.images(freq_true, freq_enc, precision)
        write('keys.txt', '\n'.join(res))
    elif op == 'a-sh':
        freq_true = read_frequencies(read(argv[2]))
        freq_enc = read_frequencies(read(argv[3]))
        alph = read(argv[4])
        prec = int(argv[5]) if len(argv) > 5 else 5

        keys = Rep.attack_shift(freq_true, freq_enc, alph, prec)
        write('keys.txt', '\n'.join(keys))
    elif op == 'brute':
        enc = read(argv[2])
        keys = read(argv[3]).split('\n')
        alph, keys = keys[0], keys[1:]
        f = get_file_write('bruted.txt')
        for key in keys:
            f.write('КЛЮЧ : {}\n{}\n\n'.format(key, Rep.decrypt(enc, key, alph)))
            f.write('-------------------------------\n')
        f.close()
    else:
        print('ОШИБКА: неверный код операции')


if __name__ == '__main__':
    main()
