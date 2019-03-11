from utils import *
from cyphers import Permutations as Perms


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
        enc = Perms.encrypt(msg, key)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2])
        key = Perms.read_key(argv[3])
        dec = Perms.decrypt(enc, key)
        write('dec.txt', dec)
    else:
        print('ОШИБКА: неверная операция')


if __name__ == '__main__':
    main()
