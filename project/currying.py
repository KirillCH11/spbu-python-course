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
        raise ValueError("Arity cannot be negative")

    if arity == 0:

        def zero_arity():
            return function()

        return zero_arity

    def curried_function(accumulated_args: tuple = ()) -> Callable:
        if len(accumulated_args) == arity:
            return function(*accumulated_args)

        def next_curried(next_arg: Any) -> Any:
            new_args = accumulated_args + (next_arg,)
            return curried_function(new_args)

        return next_curried

    return curried_function()


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
        raise ValueError("Arity cannot be negative")

    def uncurried(*args: Any) -> Any:
        if len(args) != arity:
            raise ValueError(
                f"Wrong number of arguments: expected {arity}, got {len(args)}"
            )

        current_func = function
        for arg in args:
            current_func = current_func(arg)
        return current_func

    return uncurried
