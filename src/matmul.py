"""Matrix multiplication utilities.

This module consolidates the matrix-multiplication code that was originally
scattered across multiple notebook cells (a NumPy demo and a separate
pure-Python implementation) into a single, testable, documented module.

Functions
---------
matmul(mat1, mat2)
    Pure-Python matrix multiplication with full dimension/type validation.
matmul_numpy(matrix_a, matrix_b)
    Thin wrapper around NumPy for comparison / performance-sensitive use.
determinant(matrix)
    Convenience wrapper around numpy.linalg.det with basic validation.
"""

from __future__ import annotations

import numpy as np

Number = int | float
Matrix = list[list[Number]]


def _validate_matrix(matrix: Matrix, name: str) -> tuple[int, int]:
    """Validate that ``matrix`` is a non-empty, rectangular list of lists.

    Args:
        matrix: The matrix to validate.
        name: Human-readable name used in error messages (e.g. "mat1").

    Returns:
        A ``(rows, cols)`` tuple describing the matrix shape.

    Raises:
        ValueError: If the matrix is empty or its rows have inconsistent
            lengths (i.e. it is not rectangular).
        TypeError: If any element is not numeric.
    """
    if not matrix or not matrix[0]:
        raise ValueError(f"{name} must be a non-empty 2D list.")

    n_cols = len(matrix[0])
    for i, row in enumerate(matrix):
        if len(row) != n_cols:
            raise ValueError(
                f"{name} is not rectangular: row 0 has {n_cols} columns "
                f"but row {i} has {len(row)}."
            )
        for value in row:
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"{name} must contain only numbers, found {type(value)!r}."
                )

    return len(matrix), n_cols


def matmul(mat1: Matrix, mat2: Matrix) -> Matrix:
    """Multiply two matrices using pure Python (no external dependencies).

    Args:
        mat1: The left matrix, shape (m, n), as a list of lists.
        mat2: The right matrix, shape (n, p), as a list of lists.

    Returns:
        The product matrix, shape (m, p), as a list of lists.

    Raises:
        ValueError: If either matrix is empty/ragged, or if the inner
            dimensions of ``mat1`` and ``mat2`` do not match
            (mat1 columns must equal mat2 rows).
        TypeError: If either matrix contains non-numeric values.

    Examples:
        >>> matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        [[19, 22], [43, 50]]
    """
    m, n = _validate_matrix(mat1, "mat1")
    n2, p = _validate_matrix(mat2, "mat2")

    if n != n2:
        raise ValueError(
            f"Incompatible dimensions for multiplication: "
            f"mat1 is {m}x{n}, mat2 is {n2}x{p} "
            f"(mat1 columns must equal mat2 rows)."
        )

    result: Matrix = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            s = 0
            for k in range(n):
                s += mat1[i][k] * mat2[k][j]
            result[i][j] = s

    return result


def matmul_numpy(matrix_a: Matrix, matrix_b: Matrix) -> np.ndarray:
    """Multiply two matrices using NumPy.

    Kept alongside :func:`matmul` so the pure-Python and NumPy results can
    be cross-checked in tests (see ``tests/test_matmul.py``).

    Args:
        matrix_a: The left matrix.
        matrix_b: The right matrix.

    Returns:
        The product as a NumPy array.
    """
    return np.dot(np.array(matrix_a), np.array(matrix_b))


def determinant(matrix: Matrix) -> float:
    """Compute the determinant of a square matrix.

    Args:
        matrix: A square matrix as a list of lists.

    Returns:
        The determinant as a float.

    Raises:
        ValueError: If the matrix is not square.
    """
    rows, cols = _validate_matrix(matrix, "matrix")
    if rows != cols:
        raise ValueError(f"determinant requires a square matrix, got {rows}x{cols}.")
    return float(np.linalg.det(np.array(matrix)))


if __name__ == "__main__":
    # Small runnable demo, equivalent to the original notebook cells.
    matrix_a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    matrix_b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

    product = matmul(matrix_a, matrix_b)
    print("Matrix A:", matrix_a)
    print("Matrix B:", matrix_b)
    print("A * B   :", product)
    print("det(A*B):", determinant(product))
