import math
import pytest
from project.vectors import dot_product, vector_length, vector_angle


def test_dot_product() -> None:
    """Тест скалярного произведения"""
    vec1 = [1.0, 2.0, 3.0]
    vec2 = [4.0, 5.0, 6.0]
    result = dot_product(vec1, vec2)
    assert result == 32.0


def test_dot_product_different_length() -> None:
    """Тест скалярного произведения векторов разной длины (ловим ошибку)"""
    vec1 = [1.0, 2.0]
    vec2 = [1.0, 2.0, 3.0]
    with pytest.raises(ValueError):
        dot_product(vec1, vec2)


def test_vector_length() -> None:
    """Тест вычисления длины вектора"""
    assert vector_length([3.0, 4.0]) == 5.0


def test_vector_angle() -> None:
    """Тест вычисления угла между векторами"""
    vec1 = [1.0, 0.0]
    vec2 = [0.0, 1.0]
    assert abs(vector_angle(vec1, vec2) - (math.pi / 2)) < 0.0001


def test_vector_angle_zero() -> None:
    """Тест вычисления угла с нулевым вектором (снова ловим ошибку)"""
    vec1 = [1.0, 2.0]
    vec2 = [0.0, 0.0]
    with pytest.raises(ValueError):
        vector_angle(vec1, vec2)