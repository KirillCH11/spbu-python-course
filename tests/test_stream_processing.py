import pytest
from project.stream_processing import *


@pytest.fixture
def numbers():
    return [1, 2, 3, 4, 5]


def test_generate_data():
    """Test data stream creation"""
    data = [1, 2, 3]
    stream = generate_data(data)
    result = to_list(stream)
    assert result == [1, 2, 3]


def test_map_operation():
    stream = generate_data([1, 2, 3])
    double_op = map_stream(lambda x: x * 2)
    result = to_list(double_op(stream))
    assert result == [2, 4, 6]


def test_filter_operation():
    stream = generate_data([1, 2, 3, 4, 5])
    even_op = filter_stream(lambda x: x % 2 == 0)
    result = to_list(even_op(stream))
    assert result == [2, 4]


def test_take_operation():
    stream = generate_data([1, 2, 3, 4, 5])
    take_op = take_items(3)
    result = to_list(take_op(stream))
    assert result == [1, 2, 3]


def test_reduce_operation():
    stream = generate_data([1, 2, 3, 4])
    sum_op = reduce_stream(lambda x, y: x + y)
    result = to_list(sum_op(stream))
    assert result == [10]  # 1+2+3+4


def test_basic_pipeline():
    stream = generate_data([1, 2, 3, 4, 5, 6])

    result_stream = process_pipeline(
        stream,
        filter_stream(lambda x: x > 2),  # [3, 4, 5, 6]
        map_stream(lambda x: x * 3),  # [9, 12, 15, 18]
        take_items(2),  # [9, 12]
    )

    result = to_list(result_stream)
    assert result == [9, 12]


def test_empty_pipeline():
    stream = generate_data([1, 2, 3])
    result_stream = process_pipeline(stream)
    result = to_list(result_stream)
    assert result == [1, 2, 3]


def test_different_collections():
    stream = generate_data([1, 2, 2, 3, 4])

    as_list = to_list(stream)
    assert as_list == [1, 2, 2, 3, 4]

    stream = generate_data([1, 2, 2, 3, 4])
    as_tuple = to_tuple(stream)
    assert as_tuple == (1, 2, 2, 3, 4)

    stream = generate_data([1, 2, 2, 3, 4])
    as_set = to_set(stream)
    assert as_set == {1, 2, 3, 4}


def test_lazy_evaluation_simple():
    processed = []

    def track(x):
        processed.append(x)
        return x

    stream = generate_data([1, 2, 3, 4, 5])
    tracked_stream = map_stream(track)(stream)
    taken_stream = take_items(2)(tracked_stream)

    result = to_list(taken_stream)

    assert processed == [1, 2]
    assert result == [1, 2]


def test_lazy_evaluation_infinite():
    def infinite_counter():
        i = 1
        while True:
            yield i
            i += 1

    stream = infinite_counter()
    result_stream = process_pipeline(stream, take_items(3))

    result = to_list(result_stream)
    assert result == [1, 2, 3]
