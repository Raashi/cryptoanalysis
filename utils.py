from sys import argv
from os import mkdir
from os.path import basename, exists, join

DIR_MODULE = '_' + basename(argv[0])[:-3]

rus_alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
eng_alph = 'abcdefghijklmnopqrstuvwxyz'


if not exists(DIR_MODULE):
    mkdir(DIR_MODULE)


def _resolve_path(fn):
    path = join(DIR_MODULE, fn)
    if not exists(path):
        path = fn
    return path


def read(fn):
    with open(_resolve_path(fn)) as f:
        return f.read()


def write(fn, content):
    with open(join(DIR_MODULE, fn), 'w') as f:
        f.write(content)


def read_text(fn):
    content = read(fn)
    next_lines = []
    res = ''
    for idx, c in enumerate(content):
        # if c == '\n':
        if not c.isalpha():
            next_lines.append((idx, c))
        else:
            res += c
    return res, next_lines


def write_text(fn, content, next_lines):
    for idx, c in next_lines:
        content = content[:idx] + c + content[idx:]
    write(fn, content)
