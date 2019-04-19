from random import choice

from utils import *
import cyphers.vigenere as vig


TEST_FILENAME = 'table.txt'


def get_eindex(seq1, seq2, verbose=False):
    length = min(len(seq1), len(seq2))
    seq1, seq2 = seq1[:length], seq2[:length]
    if verbose:
        print('Количество анализируемых символов: {}'.format(min(len(seq1), len(seq2))))
    eindex = sum(map(lambda x, y: int(x == y), seq1, seq2)) / length
    return eindex * 100


def get_meindex(seq1, seq2, alph, verbose=False):
    seq1 = ''.join(filter(lambda x: x in alph, seq1))
    seq2 = ''.join(filter(lambda x: x in alph, seq2))
    if verbose:
        print('Количество анализируемых символов: {}'.format(min(len(seq1), len(seq2))))
    meindex = sum(seq1.count(char) * seq2.count(char) for char in alph) / len(seq1) / len(seq2)
    return meindex * 100


def analyze_shifts(enc):
    for shift in range(1, 16):
        msg_shifted = enc[shift:]
        eindex = get_eindex(enc, msg_shifted)
        print('l = {:>2} | индекс = {:.2f}'.format(shift, eindex))


def main():
    if op == 'gen':
        alph, length = read(argv[2]), int(argv[3])
        seq = ''.join(choice(alph) for _ in range(length))
        write(argv[4], seq)
    elif op == 'eindex':
        seq1, seq2 = read(argv[2]), read(argv[3])
        eindex = get_eindex(seq1, seq2, verbose=True)
        print('Индекс вопадения x 100 : {:.2f}'.format(eindex))
    elif op == 'meindex':
        seq1, seq2 = read(argv[2]), read(argv[3])
        alph = read(argv[4])
        meindex = get_meindex(seq1, seq2, alph, verbose=True)
        print('Средний индекс совпадения x 100 : {:.2f}'.format(meindex))
    elif op == 'enc':
        vig.exec_encrypt()
    elif op == 'dec':
        vig.exec_decrypt()
    elif op == 'analyze':
        enc = read(argv[2])
        analyze_shifts(enc)
    else:
        print_wrong_op()


if __name__ == '__main__':
    main()
