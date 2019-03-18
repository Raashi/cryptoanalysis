# usage: %user%> samples/shrink.py samples
from os import listdir
from os.path import join, isdir
from sys import argv

ralph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
ralph += ralph.upper()
ealph = 'abcdefghijklmnopqrstuvwxyz'
ealph += ealph.upper()


def process(file):
    print('PROCESSING: {}'.format(file))
    with open(file, encoding='utf-8') as f:
        lines = f.readlines()
    lines = list(map(lambda line: line.strip() + '\n', lines))
    for idx, line in enumerate(lines):
        new_line = line[0]
        for c in line[1:]:
            if c == ' ' and new_line[-1] == ' ':
                continue
            new_line += c

        alph = ralph if 'eng' in file else ealph
        new_line = ''.join(filter(lambda c: c not in alph, new_line))
        lines[idx] = new_line
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(filter(lambda el: len(el.strip()), lines))


def scan(directory):
    for entry in listdir(directory):
        path = join(directory, entry)
        if entry[-3:] == 'txt':
            process(path)
        elif isdir(path):
            scan(path)


def main():
    scan(argv[1])


if __name__ == '__main__':
    main()
