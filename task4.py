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


def a1(enc, freqs, length):
    cols = {col: {"idxs": []} for col in range(length)}
    for idx, char in enumerate(enc):
        if char in freqs:
            cols[idx % length]["idxs"].append(char)
    for col_idx, col in cols.items():
        cols[col_idx]["freqs"] = frequencies(col["idxs"])
    # TODO: дописать


def frequencies_words(text):
    words = text_to_words(text)
    freqs = {word: words.count(word) for word in set(words)}
    freqs = {word: word_count / len(words) for word, word_count in freqs.items() if word_count > 1}
    freqs = list(sorted(freqs.items(), key=lambda pair: pair[1], reverse=True))
    return freqs


def main():
    op = argv[1]

    if op == 'freq1':
        text = read(argv[2]).lower()
        freqs = frequencies(text)
        freqs = map(lambda pair: '{} : {:.4f}'.format(*pair), freqs)
        write('freq1.txt', '\n'.join(freqs))
    elif op == 'enc':
        freqs = read(argv[4])
        msg = read(argv[2]).lower()
        key = read_text(argv[3])[0]
        enc = Vig.encrypt(msg.lower(), freqs, key)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2])
        freqs = read(argv[3])
        key = read(argv[4])
        dec = Vig.decrypt(enc, freqs, key)
        write('dec.txt', dec)
    elif op == 'a1':
        enc = read(argv[2])
        freqs = map(lambda pair: pair.split(':'), read(argv[3]).split('\n'))
        freqs = {k: float(v) for k, v in freqs}
        length = int(argv[4])
        a1(enc, freqs, length)
    elif op == 'freq2':
        text = read(argv[2]).lower()
        freqs = frequencies_words(text)
        freqs = map(lambda pair: '{} : {:.4f}'.format(*pair), freqs)
        write('freq2.txt', '\n'.join(freqs))
    else:
        print('ОШИБКА: неверный код операции')


if __name__ == '__main__':
    main()
