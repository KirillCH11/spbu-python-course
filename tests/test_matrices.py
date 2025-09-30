import pytest
from project.matrices import matrix_add, matrix_multiply, matrix_transpose


def test_matrix_add() -> None:
    """Тест сложения матриц"""
    mat1 = [[1.0, 2.0], [3.0, 4.0]]
    mat2 = [[5.0, 6.0], [7.0, 8.0]]
    assert matrix_add(mat1, mat2) == [[6.0, 8.0], [10.0, 12.0]]


def test_matrix_add_different_size() -> None:
    """Тест сложения матриц разного размера (ловим ошибку)"""
    mat1 = [[1.0, 2.0]]
    mat2 = [[1.0, 2.0, 3.0]]
    with pytest.raises(ValueError):
        matrix_add(mat1, mat2)


def test_matrix_multiply() -> None:
    """Тест умножения матриц"""
    mat1 = [[1.0, 2.0], [3.0, 4.0]]
    mat2 = [[2.0, 0.0], [1.0, 2.0]]
    assert matrix_multiply(mat1, mat2) == [[4.0, 4.0], [10.0, 8.0]]


def test_matrix_multiply_incompatible() -> None:
    """Тест умножения несовместимых матриц (снова ловим ошибку)"""
    mat1 = [[1.0, 2.0, 3.0]]
    mat2 = [[1.0, 2.0]]
    with pytest.raises(ValueError):
        matrix_multiply(mat1, mat2)


def test_matrix_transpose() -> None:
    """Тест транспонирования матрицы"""
    matrix = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    assert matrix_transpose(matrix) == [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
