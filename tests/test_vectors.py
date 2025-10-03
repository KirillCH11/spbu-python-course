import math
import pytest
from project.vectors import dot_product, vector_length, vector_angle


def test_dot_product() -> None:
    """Test dot product calculation"""
    vec1 = [1.0, 2.0, 3.0]
    vec2 = [4.0, 5.0, 6.0]
    result = dot_product(vec1, vec2)
    assert result == 32.0


def test_dot_product_different_length() -> None:
    """Test dot product with vectors of different lengths (catching error)"""
    vec1 = [1.0, 2.0]
    vec2 = [1.0, 2.0, 3.0]
    with pytest.raises(ValueError):
        dot_product(vec1, vec2)


def test_vector_length() -> None:
    """Test vector length calculation"""
    assert vector_length([3.0, 4.0]) == 5.0


def test_vector_angle() -> None:
    """Test angle calculation between vectors"""
    vec1 = [1.0, 0.0]
    vec2 = [0.0, 1.0]
    assert abs(vector_angle(vec1, vec2) - (math.pi / 2)) < 0.0001


def test_vector_angle_zero() -> None:
    """Test angle calculation with zero vector (catching error again)"""
    vec1 = [1.0, 2.0]
    vec2 = [0.0, 0.0]
    with pytest.raises(ValueError):
        vector_angle(vec1, vec2)
