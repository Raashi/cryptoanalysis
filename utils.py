from sys import argv
from os import mkdir
from os.path import basename, exists, join, dirname

from math import gcd as _gcd


if __name__ != '__main__' and dirname(__file__) == dirname(argv[0]):
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
    with open(_resolve_path(fn), encoding='utf-8') as f:
        return f.read()


def write(fn, content, root=False):
    path = join(DIR_MODULE, fn) if not root else fn
    with open(path, 'w', encoding='utf-8') as f:
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


#    MATHEMATICS


def gcd(a, *other):
    if hasattr(a, '__iter__') or hasattr(a, '__next__'):
        container = list(a)
    else:
        container = [a] + list(other)
    res = container[0]
    for b in container[1:]:
        res = _gcd(res, b)
    return res


if __name__ == '__main__':
    pass
