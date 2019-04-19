from utils import argv, read, write, get_file_write


def _encrypt_char(alph, idx, char, key):
    if char not in alph:
        return char
    else:
        return alph[(alph.index(char) + alph.index(key[idx % len(key)])) % len(alph)]


def encrypt(msg, alph, key):
    enc = ''
    for idx, char in enumerate(msg):
        enc += _encrypt_char(alph, idx, char, key)
    return enc


def decrypt_char(alph, idx, char, key):
    if char not in alph:
        return char
    else:
        return alph[(alph.index(char) - alph.index(key[idx % len(key)])) % len(alph)]


def decrypt(enc, alph, key):
    dec = ''
    for idx, char in enumerate(enc):
        dec += decrypt_char(alph, idx, char, key)
    return dec


def exec_encrypt():
    msg = read(argv[2]).lower()
    key = read(argv[3])
    alph = read(argv[4])
    enc = encrypt(msg, alph, key)
    write('enc.txt', enc)


def exec_decrypt():
    enc = read(argv[2])
    alph = read(argv[3])
    key = read(argv[4])
    dec = decrypt(enc, alph, key)
    write('dec.txt', dec)


def exec_brute():
    enc = read(argv[2])
    keys = read(argv[3]).split('\n')
    alph = read(argv[4])
    f = get_file_write('bruted.txt')
    for key in keys:
        f.write('КЛЮЧ : {}\n{}\n\n'.format(key, decrypt(enc, alph, key)))
        f.write('-------------------------------\n')
    f.close()
