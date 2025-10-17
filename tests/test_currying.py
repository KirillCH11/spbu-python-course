import pytest
from project.currying import curry_explicit, uncurry_explicit


def test_curry_three_args():
    def concat_three(a, b, c):
        return f"{a}-{b}-{c}"

    curried = curry_explicit(concat_three, 3)
    step1 = curried("A")
    step2 = step1("B")
    result = step2("C")
    assert result == "A-B-C"


def test_uncurry_three_args():
    def curried_func(x):
        def inner1(y):
            def inner2(z):
                return f"{x}|{y}|{z}"

            return inner2

        return inner1

    uncurried = uncurry_explicit(curried_func, 3)
    result = uncurried("X", "Y", "Z")
    assert result == "X|Y|Z"


def test_curry_uncurry_roundtrip():
    def original(x, y):
        return x * y

    curried = curry_explicit(original, 2)
    uncurried = uncurry_explicit(curried, 2)
    assert uncurried(5, 6) == 30


def test_curry_zero_arity():
    def get_answer():
        return 42

    curried = curry_explicit(get_answer, 0)
    assert curried() == 42


def test_error_cases():
    def simple_func(x, y):
        return x + y

    with pytest.raises(ValueError):
        curry_explicit(simple_func, -1)

    curried = curry_explicit(simple_func, 2)
    with pytest.raises(ValueError):
        curried(1, 2, 3)

    uncurried = uncurry_explicit(lambda x: lambda y: x + y, 2)
    with pytest.raises(ValueError):
        uncurried(1, 2, 3)
    with pytest.raises(ValueError):
        uncurried(1)


def test_only_one_argument_per_call():
    def add_three(a, b, c):
        return a + b + c

    curried = curry_explicit(add_three, 3)

    result = curried(1)(2)(3)
    assert result == 6

    result2 = curried(1, 2)(3)
    assert result2 == 6


def test_builtin_functions():
    curried_len = curry_explicit(len, 1)
    assert curried_len("hello") == 5

    curried_max = curry_explicit(max, 2)
    assert curried_max(10)(20) == 20

    curried_min = curry_explicit(min, 3)
    assert curried_min(30)(20)(10) == 10


def test_variadic_functions_frozen_arity():
    def variadic_func(*args):
        return sum(args)

    curried_variadic = curry_explicit(variadic_func, 3)

    result = curried_variadic(1)(2)(3)
    assert result == 6

    with pytest.raises(ValueError):
        curried_variadic(1, 2, 3, 4)


def test_print_function_currying():
    curried_print = curry_explicit(print, 2)

    result = curried_print("Hello")("World")
    assert result is None

    with pytest.raises(ValueError):
        curried_print("A", "B", "C")
