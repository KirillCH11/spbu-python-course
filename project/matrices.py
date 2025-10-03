from typing import List


def matrix_add(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    """
    Adds two matrices.

    Args:
        matrix1: First matrix (list of lists)
        matrix2: Second matrix (list of lists)

    Returns:
        Sum of matrices

    Raises:
        ValueError: If matrices have different dimensions
    """
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])

    if rows1 != rows2 or cols1 != cols2:
        raise ValueError("Matrices must have the same dimensions!")

    result = []
    for i in range(rows1):
        row = []
        for j in range(cols1):
            row.append(matrix1[i][j] + matrix2[i][j])
        result.append(row)
    return result


def matrix_multiply(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    """
    Multiplies two matrices.

    Args:
        matrix1: First matrix (list of lists)
        matrix2: Second matrix (list of lists)

    Returns:
        Product of matrices

    Raises:
        ValueError: If matrices cannot be multiplied
    """
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])

    if cols1 != rows2:
        raise ValueError(
            "Number of columns of the first matrix must equal number of rows of the second matrix!"
        )

    result = []
    for i in range(rows1):
        row = []
        for j in range(cols2):
            sum_val = 0.0
            for k in range(cols1):
                sum_val += matrix1[i][k] * matrix2[k][j]
            row.append(sum_val)
        result.append(row)
    return result


def matrix_transpose(matrix: List[List[float]]) -> List[List[float]]:
    """
    Transposes a matrix.

    Args:
        matrix: Input matrix (list of lists)

    Returns:
        Transposed matrix
    """
    rows, cols = len(matrix), len(matrix[0])

    result = []
    for j in range(cols):
        row = []
        for i in range(rows):
            row.append(matrix[i][j])
        result.append(row)
    return result
