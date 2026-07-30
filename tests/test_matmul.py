"""Tests for src/matmul.py.

The original notebook defined overlapping/duplicated test cases across
several cells (cell 22-26 and cell 76 both re-implemented ``matmul`` and
similar tests). This file consolidates them into one clean pytest module
that imports the real implementation instead of redefining it.

Run with:
    pytest --html=docs/test_report.html --self-contained-html tests/test_matmul.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Make src/ importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from matmul import matmul, matmul_numpy, determinant  # noqa: E402


# --------------------------------------------------------------------------- #
# Positive test cases: valid inputs that should produce a correct result.
# --------------------------------------------------------------------------- #

def test_2x2_square_matrices():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    assert matmul(a, b) == [[19, 22], [43, 50]]


def test_3x3_square_matrices_matches_numpy():
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    expected = matmul_numpy(a, b).tolist()
    assert matmul(a, b) == expected


def test_row_vector_times_matrix():
    # 1xN row vector * NxM matrix
    a = [[1, 2, 3]]
    b = [[1], [1], [1]]
    assert matmul(a, b) == [[6]]


def test_identity_matrix_is_neutral():
    a = [[4, 7], [2, 6]]
    identity = [[1, 0], [0, 1]]
    assert matmul(a, identity) == a


def test_rectangular_matrices():
    # (2x3) * (3x2) -> (2x2)
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[7, 8], [9, 10], [11, 12]]
    assert matmul(a, b) == [[58, 64], [139, 154]]


def test_determinant_of_product():
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    product = matmul(a, b)
    expected = float(np.linalg.det(np.array(product)))
    assert determinant(product) == pytest.approx(expected)


# --------------------------------------------------------------------------- #
# Negative test cases: invalid inputs that should raise an appropriate error.
# --------------------------------------------------------------------------- #

def test_incompatible_dimensions_raises_value_error():
    a = [[1, 2, 3], [4, 5, 6]]     # 2x3
    b = [[7, 8], [9, 0]]           # 2x2  -> inner dims 3 != 2
    with pytest.raises(ValueError):
        matmul(a, b)


def test_empty_matrix_raises_value_error():
    with pytest.raises(ValueError):
        matmul([], [[1, 2], [3, 4]])


def test_ragged_matrix_raises_value_error():
    ragged = [[1, 2], [3]]  # rows have different lengths
    with pytest.raises(ValueError):
        matmul(ragged, [[1, 2], [3, 4]])


def test_non_numeric_entry_raises_type_error():
    bad = [[1, "x"], [3, 4]]
    with pytest.raises(TypeError):
        matmul(bad, [[1, 0], [0, 1]])


def test_determinant_requires_square_matrix():
    with pytest.raises(ValueError):
        determinant([[1, 2, 3], [4, 5, 6]])
