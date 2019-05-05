from copy import deepcopy
from operator import xor


def swap(mat, idx_1, idx_2, indices, ops):
    mat[idx_1], mat[idx_2] = mat[idx_2], mat[idx_1]
    indices[idx_1], indices[idx_2] = indices[idx_2], indices[idx_1]
    ops[idx_1], ops[idx_2] = ops[idx_2], ops[idx_1]


def extend_list(arr1: list, arr2: list):
    arr1.extend(arr2)
    for el in set(arr1):
        if arr1.count(el) % 2 == 0:
            while el in arr1:
                arr1.remove(el)


def _gaussian(mat):
    indices = [idx for idx in range(len(mat))]
    ops = [[idx] for idx in range(len(mat))]
    sols = set()

    limit = min(len(mat), len(mat[0]))
    for i in range(limit):
        for i_find in range(i, len(mat)):
            if mat[i_find][i] == 1:
                swap(mat, i, i_find, indices, ops)
                break
        if mat[i][i] == 0:
            continue
        for i_xor in range(i + 1, len(mat)):
            if mat[i_xor][i] == 1:
                mat[i_xor] = list(map(xor, mat[i_xor], mat[i]))
                extend_list(ops[i_xor], ops[i])
                if all(map(lambda el: el == 0, mat[i_xor])):
                    sol = tuple(sorted(ops[i_xor]))
                    if sol in sols:
                        continue
                    yield sol


def gaussian(mat):
    for sol in _gaussian(deepcopy(mat)):
        if sol is None:
            return None
        buffer = [0] * len(mat[0])
        for row_idx in sol:
            for j in range(len(mat[0])):
                buffer[j] ^= mat[row_idx][j]
        assert all(map(lambda el: el == 0, buffer))
        yield sol
