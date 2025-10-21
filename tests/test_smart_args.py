import pytest
from project.smart_args import smart_args, Isolated, Evaluated


def test_isolated_protects_original_data_from_modification():
    """Test that Isolated creates deep copies to protect original data"""
    original_list = [1, 2, 3]
    original_dict = {"key": "value"}

    @smart_args
    def modify_data(*, numbers=Isolated, config=Isolated):
        numbers.append(4)
        config["modified"] = True
        return numbers, config

    result_list, result_dict = modify_data(numbers=original_list, config=original_dict)

    # Modified copies are returned
    assert result_list == [1, 2, 3, 4]
    assert result_dict == {"key": "value", "modified": True}

    # Original data remains unchanged
    assert original_list == [1, 2, 3]
    assert original_dict == {"key": "value"}


def test_evaluated_recomputes_defaults_on_each_call():
    """Test that Evaluated calls factory function for every function call"""
    call_counter = 0

    def generate_id():
        nonlocal call_counter
        call_counter += 1
        return f"id_{call_counter}"

    @smart_args
    def create_item(*, item_id=Evaluated(generate_id)):
        return item_id

    # Each call gets a new ID
    assert create_item() == "id_1"
    assert create_item() == "id_2"
    assert create_item() == "id_3"
    assert call_counter == 3


def test_evaluated_not_used_when_argument_provided():
    """Test that Evaluated factory is not called when value is provided"""
    factory_called = False

    def expensive_operation():
        nonlocal factory_called
        factory_called = True
        return "computed_value"

    @smart_args
    def test_function(*, value=Evaluated(expensive_operation)):
        return value

    # Factory not called when value provided
    result = test_function(value="provided_value")
    assert result == "provided_value"
    assert not factory_called


def test_isolated_requires_explicit_argument():
    """Test that Isolated parameters must be provided by caller"""

    @smart_args
    def process_data(*, data=Isolated):
        return data

    # Works when argument provided
    assert process_data(data=[1, 2, 3]) == [1, 2, 3]

    # Fails when argument omitted
    with pytest.raises(ValueError):
        process_data()


def test_smart_args_only_allows_keyword_arguments():
    """Test that smart_args requires keyword-only argument syntax"""

    @smart_args
    def keyword_only_function(*, param=10):
        return param

    # Keyword arguments work
    assert keyword_only_function(param=20) == 20

    # Positional arguments are rejected
    with pytest.raises(AssertionError):
        keyword_only_function(20)


def test_cannot_use_isolated_as_evaluated_factory():
    """Test that Isolated cannot be meaningfully used with Evaluated"""

    # Isolated instance is not callable, so cannot be used as Evaluated factory
    isolated_instance = Isolated()
    with pytest.raises(TypeError):
        isolated_instance()  # TypeError: 'Isolated' object is not callable

    # Isolated class itself is callable but returns useless Isolated instance
    useless_factory = Evaluated(Isolated)
    result = useless_factory.factory()
    assert isinstance(
        result, Isolated
    )  # Returns useless Isolated instance, not meaningful value


def test_cannot_use_evaluated_as_isolated_value():
    """Test that Evaluated cannot be meaningfully used as Isolated value"""

    # Evaluated instance cannot be deep copied meaningfully
    evaluated_instance = Evaluated(lambda: 42)

    # This would create a copy of Evaluated, but it's meaningless for Isolated's purpose
    # Isolated is meant for protecting user-provided values, not factory objects


def test_isolated_and_evaluated_work_correctly_in_separate_parameters():
    """Test that Isolated and Evaluated work correctly when used in separate parameters"""

    call_count = 0

    def counter():
        nonlocal call_count
        call_count += 1
        return call_count

    @smart_args
    def independent_usage(
        *,
        isolated_data=Isolated,
        evaluated_value=Evaluated(counter),
        normal_param="default",
    ):
        return isolated_data, evaluated_value, normal_param

    original = {"key": "value"}

    # First call
    result1 = independent_usage(isolated_data=original)
    assert result1[0] is not original  # isolated_data is copied
    assert result1[1] == 1  # evaluated_value is computed
    assert result1[2] == "default"  # normal_param uses default

    # Second call
    result2 = independent_usage(isolated_data=original, normal_param="custom")
    assert result2[0] is not original  # isolated_data is copied again
    assert result2[1] == 2  # evaluated_value is recomputed
    assert result2[2] == "custom"  # normal_param is overridden

    # Original remains unchanged
    assert original == {"key": "value"}


def test_multiple_evaluated_parameters_work_independently():
    """Test that multiple Evaluated parameters have independent factory functions"""
    counters = {"A": 0, "B": 0}

    def counter_a():
        counters["A"] += 1
        return f"A_{counters['A']}"

    def counter_b():
        counters["B"] += 1
        return f"B_{counters['B']}"

    @smart_args
    def use_both_counters(*, first=Evaluated(counter_a), second=Evaluated(counter_b)):
        return first, second

    # Each parameter tracks its own counter
    assert use_both_counters() == ("A_1", "B_1")
    assert use_both_counters() == ("A_2", "B_2")

    # Can override one while the other still works
    assert use_both_counters(first="fixed") == ("fixed", "B_3")


def test_multiple_isolated_parameters_create_separate_copies():
    """Test that multiple Isolated parameters create independent deep copies"""

    @smart_args
    def modify_both(*, list_data=Isolated, dict_data=Isolated):
        list_data.append("modified_list")
        dict_data["modified_dict"] = True
        return list_data, dict_data

    original_list = [1, 2, 3]
    original_dict = {"key": "value"}

    result_list, result_dict = modify_both(
        list_data=original_list, dict_data=original_dict
    )

    # Results show modifications
    assert result_list == [1, 2, 3, "modified_list"]
    assert result_dict == {"key": "value", "modified_dict": True}

    # Originals are unchanged
    assert original_list == [1, 2, 3]
    assert original_dict == {"key": "value"}


def test_regular_default_values_still_work():
    """Test that normal default values continue to work with smart_args"""

    @smart_args
    def normal_function(*, a=5, b=10):
        return a + b

    # Uses defaults
    assert normal_function() == 15

    # Can override defaults
    assert normal_function(a=2) == 12
    assert normal_function(a=1, b=1) == 2
