"""
usage:
%user%:> python friedman.py rus/alph.txt 100 seq1.txt
%user%:> python friedman.py eng/alph.txt 100 seq2.txt

%user%:> python friedman.py eindex seq1.txt seq2.txt
%user%:> python friedman.py meindex seq1.txt seq2.txt

%user%:> python friedman.py enc rus/t1.txt rus/alph.txt key.txt
%user%:> python friedman.py dec enc.txt rus/alph.txt key.txt

%user%:> python friedman.py analyze enc.txt
"""
from random import choice
from functools import reduce

from samples.sample import get_random_seq, get_random_piece
from utils import *


TEST_FILENAME = 'table.txt'


def gen_samples(length):
    ftest = open(join(DIR_MODULE, TEST_FILENAME), 'w', encoding='utf-8')
    # случайная - русский
    for _ in range(2):
        ftest.write(get_random_seq(alph_rus, length) + '\n')
        ftest.write(get_random_seq(alph_rus, length) + '\n')
    # случайная - английский
    for _ in range(2):
        ftest.write(get_random_seq(alph_eng, length) + '\n')
        ftest.write(get_random_seq(alph_eng, length) + '\n')
    ftest.write('\n')

    # русский
    for _ in range(4):
        ftest.write(get_random_piece('rus', length) + '\n')
        ftest.write(get_random_piece('rus', length) + '\n')
    ftest.write('\n')

    # английский
    for _ in range(4):
        ftest.write(get_random_piece('eng', length) + '\n')
        ftest.write(get_random_piece('eng', length) + '\n')
    ftest.close()


def read_samples(fn):
    lines = read(fn).split('\n')
    samples = list(filter(lambda row: len(row.strip()), lines))
    return {
        'rand': [samples[0:2], samples[2:4], samples[4:6], samples[6:8]],
        'rus': [samples[8:10], samples[10:12], samples[12:14], samples[14:16]],
        'eng': [samples[16:18], samples[18:20], samples[20:22], samples[22:24]]
    }


def write_answers(results, titles_column, titles_row):
    precision = 3
    space = 4
    align_head = max(map(lambda title: len(title), titles_row)) + space
    align = max(map(lambda title: len(title), titles_column)) + space
    print('{:<{align_head}} {:<{align}} {:<{align}} {:<{align}}'
          .format(titles_row[0], *titles_column, align=align, align_head=align_head))
    for idx in range(len(titles_row) - 1):
        print('{:<{align_head}} {:<{align}} {:<{align}} {:<{align}}'
              .format(titles_row[idx + 1], round(results[0][idx], precision),
                      round(results[1][idx], precision),
                      round(results[2][idx], precision),
                      align=align, align_head=align_head))


def gen_seq(fn_alph, length):
    alph = read(fn_alph)
    return ''.join(choice(alph) for _ in range(length))


def _get_eindex(seq1, seq2):
    length = min(len(seq1), len(seq2))
    seq1, seq2 = seq1[:length], seq2[:length]
    eindex = reduce(lambda acc, els: acc + int(els[0] == els[1]), zip(seq1, seq2), 0) / length
    return eindex * 100


def get_eindex(fn1, fn2):
    text1 = read(fn1).strip().lower()
    text2 = read(fn2).strip().lower()
    eindex = _get_eindex(text1, text2)
    print('Индекс вопадения: {:.2f}'.format(eindex))


def _get_meindex(seq1, seq2, alph):
    length = min(len(seq1), len(seq2))
    seq1, seq2 = seq1[:length], seq2[:length]
    meindex = sum(seq1.count(letter) * seq2.count(letter) for letter in alph) / length / length
    return meindex * 100


def get_meindex(fn1, fn2, fn_alph):
    text1 = read(fn1).strip().lower()
    text2 = read(fn2).strip().lower()
    alph = read(fn_alph).strip()
    res = _get_meindex(text1, text2, alph)
    print('Средний индекс совпадения: {:.2f}'.format(res))


def encrypt(msg, alph, key):
    enc = ''
    for idx, char in enumerate(msg):
        enc += alph[(alph.index(char) + alph.index(key[idx % len(key)])) % len(alph)]
    return enc


def decrypt(enc, alph, key):
    dec = ''
    for idx, char in enumerate(enc):
        dec += alph[(alph.index(char) - alph.index(key[idx % len(key)])) % len(alph)]
    return dec


def analyze(fn):
    msg = read_text(fn)[0].strip().lower()
    for shift in range(1, 16):
        msg_shifted = msg[:shift] + msg[:shift]
        eindex = _get_eindex(msg, msg_shifted)
        print('l = {:>2} | индекс = {:.2f}'.format(shift, eindex))


def main():
    op = argv[1]

    if op == 'gen':
        seq = gen_seq(argv[2], int(argv[3]))
        write(argv[4], seq)
    elif op == 'eindex':
        get_eindex(argv[2], argv[3])
    elif op == 'meindex':
        get_meindex(argv[2], argv[3], argv[4])
    elif op == 'enc':
        msg, symbols = read_text(argv[2])
        alph = read_text(argv[3])[0]
        key = read_text(argv[4])[0]
        enc = encrypt(msg.lower(), alph, key)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read_text(argv[2])[0]
        alph = read(argv[3])
        key = read(argv[4])
        dec = decrypt(enc, alph, key)
        write('dec.txt', dec)
    elif op == 'analyze':
        analyze(argv[2])
    else:
        print('ОШИБКА: неверный код операции')


if __name__ == '__main__':
    main()
