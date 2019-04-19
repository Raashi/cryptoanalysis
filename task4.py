from random import randint

from utils import *
from cyphers import read_freqs, exec_freqs
import cyphers.replacement as rep


def main():
    if op == 'genp':
        alph = read(argv[2])
        write('key.txt', alph + '\n' + rep.gen(alph))
    elif op == 'gens':
        alph = read(argv[2])
        write('key.txt', alph + '\n' + str(randint(1, len(alph) - 1)))
    elif op == 'enc':
        rep.exec_encrypt()
    elif op == 'dec':
        rep.exec_decrypt()
    elif op == 'freq':
        exec_freqs()
    elif op == 'a-perm':
        freq_true = read_freqs(argv[2])
        freq_enc = read_freqs(argv[3])
        precision = int(argv[4]) if len(argv) > 4 else 3

        keys = rep.images(freq_true, freq_enc, precision)
        write('keys.txt', '\n'.join(keys))
    elif op == 'a-sh':
        freq_true = read_freqs(argv[2])
        freq_enc = read_freqs(argv[3])
        alph = read(argv[4])
        precision = int(argv[5]) if len(argv) > 5 else 5

        keys = rep.attack_shift(freq_true, freq_enc, alph, precision)
        write('keys.txt', '\n'.join(keys))
    elif op == 'brute':
        enc = read(argv[2])
        keys = read(argv[3]).split('\n')
        alph, keys = keys[0], keys[1:]
        f = get_file_write('bruted.txt')
        for key in keys:
            f.write('КЛЮЧ : {}\n{}\n\n'.format(key, rep.decrypt(enc, key, alph)))
            f.write('-------------------------------\n')
        f.close()
    else:
        print_wrong_op()


if __name__ == '__main__':
    main()
