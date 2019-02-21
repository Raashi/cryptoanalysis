# usage: %user%:> python friedman.py gen [length]
#        %user%:> python friedman.py eindex filename
from sys import argv
from os.path import join, exists
from functools import reduce

from samples.sample import get_random_seq, get_random_piece
from utils import DIR_MODULE, rus_alph, eng_alph, read, write


TEST_FILENAME = 'test.txt'
TEST_FILENAME_BACKUP = 'test_old.txt'


def handle_backup():
    path_old = join(DIR_MODULE, TEST_FILENAME)
    if exists(path_old):
        write(TEST_FILENAME_BACKUP, read(path_old))


def gen_samples(length):
    handle_backup()

    ftest = open(join(DIR_MODULE, TEST_FILENAME), 'w', encoding='utf-8')
    # случайная - русский
    for _ in range(2):
        ftest.write(get_random_seq(rus_alph, length) + '\n')
        ftest.write(get_random_seq(rus_alph, length) + '\n')
    # случайная - английский
    for _ in range(2):
        ftest.write(get_random_seq(eng_alph, length) + '\n')
        ftest.write(get_random_seq(eng_alph, length) + '\n')
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


def write_answers(results, titles):
    precision = 3
    align = max(map(lambda title: len(title), titles)) + 4
    print('{}    {:<{align}} {:<{align}} {:<{align}}'.format(' ' * 8, *titles, align=align))
    for idx in range(4):
        print('Пример {}    {:<{align}} {:<{align}} {:<{align}}'
              .format(idx, round(results[0][idx], precision),
                      round(results[1][idx], precision),
                      round(results[2][idx], precision), align=align))


def _eindex(seq1, seq2):
    return reduce(lambda acc, els: acc + int(els[0] == els[1]), zip(seq1, seq2), 0) / len(seq1)


def eindex(fn):
    samples = read_samples(fn)
    results = {key: [_eindex(sample[0], sample[1]) for sample in samples[key]] for key in samples}
    results = [results['rand'], results['eng'], results['rus']]
    write_answers(results, ['I(y,z)×100 случ', 'I(y,z)×100 англ', 'I(y,z)×100 рус'])


def _meindex(seq1, seq2):
    length = len(seq1)
    alph = rus_alph if any(seq1.count(letter) for letter in rus_alph) else eng_alph
    return sum(seq1.count(letter) * seq2.count(letter) * (length ** -2) for letter in alph)


def meindex(fn):
    samples = read_samples(fn)
    results = {key: [_meindex(sample[0], sample[1]) for sample in samples[key]] for key in samples}
    results = [results['rand'], results['eng'], results['rus']]
    write_answers(results, ['Iср(y,z)×100 случ', 'Iср(y,z)×100 англ', 'Iср(y,z)×100 рус'])


def main():
    op = argv[1]

    if op == 'gen':
        gen_samples(100 if len(argv) < 3 else int(argv[2]))
    elif op == 'eindex':
        eindex(argv[2])
    elif op == 'meindex':
        meindex(argv[2])
    else:
        print('ОШИБКА: неверный код операции')


if __name__ == '__main__':
    main()
