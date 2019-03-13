import json

from utils import *
from cyphers import Permutations as Perms

SPACER = '   '


def get_banned_bigrams(text):
    idx = 0
    words = []
    while idx < len(text):
        start = idx
        while text[idx].isalpha():
            idx += 1
        if idx > start:
            words.append(text[start:idx])
        else:
            idx += 1
    alph = set()
    bigrams = set()
    for word in words:
        for char, char_next in zip(word[:-1], word[1:]):
            alph.add(char)
            alph.add(char_next)
            bigrams.add(char + char_next)
    banned = [a + b for a in alph for b in alph if (a + b) not in bigrams]
    banned.sort()
    alph = ''.join(sorted(alph))
    return alph, banned


def get_table(enc, banned, length):
    blocks = []
    for block_idx in range(0, len(enc), length):
        blocks.append(enc[block_idx:block_idx + length])

    table = [[True] * length for _ in range(length)]
    for col_l in range(length):
        for col_r in range(length):
            if col_l == col_r:
                table[col_l][col_r] = False
                continue
            for b in blocks:
                cl, cr = b[col_l], b[col_r]
                if not cl.isalpha() or not cr.isalpha():
                    continue
                bigram = cl + cr
                if bigram in banned:
                    table[col_l][col_r] = False
                    break
            else:
                table[col_l][col_r] = True
    return table


def _get_tree(table, row, k, depth, used: set):
    if depth == k:
        return {}

    if depth == k - 1:
        res = {}
        for col in range(k):
            if table[row][col] and col not in used:
                res[col + 1] = {}
        return res

    res = {}
    for col in range(k):
        if table[row][col] and col not in used:
            used.add(col)
            sub_node = _get_tree(table, col, k, depth + 1, used)
            used.remove(col)
            if sub_node:
                res[col + 1] = sub_node
    return res


def get_tree(table):
    k = len(table)
    col_trues = [[table[row][col] for row in range(k)].count(True) for col in range(k)]
    cols = [idx for idx in range(k)]
    cols.sort(key=lambda col: col_trues[col])

    tree = {start + 1: _get_tree(table, start, k, 1, {start}) for start in cols}
    tree = {key: value for (key, value) in tree.items() if value}
    tree["length"] = k
    return tree


def _display_tree(node, lines, depth):
    for vertex in node:
        lines.append((SPACER * depth) + str(vertex))
        _display_tree(node[vertex], lines, depth + 1)


def display_tree(tree: dict):
    lines = []
    for start in tree:
        lines.append(str(start))
        _display_tree(tree[start], lines, 1)
    return lines


def read_tree(tree):
    pass


def _brute(node, k, container):
    for vertex in node:
        container.append(int(vertex) - 1)
        if len(container) == k:
            yield container
        else:
            yield from _brute(node[vertex], k, container)
        container.pop()


def brute(enc, tree):
    k = tree["length"]
    del tree["length"]

    f = get_file_write("bruted.txt")
    for key in _brute(tree, k, []):
        print(Perms.str_key(key) + '\r', end='')
        dec = Perms.decrypt(enc, key)
        f.write(Perms.str_key(key) + '\n')
        f.write(dec + '\n\n')
    f.close()


def main():
    op = argv[1]

    if op == 'bigram':
        text = read(argv[2]).lower()
        alph, banned = get_banned_bigrams(text)
        write('alph.txt', alph)
        write('banned.txt', '\n'.join(banned))
    elif op == 'enc':
        msg = read(argv[2])
        key = Perms.read_key(argv[3])
        # msg = msg[:(len(msg) // len(key)) * len(key)]
        while len(msg) % len(key):
            msg += ' '
        enc = Perms.encrypt(msg, key)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2])
        key = Perms.read_key(argv[3])
        dec = Perms.decrypt(enc, key)
        write('dec.txt', dec)
    elif op == 'table':
        enc = read(argv[2]).lower()
        banned = read(argv[3]).split('\n')
        length = int(argv[4])
        table = get_table(enc, banned, length)
        write('table.txt', '\n'.join(map(lambda x: ' '.join(map(lambda x: str(int(x)), x)), table)))
    elif op == 'tree':
        table = read(argv[2]).split('\n')
        for idx, row in enumerate(table):
            table[idx] = list(map(lambda x: bool(int(x)), row.split(' ')))
        tree = get_tree(table)
        # disp_tree = '\n'.join(display_tree(tree))
        write('tree.txt', json.dumps(tree, indent=4))
    elif op == 'brute':
        enc = read(argv[2])
        tree = json.loads(read(argv[3]))
        brute(enc, tree)
    else:
        print('ОШИБКА: неверная операция')


if __name__ == '__main__':
    main()
