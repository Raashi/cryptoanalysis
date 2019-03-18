from itertools import product

from utils import *
from cyphers import Vigenere as Vig, text_to_words


def frequencies(text):
    freqs = {}
    alphas = 0
    for c in text:
        if c.isalpha():
            freqs[c] = freqs.get(c, 0) + 1
            alphas += 1

    for alpha, count in freqs.items():
        freqs[alpha] = count / alphas
    freqs = list(sorted(freqs.items(), key=lambda pair: pair[1], reverse=True))
    return freqs


def a1(enc, freqs, alph, length):
    cols = [{"idxs": []} for col in range(length)]
    for idx, char in enumerate(enc):
        if char in alph:
            cols[idx % length]["idxs"].append(char)

    keys = [[] for _ in range(length)]
    for col_idx, col in enumerate(cols):
        col_freqs = frequencies(col["idxs"])
        cols[col_idx]["freqs"] = col_freqs
        # пробуем самым частым буквам криптограммы подставить самую частую букву алфавита
        # берем первые 3
        for c_idx, (c, c_freq) in enumerate(col_freqs[:3]):
            keys[col_idx].append(alph[(alph.index(c) - alph.index(freqs[0][0])) % len(alph)])

    f = get_file_write('bruted1.txt')
    for comb in product(*keys):
        key = ''.join(comb)
        f.write('КЛЮЧ: {}\n{}\n\n'.format(key, Vig.decrypt(enc, alph, key)))
    f.close()


def frequencies_words(text):
    words = text_to_words(text)
    freqs = {word: words.count(word) for word in set(words)}
    freqs = {word: word_count / len(words) for word, word_count in freqs.items() if word_count > 1}
    freqs = list(sorted(freqs.items(), key=lambda pair: pair[1], reverse=True))
    return freqs[:1000]


def a2_decrypt_char(idx, char, key, alph):
    if key[idx % len(key)] == '*':
        return '*'
    else:
        return Vig.decrypt_char(alph, idx, char, key)


def a2_decrypt(enc, key, alph):
    dec = ''
    for idx, char in enumerate(enc):
        dec += a2_decrypt_char(idx, char, key, alph)
    return dec


def a2(enc, alph, length, word):
    f = get_file_write('bruted2.txt')
    for idx_start in range(len(enc) - len(word)):
        if len(word) > length:
            # если что - отсечь
            pass
        if not all(map(lambda char: char in alph, enc[idx_start:idx_start + len(word)])):
            continue
        key = ''.join([alph[(alph.index(enc[idx + idx_start]) - alph.index(c)) % len(alph)] for idx, c in enumerate(word)])
        key += '*' * (length - len(key))
        for _ in range(idx_start % length):
            key = key[-1] + key[:-1]
        f.write('КЛЮЧ: {}\n{}\n\n'.format(key, a2_decrypt(enc, key, alph)))
    f.close()


def main():
    op = argv[1]

    if op == 'freq1':
        text = '\n'.join(map(lambda arg: read(arg).lower(), argv[2:]))
        freqs = frequencies(text)
        freqs = map(lambda pair: '{} : {:.4f}'.format(*pair), freqs)
        write('freq1.txt', '\n'.join(freqs))
    elif op == 'enc':
        msg = read(argv[2]).lower()
        key = read_text(argv[3])[0]
        alph = read(argv[4])
        enc = Vig.encrypt(msg.lower(), alph, key)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2])
        key = read(argv[3])
        alph = read(argv[4])
        dec = Vig.decrypt(enc, alph, key)
        write('dec.txt', dec)
    elif op == 'a1':
        enc = read(argv[2])
        freqs = map(lambda pair: pair.split(':'), read(argv[3]).split('\n'))
        freqs = [(k.strip(), float(v)) for k, v in freqs]
        alph = read(argv[4])
        length = int(argv[5])
        a1(enc, freqs, alph, length)
    elif op == 'freq2':
        text = '\n'.join(map(lambda arg: read(arg).lower(), argv[2:]))
        freqs = frequencies_words(text)
        freqs = map(lambda pair: '{} : {:.4f}'.format(*pair), freqs)
        write('freq2.txt', '\n'.join(freqs))
    elif op == 'a2':
        enc = read(argv[2])
        # freqs = map(lambda pair: pair.split(':'), read(argv[3]).split('\n'))
        # freqs = [(k.strip(), float(v)) for k, v in freqs]
        alph = read(argv[3])
        length = int(argv[4])
        word = argv[5]
        if not all(map(lambda c: c in alph, word)):
            print('В слове есть символы не из алфавита')
            exit(1)
        a2(enc, alph, length, word)
    else:
        print('ОШИБКА: неверный код операции')


if __name__ == '__main__':
    main()
