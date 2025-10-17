from typing import Callable, Any


def curry_explicit(function: Callable, arity: int) -> Callable:
    """
    Converts a function into a curried version
    Args:
        function: Function to curry
        arity: Number of arguments the function expects
    Returns:
        Curried function
    Raises:
        ValueError: If arity is negative
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative!")

    def curried(*args):
        if len(args) > arity:
            raise ValueError(f"Many arguments: expected {arity}, got {len(args)}!")

        if len(args) == arity:
            return function(*args)

        def next_curried(next_arg):
            return curried(*(args + (next_arg,)))

        return next_curried

    return curried


def uncurry_explicit(function: Callable, arity: int) -> Callable:
    """
    Converts a curried function back to normal form
    Args:
        function: Curried function
        arity: Number of arguments the function expects
    Returns:
        Uncurried function
    Raises:
        ValueError: If arity is negative
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative!")

    def uncurried(*args):
        if len(args) != arity:
            raise ValueError(f"Many arguments: expected {arity}, got {len(args)}")

        result = function
        for arg in args:
            result = result(arg)

        return result

    return uncurried
