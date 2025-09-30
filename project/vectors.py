from math import *
from typing import List


def dot_product(vec1: List[float], vec2: List[float]) -> float:
    """
    Вычисляет скалярное произведение двух векторов.

    Args:
        vec1: Первый вектор (список чисел)
        vec2: Второй вектор (список чисел)

    Returns:
        Скалярное произведение

    Raises:
        ValueError: Если векторы разной длины
    """
    if len(vec1) != len(vec2):
        raise ValueError("Некорректный ввод: векторы должны быть одинаковой длины!")
    else:
        result = 0
        for i in range(len(vec1)):
            result += vec1[i] * vec2[i]
        return result


def vector_length(vec: List[float]) -> float:
    """
    Вычисляет длину вектора.
    Args:
        vec: Вектор (список чисел)
    Returns:
        Длина вектора
    """
    sm_sq = 0
    for num in vec:
        sm_sq += num**2
    return sqrt(sm_sq)


def vector_angle(vec1: List[float], vec2: List[float]) -> float:
    """
    Вычисляет угол между двумя векторами в радианах.
    Args:
        vec1: Первый вектор (список чисел)
        vec2: Второй вектор (список чисел)
    Returns:
        Угол между векторами в радианах
    Raises:
        ValueError: Если векторы разной длины или нулевые
    """
    if len(vec1) != len(vec2):
        raise ValueError("Некорректный ввод: векторы должны быть одинаковой длины!")

    else:
        dot = dot_product(vec1, vec2)
        len1 = vector_length(vec1)
        len2 = vector_length(vec2)

        if len1 == 0 or len2 == 0:
            raise ValueError("Некорректный ввод: векторы должны быть ненулевыми!")

        return acos(dot / (len1 * len2))
