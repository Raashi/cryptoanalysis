from sys import argv
from os.path import join, exists

from samples.sample import get_random_seq, get_random_piece
from utils import DIR_MODULE, rus_alph, eng_alph, read, write


TEST_FILENAME = 'test.txt'
TEST_FILENAME_BACKUP = 'test_old.txt'


def handle_backup():
    path_old = join(DIR_MODULE, TEST_FILENAME)
    if exists(path_old):
        path_backup = join(DIR_MODULE, TEST_FILENAME_BACKUP)
        write(path_backup, read(path_old))


def gen_sample(length):
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


def read_sample(fn):
    fsamples = open(fn, encoding='utf-8')
    samples = list(filter(lambda row: len(row.strip()), fsamples.readlines()))
    return {
        'rand': [samples[0:2], samples[2:4], samples[6:8], samples[8:10]],
        'rus': [samples[10:12], samples[12:14], samples[14:16], samples[16:18]],
        'eng': [samples[18:20], samples[20:22], samples[22:24], samples[24:26]]
    }


def write_answers():
    pass


def eindex():
    pass


def main():
    op = argv[1]

    if op == 'eindex':
        eindex()


if __name__ == '__main__':
    main()
