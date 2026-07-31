def matmul(mat1, mat2):
    m = len(mat1)
    n = len(mat1[0])
    n2 = len(mat2)
    p = len(mat2[0])

    if n != n2:
        raise ValueError("Incompatible dimensions")

    result = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            s = 0
            for k in range(n):
                s += mat1[i][k] * mat2[k][j]
            result[i][j] = s

    return result


def matmul_numpy(matrix_a, matrix_b):
    import numpy as np
    return np.dot(np.array(matrix_a), np.array(matrix_b))


def determinant(matrix):
    import numpy as np
    rows = len(matrix)
    cols = len(matrix[0])
    if rows != cols:
        raise ValueError("Matrix must be square")
    return float(np.linalg.det(np.array(matrix)))
