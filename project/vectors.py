from math import *
from typing import List


def dot_product(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculates the dot product of two vectors.

    Args:
        vec1: First vector (list of numbers)
        vec2: Second vector (list of numbers)

    Returns:
        Dot product of vectors

    Raises:
        ValueError: If vectors have different lengths
    """
    if len(vec1) != len(vec2):
        raise ValueError("Invalid input: vectors must have the same length!")
    else:
        result = 0.0
        for i in range(len(vec1)):
            result += vec1[i] * vec2[i]
        return result


def vector_length(vec: List[float]) -> float:
    """
    Calculates the length of a vector.

    Args:
        vec: Vector (list of numbers)

    Returns:
        Length of the vector
    """
    sm_sq = 0.0
    for num in vec:
        sm_sq += num**2
    return sqrt(sm_sq)


def vector_angle(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculates the angle between two vectors in radians.

    Args:
        vec1: First vector (list of numbers)
        vec2: Second vector (list of numbers)

    Returns:
        Angle between vectors in radians

    Raises:
        ValueError: If vectors have different lengths or are zero vectors
    """
    if len(vec1) != len(vec2):
        raise ValueError("Invalid input: vectors must have the same length!")

    else:
        dot = dot_product(vec1, vec2)
        len1 = vector_length(vec1)
        len2 = vector_length(vec2)

        if len1 == 0 or len2 == 0:
            raise ValueError("Invalid input: vectors must be non-zero!")

        return acos(dot / (len1 * len2))
