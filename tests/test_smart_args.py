import pytest
from project.smart_args import smart_args, Isolated, Evaluated


def test_isolated_protects_original_data():
    @smart_args
    def modify_list(*, items=Isolated):
        items.append("modified")
        return items

    original_list = [1, 2, 3]
    result = modify_list(items=original_list)

    assert result == [1, 2, 3, "modified"]
    assert original_list == [1, 2, 3]
    assert result is not original_list


def test_evaluated_calls_factory_each_time():
    call_count = 0

    def counter():
        nonlocal call_count
        call_count += 1
        return call_count

    @smart_args
    def use_counter(*, value=Evaluated(counter)):
        return value

    assert use_counter() == 1
    assert use_counter() == 2
    assert use_counter() == 3


def test_evaluated_with_provided_value():
    def expensive_operation():
        assert False, "This should not be called!"

    @smart_args
    def test_func(*, data=Evaluated(expensive_operation)):
        return data

    result = test_func(data="provided_value")
    assert result == "provided_value"


def test_isolated_requires_value():
    @smart_args
    def requires_data(*, important_data=Isolated):
        return important_data

    with pytest.raises(ValueError):
        requires_data()


def test_no_positional_arguments_allowed():
    @smart_args
    def keyword_only(*, x=10):
        return x

    with pytest.raises(AssertionError):
        keyword_only(5)


def test_regular_defaults_work_normally():
    @smart_args
    def normal_function(*, a=100, b=200):
        return a + b

    assert normal_function() == 300
    assert normal_function(a=50) == 250
    assert normal_function(a=1, b=2) == 3
