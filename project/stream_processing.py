from typing import Any, Callable, Generator, Iterable, List, Tuple, Set
from functools import reduce


def generate_data(data: Iterable) -> Generator[Any, None, None]:
    """
    Creates a data stream from a collection.
    Args:
        data: Any collection (list, tuple, range, etc.)
    Yields:
        Data elements one by one
    """
    for item in data:
        yield item


def process_pipeline(stream: Generator, *operations: Callable) -> Generator:
    """
    Applies operations to the data stream sequentially.
    Args:
        stream: Data stream
        *operations: Processing functions
    Yields:
        Processed data
    """
    current_stream = stream
    for operation in operations:
        current_stream = operation(current_stream)
    yield from current_stream


def map_stream(func: Callable) -> Callable:
    """
    Transforms each element in the stream using Python's built-in map.
    Args:
        func: Transformation function
    Returns:
        Function for the pipeline
    """

    def mapper(stream: Generator) -> Generator:
        yield from map(func, stream)

    return mapper


def filter_stream(func: Callable) -> Callable:
    """
    Filters elements in the stream using Python's built-in filter.

    Args:
        func: Filter function (returns True/False)

    Returns:
        Function for the pipeline
    """

    def filterer(stream: Generator) -> Generator:
        yield from filter(func, stream)

    return filterer


def take_items(count: int) -> Callable:
    """
    Takes only the first N elements.
    Args:
        count: How many elements to take

    Returns:
        Function for the pipeline
    """

    def taker(stream: Generator) -> Generator:
        for i, item in enumerate(stream):
            if i >= count:
                break
            yield item

    return taker


def skip_items(count: int) -> Callable:
    """
    Skips the first N elements.
    Args:
        count: How many elements to skip
    Returns:
        Function for the pipeline
    """

    def skipper(stream: Generator) -> Generator:
        for i, item in enumerate(stream):
            if i >= count:
                yield item

    return skipper


def reduce_stream(func: Callable, initial: Any = None) -> Callable:
    """
    Reduces the stream to a single value.
    Args:
        func: Reduction function
        initial: Initial value

    Returns:
        Function for the pipeline
    """

    def reducer(stream: Generator) -> Generator:
        items = list(stream)
        if initial is not None:
            result = reduce(func, items, initial)
        else:
            result = reduce(func, items)
        yield result

    return reducer


def to_list(stream: Generator) -> List[Any]:
    """
    Collects the stream into a list.
    Args:
        stream: Data stream
    Returns:
        List of elements
    """
    return list(stream)


def to_tuple(stream: Generator) -> Tuple[Any, ...]:
    """
    Collects the stream into a tuple.
    Args:
        stream: Data stream
    Returns:
        Tuple of elements
    """
    return tuple(stream)


def to_set(stream: Generator) -> Set[Any]:
    """
    Collects the stream into a set.
    Args:
        stream: Data stream
    Returns:
        Set of elements
    """
    return set(stream)
