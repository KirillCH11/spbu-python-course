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

    def curried(*args):
        if len(args) > 1:
            raise ValueError(f"Too many arguments: expected at most 1, got {len(args)}")

        if len(args) == 0 and arity > 0:
            return curried

        if len(args) == 1:
            arg = args[0]

            if not hasattr(curried, "accumulated_args"):
                curried.accumulated_args = []

            curried.accumulated_args.append(arg)

            if len(curried.accumulated_args) == arity:
                result = function(*curried.accumulated_args)
                curried.accumulated_args = []
                return result
            else:
                return curried

        if arity == 0:
            return function()

        return curried

    curried.accumulated_args = []
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
        raise ValueError("Arity cannot be negative")

    def uncurried(*args):
        if len(args) != arity:
            raise ValueError(
                f"Wrong number of arguments: expected {arity}, got {len(args)}"
            )

        result = function
        for arg in args:
            result = result(arg)
        return result

    return uncurried
