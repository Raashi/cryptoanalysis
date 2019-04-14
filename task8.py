from random import choice

from utils import *
from cyphers import Vigenere as Vig


def get_freqs_bigrams(text, alph):
    count = 0
    matrix = [[0] * len(alph) for _ in range(len(alph))]
    for idx in range(len(text) - 1):
        char_cur, char_next = text[idx], text[idx + 1]
        if char_cur not in alph or char_next not in alph:
            continue
        count += 1
        matrix[alph.index(char_cur)][alph.index(char_next)] += 1
    matrix = [[el / count for el in row] for row in matrix]
    return matrix


def str_freqs_bigrams(text, alph):
    matrix = get_freqs_bigrams(text, alph)
    for idx_row, row in enumerate(matrix):
        for idx, el in enumerate(row):
            row[idx] = '{:.6f}'.format(el)
        matrix[idx_row] = ' '.join(row)
    return matrix


def get_w(mat1, mat2):
    res = 0
    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
            res += abs(mat1[i][j] - mat2[i][j])
    return res


def attack(enc, alph, bi, length):
    key0 = ''.join(choice(alph) for _ in range(length))
    key = ''
    while key != key0:
        key = key0
        dec = Vig.decrypt(enc, alph, key)
        bi_dec = get_freqs_bigrams(dec, alph)
        wk = get_w(bi_dec, bi)
        print(wk)

        key0 = key
        for idx_ki in range(length):
            wks_ki = []
            for letter in alph:
                key_ki = key0[:idx_ki] + letter + key0[idx_ki + 1:]
                dec_ki = Vig.decrypt(enc, alph, key_ki)
                wk_ki = get_w(get_freqs_bigrams(dec_ki, alph), bi)
                wks_ki.append(wk_ki)
            wk_ki_min = min(wks_ki)
            if wk_ki_min <= wk:
                ki_true = alph[wks_ki.index(wk_ki_min)]
                key0 = key0[:idx_ki] + ki_true + key0[idx_ki + 1:]
        print(key0)
    return key


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
    elif op == 'bi':
        text = read(argv[2]).lower()
        alph = read(argv[3])
        write('bi.txt', '\n'.join(str_freqs_bigrams(text, alph)))
    elif op == 'attack':
        enc = read(argv[2])
        alph = read(argv[3])
        bi = read(argv[4]).split('\n')
        bi = [[float(el) for el in row.split(' ')] for row in bi]
        length = int(argv[5])
        key = attack(enc, alph, bi, length)
        print(key)
        # write('keys.txt', '\n'.join(keys))
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

# key0 = ''
# for idx_ki in range(length):
#     wks_ki = []
#     for letter in alph:
#         key_ki = key[:idx_ki] + letter + key[idx_ki + 1:]
#         dec_ki = Vig.decrypt(enc, alph, key_ki)
#         wk_ki = get_w(get_freqs_bigrams(dec_ki, alph), bi)
#         wks_ki.append(wk_ki)
#     wk_ki_min = min(wks_ki)
#     if wk_ki_min <= wk:
#         ki_true = alph[wks_ki.index(wk_ki_min)]
#         key0 += ki_true
#     else:
#         key0 += key[idx_ki]
# print(key0)
