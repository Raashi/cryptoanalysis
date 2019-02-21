from sys import argv
from os import mkdir
from os.path import basename, exists, join
from random import randint


if __name__ != '__main__':
    DIR_MODULE = '_' + basename(argv[0])[:-3]

    if not exists(DIR_MODULE):
        mkdir(DIR_MODULE)
else:
    DIR_MODULE = ''

rus_alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
eng_alph = 'abcdefghijklmnopqrstuvwxyz'


def _resolve_path(fn):
    paths = [join(DIR_MODULE, fn), join('tests', fn)]
    for path in paths:
        if exists(path):
            return path
    return fn


def read(fn):
    with open(_resolve_path(fn)) as f:
        return f.read()


def write(fn, content, root=False):
    path = join(DIR_MODULE, fn) if not root else fn
    with open(path, 'w') as f:
        f.write(content)


def read_text(fn):
    content = read(fn)
    next_lines = []
    res = ''
    for idx, c in enumerate(content):
        if not c.isalpha():
            next_lines.append((idx, c))
        else:
            res += c
    return res, next_lines


def write_text(fn, content, next_lines, *args):
    for idx, c in next_lines:
        content = content[:idx] + c + content[idx:]
    write(fn, content, *args)


if __name__ == '__main__':
    fn_dst = argv[2]
    sample_length = 100
    text, _ = read_text(argv[1])
    pos_begin = randint(0, len(text) - sample_length - 1)
    pos_end = pos_begin + sample_length
    with open(fn_dst, 'w') as f:
        f.write(text[pos_begin: pos_end])
