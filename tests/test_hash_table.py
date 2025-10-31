import pytest
from project.hash_table import HashTable, LinkedList


class TestHashTable:
    """Test cases for HashTable class."""

    def test_basic_operations(self) -> None:
        """Test basic hash table operations."""
        table = HashTable()

        # Test insertion and retrieval
        table["name"] = "Kirill"
        table["age"] = 19
        table["city"] = "St. Petersburg"

        assert table["name"] == "Kirill"
        assert table["age"] == 19
        assert table["city"] == "St. Petersburg"

        # Test length
        assert len(table) == 3

        # Test contains
        assert "name" in table
        assert "country" not in table

    def test_update_value(self) -> None:
        """Test updating existing key."""
        table = HashTable()
        table["key"] = "old_value"
        table["key"] = "new_value"  # Update

        assert table["key"] == "new_value"
        assert len(table) == 1  # Length should not change

    def test_key_error(self) -> None:
        """Test KeyError for non-existent keys."""
        table = HashTable()

        with pytest.raises(KeyError):
            _ = table["nonexistent"]

        with pytest.raises(KeyError):
            del table["nonexistent"]

    def test_deletion(self) -> None:
        """Test element deletion."""
        table = HashTable()
        table["a"] = 1
        table["b"] = 2

        del table["a"]

        assert "a" not in table
        assert "b" in table
        assert len(table) == 1

    def test_collision_resolution(self) -> None:
        """
        Test collision resolution with small table size.

        This test forces collisions by using a very small table size (2).
        Multiple keys will hash to the same bucket, testing the linked list.
        """
        table = HashTable(size=2)  # Small size to guarantee collisions

        # These keys will likely collide in 2 buckets
        table["x"] = 1
        table["y"] = 2
        table["z"] = 3
        table["w"] = 4

        # Verify all values can be retrieved correctly
        assert table["x"] == 1
        assert table["y"] == 2
        assert table["z"] == 3
        assert table["w"] == 4

        # Verify length is correct
        assert len(table) == 4

        # Verify all keys are accessible
        assert "x" in table
        assert "y" in table
        assert "z" in table
        assert "w" in table

        # Test deletion with collisions
        del table["y"]
        assert "y" not in table
        assert len(table) == 3
        assert table["x"] == 1  # Other keys should still work
        assert table["z"] == 3
        assert table["w"] == 4

    def test_iteration(self) -> None:
        """Test forward iteration."""
        table = HashTable()
        table["a"] = 1
        table["b"] = 2
        table["c"] = 3

        keys = []
        for key in table:
            keys.append(key)

        assert set(keys) == {"a", "b", "c"}

    def test_keys_values_items(self) -> None:
        """Test keys(), values(), and items() methods."""
        table = HashTable()
        table["a"] = 1
        table["b"] = 2

        assert set(table.keys()) == {"a", "b"}
        assert set(table.values()) == {1, 2}
        assert set(table.items()) == {("a", 1), ("b", 2)}

    def test_empty_table(self) -> None:
        """Test behavior of empty hash table."""
        table = HashTable()

        assert len(table) == 0
        assert list(table) == []
        assert table.keys() == []
        assert table.values() == []
        assert table.items() == []


class TestLinkedList:
    """Test cases for LinkedList class."""

    def test_linked_list_operations(self) -> None:
        """Test basic linked list operations."""
        lst = LinkedList()

        # Test insertion
        assert lst.insert("a", 1) == True
        assert lst.insert("b", 2) == True
        assert lst.insert("a", 3) == False  # Update existing

        # Test find
        assert lst.find("a") == 3
        assert lst.find("b") == 2
        assert lst.find("c") is None

        # Test remove
        assert lst.remove("a") == True
        assert lst.remove("c") == False
        assert lst.find("a") is None

    def test_forward_iteration(self) -> None:
        """Test forward iteration in linked list."""
        lst = LinkedList()
        lst.insert("a", 1)
        lst.insert("b", 2)
        lst.insert("c", 3)

        keys = list(lst)
        assert keys == ["a", "b", "c"]

    def test_reverse_iteration(self) -> None:
        """Test reverse iteration in linked list."""
        lst = LinkedList()
        lst.insert("a", 1)
        lst.insert("b", 2)
        lst.insert("c", 3)

        keys = list(lst.reverse_iter())
        assert keys == ["c", "b", "a"]

    def test_empty_list(self) -> None:
        """Test behavior of empty linked list."""
        lst = LinkedList()

        assert list(lst) == []
        assert list(lst.reverse_iter()) == []
        assert lst.find("any") is None
        assert lst.remove("any") == False


def test_doubly_linked_table_structure():
    """Test that hash table uses doubly linked lists for buckets."""
    table = HashTable(size=3)

    # Check that buckets are connected in a doubly linked list
    assert table.buckets.head is not None
    assert table.buckets.tail is not None

    # Check connections between buckets
    bucket1 = table.buckets.head
    bucket2 = bucket1.next
    bucket3 = bucket2.next

    assert bucket1.index == 0
    assert bucket2.index == 1
    assert bucket3.index == 2

    # Check reverse connections
    assert bucket3.prev == bucket2
    assert bucket2.prev == bucket1
    assert bucket1.prev is None

    # Check data operations work correctly
    table["test"] = "value"
    assert "test" in table
    assert table["test"] == "value"


def test_table_iteration_through_linked_buckets():
    """Test iteration goes through linked buckets properly."""
    table = HashTable(size=2)

    table["a"] = 1
    table["b"] = 2
    table["c"] = 3

    # Forward iteration through doubly linked lists
    keys_forward = list(table)
    keys_reverse = list(table.reverse_iter())

    assert set(keys_forward) == {"a", "b", "c"}
    assert set(keys_reverse) == {"a", "b", "c"}
