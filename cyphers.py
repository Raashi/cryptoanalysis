from random import choice, shuffle
from itertools import permutations

from utils import alph_rus, write


def text_to_words(text):
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
    return words


def frequencies(text, alph):
    freqs = {}
    alphas = 0
    for c in text:
        if c in alph:
            freqs[c] = freqs.get(c, 0) + 1
            alphas += 1

    for alpha, count in freqs.items():
        freqs[alpha] = count / alphas
    freqs = list(sorted(freqs.items(), key=lambda pair: pair[1], reverse=True))
    return freqs


class Permutations:
    @staticmethod
    def read_key(skey):
        return list(map(lambda el: int(el) - 1, skey.split(',')))

    @staticmethod
    def str_key(key):
        return ','.join(map(lambda el: str(el + 1), key))

    @staticmethod
    def is_monocycle_key(key):
        idx, start, cycle = 0, 0, 1
        while key[idx] != start:
            idx, cycle = key[idx], cycle + 1
        res = cycle == len(key)
        if not res:
            print('ОШИБКА: сгенерированный ключ не моноцикличен:', Permutations.str_key(key))
        return res

    @staticmethod
    def gen_monocycle_key(length):
        key = [None] * length
        free = [idx for idx in range(1, length)]

        start = idx = 0
        while len(free):
            idx_next = choice(free)
            free.remove(idx_next)
            key[idx] = idx_next
            idx = idx_next
        # noinspection PyTypeChecker
        key[idx] = start

        if not Permutations.is_monocycle_key(key):
            exit(1)
        print('Сгенерирован ключ длины {}:'.format(length), Permutations.str_key(key))
        write('key.txt', Permutations.str_key(key))
        return key

    @staticmethod
    def encrypt(msg, key):
        length = len(key)
        while len(msg) % length:
            msg += choice(alph_rus)

        enc = ''
        for b in range(len(msg) // length):
            block = msg[b * length: (b + 1) * length]
            # enc += ''.join(block[el] for el in key)
            enc += ''.join(block[key.index(idx)] for idx in range(length))
        return enc

    @staticmethod
    def decrypt(enc, key):
        length = len(key)

        dec = ''
        for b in range(len(enc) // length):
            block = enc[b * length: (b + 1) * length]
            # dec += ''.join(block[key.index(idx)] for idx in range(length))
            dec += ''.join(block[el] for el in key)
        return dec


class Vigenere:
    @staticmethod
    def _encrypt_char(alph, idx, char, key):
        if char not in alph:
            return char
        else:
            return alph[(alph.index(char) + alph.index(key[idx % len(key)])) % len(alph)]

    @staticmethod
    def encrypt(msg, alph, key):
        enc = ''
        for idx, char in enumerate(msg):
            enc += Vigenere._encrypt_char(alph, idx, char, key)
        return enc

    @staticmethod
    def decrypt_char(alph, idx, char, key):
        if char not in alph:
            return char
        else:
            return alph[(alph.index(char) - alph.index(key[idx % len(key)])) % len(alph)]

    @staticmethod
    def decrypt(enc, alph, key):
        dec = ''
        for idx, char in enumerate(enc):
            dec += Vigenere.decrypt_char(alph, idx, char, key)
        return dec


class Replacement:
    PRECISION = 3

    @staticmethod
    def gen(alph):
        key = list(alph)
        shuffle(key)
        return ''.join(key)

    @staticmethod
    def encrypt(msg, key, alph):
        return ''.join(map(lambda c: key[alph.index(c)] if c in alph else c, msg))

    @staticmethod
    def decrypt(enc, key, alph):
        return ''.join(map(lambda c: alph[key.index(c)] if c in alph else c, enc))

    @staticmethod
    def attack_shift(freq_true, freq_enc, count):
        freq_true = ''.join(map(lambda pair: pair[0], freq_true))
        alph = ''.join(sorted(freq_true))

        keys = []
        for letter, freq in freq_enc[:count]:
            shift = alph.index(letter) - alph.index(freq_true[0][0])
            keys.append(alph[shift:] + alph[:shift])
        return keys

    @staticmethod
    def brute(groups, idx, cont):
        if idx == len(groups):
            yield cont
            return
        for perm in permutations(groups[idx]):
            cont.extend(perm)
            yield from Replacement.brute(groups, idx + 1, cont)
            for _ in range(len(perm)):
                cont.pop()

    @staticmethod
    def images(freq_true, freq_enc, prec):
        freq_true = ''.join(map(lambda pair: pair[0], freq_true))

        for idx, (letter, freq) in enumerate(freq_enc):
            freq_new = freq[:2] + freq[2:2 + prec + 1]
            freq_enc[idx] = (letter, freq_new)

        alph = ''.join(sorted(freq_true))
        for c in alph:
            if not any(pair[0] == c for pair in freq_enc):
                freq_enc.append((c, '0.0'))

        groups = []
        while len(freq_enc):
            groups.append([freq_enc[0][0]])
            value = freq_enc[0][1]
            freq_enc = freq_enc[1:]
            while len(freq_enc) and freq_enc[0][1] == value:
                groups[-1].append(freq_enc[0][0])
                freq_enc = freq_enc[1:]

        for item in groups:
            print(item)

        res = []
        for key in Replacement.brute(groups, 0, []):
            key_str = ''.join(key)
            key_good = ''.join([key_str[freq_true.index(c)] for c in alph])
            res.append(key_good)
        return res
