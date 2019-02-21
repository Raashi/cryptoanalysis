from os import listdir
from os.path import dirname, join
from sys import path

from random import randint, choice

currentdir = dirname(__file__)
path.insert(0, dirname(currentdir))

from utils import read_text


def get_random_seq(alph, length):
    return ''.join(choice(alph) for _ in range(length))


def get_random_piece(lang, length):
    # выбираем книгу
    directory = join(currentdir, lang)
    book = join(directory, choice(listdir(directory)))
    content = read_text(book)[0].lower()
    # выбираем отрезок книги
    pos_begin = randint(0, len(content) - length - 1)
    pos_end = pos_begin + length
    return content[pos_begin: pos_end]
