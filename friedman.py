"""
usage:
%user%:> python friedman.py gen 100

%user%:> python friedman.py eindex table.txt
%user%:> python friedman.py meindex table.txt

%user%:> python friedman.py enc text_rus.txt alph_rus.txt key_rus.txt
%user%:> python friedman.py dec enc.txt alph_rus.txt key_rus.txt

%user%:> python friedman.py enc text_eng.txt alph_eng.txt key_eng.txt
%user%:> python friedman.py dec enc.txt alph_eng.txt key_eng.txt

%user%:> python friedman.py analyze text_eng.txt alph_eng.txt key_eng.txt key_eng_7.txt
%user%:> python friedman.py analyze text_rus.txt alph_rus.txt key_rus.txt key_rus_7.txt
"""
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


def _eindex(seq1, seq2):
    return reduce(lambda acc, els: acc + int(els[0] == els[1]), zip(seq1, seq2), 0) / len(seq1) * 100


def eindex(fn1, fn2):
    text1 = read(fn1).strip().lower()
    text2 = read(fn2).strip().lower()
    res = _eindex(text1, text2)
    print('Индекс вопадения: {}'.format(res))


def _meindex(seq1, seq2, alph):
    length = min(len(seq1), len(seq2))
    seq1, seq2 = seq1[:length], seq2[:length]
    return sum(seq1.count(letter) * seq2.count(letter) * (length ** -2) for letter in alph) * 100


def meindex(fn1, fn2, fn_alph):
    text1 = read(fn1).strip().lower()
    text2 = read(fn2).strip().lower()
    alph = read(fn_alph).strip()
    res = _meindex(text1, text2, alph)
    print('Средний индекс совпадения: {}'.format(res))


def encrypt(msg: str, alph: str, key: str):
    enc = ''
    for idx, char in enumerate(msg):
        enc += alph[(alph.index(char) + alph.index(key[idx % len(key)])) % len(alph)]
    return enc


def decrypt(enc: str, alph: str, key: str):
    dec = ''
    for idx, char in enumerate(enc):
        dec += alph[(alph.index(char) - alph.index(key[idx % len(key)])) % len(alph)]
    return dec


def analyze(msg: str, alph: str, key_5: str, key_7: str):
    enc_5 = encrypt(msg, alph, key_5)
    enc_7 = encrypt(msg, alph, key_7)
    results = {'orig': [], '5': [], '7': []}
    for shift in range(1, 16):
        msg_shifted = msg[shift:] + msg[:shift]
        enc_5_shifted = enc_5[shift:] + enc_5[:shift]
        enc_7_shifted = enc_7[shift:] + enc_7[:shift]
        results['orig'].append(_eindex(msg, msg_shifted))
        results['5'].append(_eindex(enc_5, enc_5_shifted))
        results['7'].append(_eindex(enc_7, enc_7_shifted))
    results = [results['orig'], results['5'], results['7']]
    titles = ['I(y,y(+l))×100 для открытого',
              'I(y,y(+l))×100 для шифрограммы, k=5',
              'I(y,y(+l))×100 для шифрограммы, k=7']
    columns = [''] + [str(shift) for shift in range(1, 16)]
    write_answers(results, titles, columns)


def main():
    op = argv[1]

    if op == 'gen':
        gen_samples(100 if len(argv) < 3 else int(argv[2]))
    elif op == 'eindex':
        eindex(argv[2], argv[3])
    elif op == 'meindex':
        meindex(argv[2])
    elif op == 'enc':
        msg, symbols = read_text(argv[2])
        alph = read_text(argv[3])[0]
        key = read_text(argv[4])[0]
        enc = encrypt(msg.lower(), alph, key)
        write_text('enc.txt', enc, symbols)
    elif op == 'dec':
        enc, symbols = read_text(argv[2])
        alph = read_text(argv[3])[0]
        key = read_text(argv[4])[0]
        dec = decrypt(enc, alph, key)
        write_text('dec.txt', dec, symbols)
    elif op == 'analyze':
        msg = read_text(argv[2])[0]
        msg = msg[:100]
        msg = msg.lower()
        if len(msg) != 100:
            print('ОШИБКА: текст должен быть длиной 100 символов и более')
        alph = read_text(argv[3])[0]
        key_5 = read_text(argv[4])[0]
        key_7 = read_text(argv[5])[0]
        analyze(msg, alph, key_5, key_7)
    else:
        print('ОШИБКА: неверный код операции')


if __name__ == '__main__':
    main()
