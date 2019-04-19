from utils import argv, write, read


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
