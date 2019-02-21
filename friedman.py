from sys import argv
from random import choice

from utils import rus_alph, eng_alph


def read_tests():
    pass


def write_answers():
    pass


def eindex():
    pass


def main():
    op = argv[1]

    if op == 'eindex':
        eindex()


if __name__ == '__main__':
    with open('tests.txt', 'w') as f:
        # пример 1
        f.write(''.join(choice(rus_alph) for _idx in range(100)) + '\n')
        f.write(''.join(choice(rus_alph) for _idx in range(100)) + '\n')
        # пример 2
        f.write(''.join(choice(rus_alph) for _idx in range(100)) + '\n')
        f.write(''.join(choice(rus_alph) for _idx in range(100)) + '\n')
        # пример 3
        f.write(''.join(choice(eng_alph) for _idx in range(100)) + '\n')
        f.write(''.join(choice(eng_alph) for _idx in range(100)) + '\n')
        # пример 4
        f.write(''.join(choice(eng_alph) for _idx in range(100)) + '\n')
        f.write(''.join(choice(eng_alph) for _idx in range(100)) + '\n')
