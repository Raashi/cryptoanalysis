from random import choice

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
