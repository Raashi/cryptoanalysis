from utils import *
from cyphers import Replacement as Rep, frequencies


def main():
    op = argv[1]

    if op == 'gen':
        alph = read(argv[2])
        write('key.txt', Rep.gen(alph))
    elif op == 'enc':
        msg = read(argv[2]).lower()
        key = read(argv[3])
        alph = read(argv[4])
        enc = Rep.encrypt(msg, key, alph)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2]).lower()
        key = read(argv[3])
        alph = read(argv[4])
        dec = Rep.decrypt(enc, key, alph)
        write('dec.txt', dec)
    elif op == 'freq':
        text = read(argv[2]).lower()
        alph = read(argv[3])
        freqs = frequencies(text, alph)
        freqs = map(lambda pair: '{} : {:.4f}'.format(*pair), freqs)
        write(argv[4], '\n'.join(freqs))
    elif op == 'attack':
        freq_true = map(lambda pair: pair.split(':'), read(argv[2]).split('\n'))
        freq_true = [(k[0], v) for k, v in freq_true]

        freq_enc = map(lambda pair: pair.split(':'), read(argv[3]).split('\n'))
        freq_enc = [(k[0], v) for k, v in freq_enc]
        res = Rep.images(freq_true, freq_enc, int(argv[4]) if len(argv) > 4 else 3)
        write('keys.txt', '\n'.join(res))
    elif op == 'brute':
        enc = read(argv[2])
        keys = read(argv[3]).split('\n')
        alph = read(argv[4])
        f = get_file_write('bruted.txt')
        for key in keys:
            f.write('КЛЮЧ : {}\n{}\n\n'.format(key, Rep.decrypt(enc, key, alph)))
        f.close()
    else:
        print('ОШИБКА: неверный код операции')


if __name__ == '__main__':
    main()
