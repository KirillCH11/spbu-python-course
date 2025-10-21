from copy import deepcopy
from typing import Callable, Any


class Isolated:
    """
    Marker for arguments that should be deep copied
    """

    pass


class Evaluated:
    """
    Marker for arguments with dynamically evaluated default values
    Args:
        factory: Function that produces the default value
    """

    def __init__(self, factory: Callable[[], Any]):
        self.factory = factory


def smart_args(func: Callable) -> Callable:
    """
    Decorator that handles Isolated and Evaluated arguments
    Args:
        func: Function to decorate
    Returns:
        Decorated function
    """
    import inspect

    signature = inspect.signature(func)

    def wrapper(*args, **kwargs):
        assert len(args) == 0, "smart_args only supports keyword arguments!"

        new_kwargs = {}

        for param_name, param in signature.parameters.items():
            if param_name in kwargs:
                value = kwargs[param_name]

                if param.default is Isolated:
                    new_kwargs[param_name] = deepcopy(value)
                else:
                    new_kwargs[param_name] = value

            else:
                default = param.default

                if isinstance(default, Evaluated):
                    new_kwargs[param_name] = default.factory()
                elif default is Isolated:
                    raise ValueError(
                        f"Isolated parameter '{param_name}' must be provided"
                    )
                else:
                    new_kwargs[param_name] = default

        return func(**new_kwargs)

    return wrapper
