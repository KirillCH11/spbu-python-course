from typing import Any, Callable, Generator, Iterable, List
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
    for operation in operations:
        stream = operation(stream)
    yield from stream


def map_stream(func: Callable) -> Callable:
    """
    Transforms each element in the stream.
    Args:
        func: Transformation function
    Returns:
        Function for the pipeline
    """

    def mapper(stream: Generator) -> Generator:
        for item in stream:
            yield func(item)

    return mapper


def filter_stream(func: Callable) -> Callable:
    """
    Filters elements in the stream.
    Args:
        func: Filter function (returns True/False)
    Returns:
        Function for the pipeline
    """

    def filterer(stream: Generator) -> Generator:
        for item in stream:
            if func(item):
                yield item

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
