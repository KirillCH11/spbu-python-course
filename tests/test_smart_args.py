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


def test_cannot_combine_isolated_and_evaluated():
    evaluated_with_isolated = Evaluated(Isolated())

    with pytest.raises(TypeError):
        evaluated_with_isolated.factory()
    evaluated_with_isolated_class = Evaluated(Isolated)
    with pytest.raises(TypeError):
        evaluated_with_isolated_class.factory()


def test_separate_isolated_and_evaluated_parameters():
    call_count = 0

    def counter():
        nonlocal call_count
        call_count += 1
        return call_count

    @smart_args
    def combined_function(
        *, isolated_param=Isolated, evaluated_param=Evaluated(counter), normal_param=100
    ):
        return isolated_param, evaluated_param, normal_param

    original_data = {"key": "value"}

    result1 = combined_function(isolated_param=original_data)
    assert result1[0] is not original_data
    assert result1[1] == 1
    assert result1[2] == 100

    result2 = combined_function(isolated_param=original_data, normal_param=200)
    assert result2[0] is not original_data
    assert result2[1] == 2
    assert result2[2] == 200

    assert original_data == {"key": "value"}


def test_multiple_evaluated_parameters():
    counters = {"a": 0, "b": 0}

    def counter_a():
        counters["a"] += 1
        return f"a_{counters['a']}"

    def counter_b():
        counters["b"] += 1
        return f"b_{counters['b']}"

    @smart_args
    def multi_evaluated(*, first=Evaluated(counter_a), second=Evaluated(counter_b)):
        return first, second

    result1 = multi_evaluated()
    assert result1 == ("a_1", "b_1")

    result2 = multi_evaluated()
    assert result2 == ("a_2", "b_2")

    result3 = multi_evaluated(first="fixed")
    assert result3 == ("fixed", "b_3")


def test_multiple_isolated_parameters():
    @smart_args
    def multi_isolated(*, list_data=Isolated, dict_data=Isolated):
        list_data.append("modified_list")
        dict_data["modified"] = True
        return list_data, dict_data

    original_list = [1, 2, 3]
    original_dict = {"key": "value"}

    result_list, result_dict = multi_isolated(
        list_data=original_list, dict_data=original_dict
    )

    assert result_list == [1, 2, 3, "modified_list"]
    assert result_dict == {"key": "value", "modified": True}

    assert original_list == [1, 2, 3]
    assert original_dict == {"key": "value"}
