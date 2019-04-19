from utils import *
import cyphers.permutation as perm


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
            if not perm.is_monocycle_key(container):
                print('ОШИБКА: неверно сгенерирован ключ длины {}: {}'.format(length, perm.str_key(container)))
            yield container
            container[idx_next] = None
    container[idx_cur] = None


def brute(enc, length):
    container = [None] * length
    f = get_file_write('bruted.txt')
    for key in _brute(length, container, 0):
        print(perm.str_key(key) + '\r', end='')
        dec = perm.decrypt(enc, key)
        f.write(perm.str_key(key) + '\n')
        f.write(dec + '\n\n')
    f.close()


def main():
    if op == 'gen':
        perm.exec_gen_mono_key()
    elif op == 'enc':
        perm.exec_encrypt()
    elif op == 'dec':
        perm.exec_decrypt()
    elif op == 'kas':
        enc = read(argv[2]).lower()
        print('Количество символов: {}'.format(len(enc)))
        start, end = int(argv[3]), int(argv[4])
        kasiski(enc, start, end)
    elif op == 'brute':
        enc = read(argv[2])
        length = int(argv[3])
        brute(enc, length)
    else:
        print_wrong_op()


if __name__ == '__main__':
    main()
