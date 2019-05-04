import copy


def swap(mat, idx_1, idx_2, indices, ops):
    mat[idx_1], mat[idx_2] = mat[idx_2], mat[idx_1]
    indices[idx_1], indices[idx_2] = indices[idx_2], indices[idx_1]
    ops[idx_1], ops[idx_2] = ops[idx_2], ops[idx_1]


def _gaussian(mat):
    indices = [idx for idx in range(len(mat))]
    ops = [[idx] for idx in range(len(mat))]

    for i in range(len(mat[0])):
        for i_find in range(i, len(mat)):
            if mat[i_find][i] == 1:
                swap(mat, i, i_find, indices, ops)
                break
        if mat[i][i] == 0:
            continue
        for i_xor in range(i + 1, len(mat)):
            if mat[i_xor][i] == 1:
                mat[i_xor] = list(map(lambda a, b: a ^ b, mat[i_xor], mat[i]))
                ops[i_xor].extend(ops[i])
                if all(map(lambda el: el == 0, mat[i_xor])):
                    return ops[i_xor]


def gaussian(mat):
    sol = _gaussian(copy.deepcopy(mat))
    if sol is None:
        return None
    buffer = [0] * len(mat[0])
    for row_idx in sol:
        for j in range(len(mat[0])):
            buffer[j] ^= mat[row_idx][j]
    assert all(map(lambda el: el == 0, buffer))
    return sol
