"""
usage:
%user%:> python kasiski.py gen 4
%user%:> python kasiski.py enc test.txt 2,4,1,3
%user%:> python kasiski.py dec enc.txt 2,4,1,3
%user%:> python kasiski.py kas enc.txt
"""
from utils import *
from cyphers import Permutations as Perms


def get_seqs(enc, length) -> dict:
    seqs = {}
    for idx in range(len(enc) - length):
        seq = enc[idx: idx + length]
        if seq not in seqs:
            seqs[seq] = (idx, [])
        else:
            seqs[seq][1].append(idx - seqs[seq][0])
    return {key: gcd(seqs[key][1]) for key in seqs if len(seqs[key][1])}


def _kasiski(enc, length):
    seqs = get_seqs(enc, length)
    possible = list(set(seqs.values()))
    possible.sort()
    return possible


def kasiski(enc, start, end):
    results = [_kasiski(enc, length) for length in range(start, end + 1)]
    report = []
    for idx, possible in zip(range(start, end + 1), results):
        res_str = 'Длина: {:>2} | Возможные длины ключей: {}'.format(idx, possible)
        report.append(res_str)
        print(res_str)
    write('kasiski.txt', '\n'.join(report))


def _brute(length, container: list, idx_cur):
    free = [idx for idx in range(length) if idx not in container + [idx_cur, 0]]
    for idx_next in free:
        container[idx_cur] = idx_next
        if container.count(None) > 1:
            yield from _brute(length, container, idx_next)
        else:
            container[idx_next] = 0
            if not Perms.is_monocycle_key(container):
                print('ОШИБКА: неверно сгенерирован ключ длины {}: {}'.format(length, Perms.str_key(container)))
            yield container
            container[idx_next] = None
    container[idx_cur] = None


def brute(enc, length):
    container = [None] * length
    f = get_file_write('bruted.txt')
    for key in _brute(length, container, 0):
        print(Perms.str_key(key) + '\r', end='')
        dec = Perms.decrypt(enc, key)
        f.write(Perms.str_key(key) + '\n')
        f.write(dec + '\n\n')
    f.close()


def main():
    op = argv[1]

    if op == 'gen':
        length = int(argv[2])
        Perms.gen_monocycle_key(length)
    elif op == 'enc':
        msg = read(argv[2])
        key = Perms.read_key(read(argv[3]))
        enc = Perms.encrypt(msg, key)
        write('enc.txt', enc)
    elif op == 'dec':
        enc = read(argv[2])
        key = Perms.read_key(read(argv[3]))
        dec = Perms.decrypt(enc, key)
        write('dec.txt', dec)
    elif op == 'kas':
        enc = read(argv[2]).lower()
        print('Количество символов: {}'.format(len(enc)))
        start, end = int(argv[3]), int(argv[4])
        kasiski(enc, start, end)
    elif op == 'brute':
        enc = read(argv[2]).lower()
        length = int(argv[3])
        brute(enc, length)
    else:
        print('ОШИБКА: неверная операция')


if __name__ == '__main__':
    main()
