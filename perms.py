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
        return {}, True
    res = {}
    for col in range(k):
        if table[row][col] and col not in used:
            used.add(col)
            sub_node, rr = _get_tree(table, col, k, depth + 1, used)
            used.remove(col)
            if sub_node or rr:
                res[col] = sub_node
    return res, False
    # return {col: _get_tree(table, col, k, depth + 1) for col in range(k) if table[row][col]}


def get_tree(table):
    k = len(table)
    col_trues = [[table[row][col] for row in range(k)].count(True) for col in range(k)]
    cols = [idx for idx in range(k) if col_trues[idx]]
    cols.sort(key=lambda col: col_trues[col], reverse=True)

    tree = {start: _get_tree(table, start, k, 1, {start})[0] for start in cols}
    tree = {key: value for (key, value) in tree.items() if value}
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
        msg = msg[:(len(msg) // len(key)) * len(key)]
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
        write('tree.txt', '\n'.join(display_tree(tree)))
    else:
        print('ОШИБКА: неверная операция')


if __name__ == '__main__':
    main()
