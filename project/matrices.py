from typing import List


def matrix_add(matrix1: List[List[float]], matrix2: List[List[float]]) -> List[List[float]]:
    """
    Складывает две матрицы.
    Args:
        matrix1: Первая матрица (список списков)
        matrix2: Вторая матрица (список списков)
    Returns:
        Сумма матриц
    Raises:
        ValueError: Если матрицы разных размеров
    """
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])

    if rows1 != rows2 or cols1 != cols2:
        raise ValueError("Матрицы должны быть одинакового размера!")

    result = []
    for i in range(rows1):
        row = []
        for j in range(cols1):
            row.append(matrix1[i][j] + matrix2[i][j])
        result.append(row)
    return result


def matrix_multiply(matrix1: List[List[float]], matrix2: List[List[float]]) -> List[List[float]]:
    """
    Умножает две матрицы.
    Args:
        matrix1: Первая матрица (список списков)
        matrix2: Вторая матрица (список списков)
    Returns:
        Произведение матриц
    Raises:
        ValueError: Если матрицы невозможно перемножить
    """
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])

    if cols1 != rows2:
        raise ValueError("Число столбцов первой матрицы должно равняться числу строк второй!")

    result = []
    for i in range(rows1):
        row = []
        for j in range(cols2):
            sum_val = 0
            for k in range(cols1):
                sum_val += matrix1[i][k] * matrix2[k][j]
            row.append(sum_val)
        result.append(row)
    return result


def matrix_transpose(matrix: List[List[float]]) -> List[List[float]]:
    """
    Транспонирует матрицу.
    Args:
        matrix: Исходная матрица (список списков)
    Returns:
        Транспонированная матрица
    """
    rows, cols = len(matrix), len(matrix[0])

    result = []
    for j in range(cols):
        row = []
        for i in range(rows):
            row.append(matrix[i][j])
        result.append(row)
    return result