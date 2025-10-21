import pytest
from project.currying import curry_explicit, uncurry_explicit


def test_curry_processes_arguments_step_by_step():
    """Test that curried function processes one argument at each step"""

    def concatenate(a, b, c):
        return f"{a}-{b}-{c}"

    curried = curry_explicit(concatenate, 3)

    # Apply arguments one by one
    after_first = curried("A")  # Returns function waiting for 2nd argument
    after_second = after_first("B")  # Returns function waiting for 3rd argument
    result = after_second("C")  # Returns final result

    assert result == "A-B-C"
    assert callable(after_first)
    assert callable(after_second)


def test_uncurry_combines_function_chain():
    """Test that uncurry turns function chain back into multi-argument function"""

    def curried_func(x):
        def inner1(y):
            def inner2(z):
                return f"{x}|{y}|{z}"

            return inner2

        return inner1

    uncurried = uncurry_explicit(curried_func, 3)
    result = uncurried("X", "Y", "Z")

    assert result == "X|Y|Z"


def test_curry_uncurry_preserves_original_behavior():
    """Test that curry and uncurry are inverse operations"""

    def original(x, y):
        return x * y

    curried = curry_explicit(original, 2)
    uncurried = uncurry_explicit(curried, 2)

    assert uncurried(5, 6) == 30


def test_curry_with_zero_arguments():
    """Test currying function with no arguments"""

    def get_answer():
        return 42

    curried = curry_explicit(get_answer, 0)
    assert curried() == 42


def test_curry_with_one_argument():
    """Test currying function with single argument"""

    def identity(x):
        return x

    curried = curry_explicit(identity, 1)
    assert curried(5) == 5


def test_error_on_negative_arity():
    """Test that negative arity raises ValueError"""

    def func(x):
        return x

    with pytest.raises(ValueError):
        curry_explicit(func, -1)


def test_curried_function_accepts_only_one_argument_per_call():
    """Test that curried function rejects multiple arguments in single call"""

    def func(a, b, c):
        return a + b + c

    curried = curry_explicit(func, 3)

    result = curried(1)(2)(3)
    assert result == 6

    with pytest.raises(ValueError):
        curried(1, 2)  # Multiple args in first call

    with pytest.raises(ValueError):
        curried(1)(2, 3)  # Multiple args in later call


def test_error_on_too_many_arguments():
    """Test error when too many arguments passed to curried function"""

    def func(x, y):
        return x + y

    curried = curry_explicit(func, 2)

    # Too many in single call to curried function
    with pytest.raises(ValueError):
        curried(1, 2, 3)


def test_error_on_wrong_arity_in_uncurry():
    """Test error when wrong number of arguments passed to uncurried function"""
    uncurried = uncurry_explicit(lambda x: lambda y: x + y, 2)

    with pytest.raises(ValueError):
        uncurried(1, 2, 3)  # Too many arguments

    with pytest.raises(ValueError):
        uncurried(1)  # Too few arguments


def test_curry_with_builtin_functions():
    """Test currying works with Python built-in functions"""
    # Curried len function
    curried_len = curry_explicit(len, 1)
    assert curried_len("hello") == 5

    # Curried max function for 2 arguments
    curried_max = curry_explicit(max, 2)
    assert curried_max(10)(20) == 20


def test_curry_freezes_variadic_function_arity():
    """Test that currying fixes the number of arguments for variadic functions"""

    def sum_any(*args):
        return sum(args)

    # Freeze at 3 arguments
    curried_sum = curry_explicit(sum_any, 3)

    # Works with exactly 3 arguments
    result = curried_sum(1)(2)(3)
    assert result == 6

    # Cannot use with different number of arguments
    with pytest.raises(ValueError):
        curried_sum(1, 2)  # Too few in first call


def test_curry_with_variadic_builtin_functions_comprehensive():
    """Test currying with various built-in variadic functions"""

    # Test with multiple built-in variadic functions
    curried_max = curry_explicit(max, 3)
    assert curried_max(1)(5)(3) == 5

    curried_min = curry_explicit(min, 4)
    assert curried_min(10)(5)(8)(2) == 2

    # Test with print function
    curried_print = curry_explicit(print, 2)
    result = curried_print("Hello")("World")
    assert result is None

    # Verify arity freezing for all functions
    with pytest.raises(ValueError):
        curried_max(1, 2)  # Multiple args in first call

    with pytest.raises(ValueError):
        curried_min(10)(5, 8)  # Multiple args in later call

    with pytest.raises(ValueError):
        curried_print("A", "B")  # Multiple args for print
