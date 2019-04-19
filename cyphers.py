from sys import argv
from random import choice, shuffle
from itertools import permutations

from utils import write, read, get_file_write


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


def get_freqs(text, alph):
    freqs = {letter: 0 for letter in alph}
    chars_count = 0
    for char in text:
        if char in alph:
            freqs[char] += 1
            chars_count += 1

    for char, count in freqs.items():
        freqs[char] = count / chars_count

    freqs = list(sorted(freqs.items(), key=lambda pair: pair[1], reverse=True))
    return [(char, '{:.5f}'.format(count)) for char, count in freqs]


def read_freqs(filename):
    freqs = map(lambda pair: pair.split(':'), read(filename).split('\n'))
    return [(k[0], v) for k, v in freqs]


def write_freqs(filename, freqs):
    res = map(lambda pair: '{} : {}'.format(*pair), freqs)
    write(filename, '\n'.join(res))


def exec_freqs():
    text = read(argv[2]).lower()
    alph = read(argv[3])
    freqs = get_freqs(text, alph)
    write_freqs(argv[4], freqs)


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
        key[idx] = start

        if not Permutations.is_monocycle_key(key):
            exit(1)
        print('Сгенерирован ключ длины {}:'.format(length), Permutations.str_key(key))
        return key

    @staticmethod
    def encrypt(msg, key):
        length = len(key)

        alph_from_msg = list({char for char in msg if char.isalpha()})
        alph_from_msg = alph_from_msg if len(alph_from_msg) else list({char for char in msg})
        while len(msg) % length:
            msg += choice(alph_from_msg)

        enc = ''
        for b in range(len(msg) // length):
            block = msg[b * length: (b + 1) * length]
            enc += ''.join(block[key.index(idx)] for idx in range(length))
        return enc

    @staticmethod
    def decrypt(enc, key):
        length = len(key)

        dec = ''
        for b in range(len(enc) // length):
            block = enc[b * length: (b + 1) * length]
            dec += ''.join(block[el] for el in key)
        return dec

    @staticmethod
    def exec_gen_mono_key():
        length = int(argv[2])
        key = Permutations.gen_monocycle_key(length)
        write('key.txt', Permutations.str_key(key))

    @staticmethod
    def exec_encrypt():
        msg = read(argv[2])
        key = Permutations.read_key(read(argv[3]))
        enc = Permutations.encrypt(msg, key)
        write('enc.txt', enc)

    @staticmethod
    def exec_decrypt():
        enc = read(argv[2])
        key = Permutations.read_key(read(argv[3]))
        dec = Permutations.decrypt(enc, key)
        write('dec.txt', dec)


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

    @staticmethod
    def exec_encrypt():
        msg = read(argv[2]).lower()
        key = read(argv[3])
        alph = read(argv[4])
        enc = Vigenere.encrypt(msg, alph, key)
        write('enc.txt', enc)

    @staticmethod
    def exec_decrypt():
        enc = read(argv[2])
        alph = read(argv[3])
        key = read(argv[4])
        dec = Vigenere.decrypt(enc, alph, key)
        write('dec.txt', dec)

    @staticmethod
    def exec_brute():
        enc = read(argv[2])
        keys = read(argv[3]).split('\n')
        alph = read(argv[4])
        f = get_file_write('bruted.txt')
        for key in keys:
            f.write('КЛЮЧ : {}\n{}\n\n'.format(key, Vigenere.decrypt(enc, alph, key)))
            f.write('-------------------------------\n')
        f.close()


class Replacement:
    PRECISION = 3

    @staticmethod
    def gen(alph):
        key = list(alph)
        shuffle(key)
        return ''.join(key)

    @staticmethod
    def handle_key(key, alph):
        try:
            key = int(key)
            key = alph[key:] + alph[:key]
        except ValueError:
            pass
        return key

    @staticmethod
    def encrypt(msg, key, alph):
        key = Replacement.handle_key(key, alph)
        return ''.join(map(lambda c: key[alph.index(c)] if c in alph else c, msg))

    @staticmethod
    def decrypt(enc, key, alph):
        key = Replacement.handle_key(key, alph)
        return ''.join(map(lambda c: alph[key.index(c)] if c in alph else c, enc))

    @staticmethod
    def attack_shift(freq_true, freq_enc, alph, precision):
        keys = Replacement.images(freq_true, freq_enc, precision)
        shifts = {}
        for key in keys:
            key = ''.join(sorted(key, key=lambda x: alph.index(freq_true[key.index(x)][0])))
            for idx, letter in enumerate(key):
                shift = (alph.index(letter) - idx) % len(alph)
                shifts[shift] = shifts.get(shift, 0) + 1
        # берем только самые большие по количеству смещения
        min_count, max_count = min(shifts.values()), max(shifts.values())
        border_value = min_count + (max_count - min_count) * 0.5
        shifts = {shift: count for shift, count in shifts.items() if count > border_value}
        shifts = list(sorted(shifts.keys(), key=lambda x: shifts[x], reverse=True))
        return [alph] + list(map(str, shifts[:3]))

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
    def images(freq_true, freq_enc, precision):
        freq_true = ''.join(map(lambda pair: pair[0], freq_true))

        for idx, (letter, freq) in enumerate(freq_enc):
            freq_new = freq[:2] + freq[2:2 + precision + 1]
            freq_enc[idx] = (letter, freq_new)

        groups = []
        while len(freq_enc):
            groups.append([freq_enc[0][0]])
            value = freq_enc[0][1]
            freq_enc = freq_enc[1:]
            while len(freq_enc) and freq_enc[0][1] == value and float(value) > 0:
                groups[-1].append(freq_enc[0][0])
                freq_enc = freq_enc[1:]

        res = [''.join(map(lambda pair: pair[0], freq_true))]
        for key in Replacement.brute(groups, 0, []):
            res.append(''.join(key))
            if len(res) > 1000:
                break
        return res

    @staticmethod
    def exec_encrypt():
        msg = read(argv[2]).lower()
        alph, key = read(argv[3]).split('\n')
        enc = Replacement.encrypt(msg, key, alph)
        write('enc.txt', enc)

    @staticmethod
    def exec_decrypt():
        enc = read(argv[2]).lower()
        alph, key = read(argv[3]).split('\n')
        dec = Replacement.decrypt(enc, key, alph)
        write('dec.txt', dec)
