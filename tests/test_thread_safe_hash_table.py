import pytest
import time
import threading
from multiprocessing import Process
from typing import List, Any
from project.thread_safe_hash_table import (
    ThreadSafeHashTable,
    LinkedList,
    Bucket,
    BucketList,
)


def process_worker(process_id: int, shared_table: ThreadSafeHashTable) -> None:
    """Worker function for multiprocessing test (must be at module level)."""
    for i in range(10):
        key = f"process_{process_id}_item_{i}"
        shared_table[key] = f"value_{process_id}_{i}"


class TestThreadSafeHashTable:
    """Test cases for ThreadSafeHashTable class."""

    def test_basic_operations(self) -> None:
        """Test basic thread-safe hash table operations."""
        table = ThreadSafeHashTable()

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
        table = ThreadSafeHashTable()
        table["key"] = "old_value"
        table["key"] = "new_value"  # Update

        assert table["key"] == "new_value"
        assert len(table) == 1  # Length should not change

    def test_key_error(self) -> None:
        """Test KeyError for non-existent keys."""
        table = ThreadSafeHashTable()

        with pytest.raises(KeyError):
            _ = table["nonexistent"]

        with pytest.raises(KeyError):
            del table["nonexistent"]

    def test_deletion(self) -> None:
        """Test element deletion."""
        table = ThreadSafeHashTable()
        table["a"] = 1
        table["b"] = 2

        del table["a"]

        assert "a" not in table
        assert "b" in table
        assert len(table) == 1

    def test_collision_resolution(self) -> None:
        """
        Test collision resolution with small table size.
        """
        table = ThreadSafeHashTable(size=2)  # Small size to guarantee collisions

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
        table = ThreadSafeHashTable()
        table["a"] = 1
        table["b"] = 2
        table["c"] = 3

        keys = []
        for key in table:
            keys.append(key)

        assert set(keys) == {"a", "b", "c"}

    def test_keys_values_items(self) -> None:
        """Test keys(), values(), and items() methods."""
        table = ThreadSafeHashTable()
        table["a"] = 1
        table["b"] = 2

        assert set(table.keys()) == {"a", "b"}
        assert set(table.values()) == {1, 2}
        assert set(table.items()) == {("a", 1), ("b", 2)}

    def test_empty_table(self) -> None:
        """Test behavior of empty hash table."""
        table = ThreadSafeHashTable()

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
    table = ThreadSafeHashTable(size=3)

    table["test"] = "value"
    assert "test" in table
    assert table["test"] == "value"


def test_table_iteration_through_linked_buckets():
    """Test iteration goes through linked buckets properly."""
    table = ThreadSafeHashTable(size=2)

    table["a"] = 1
    table["b"] = 2
    table["c"] = 3

    keys_forward = list(table)
    assert set(keys_forward) == {"a", "b", "c"}


def test_concurrent_insertions() -> None:
    """Test that concurrent insertions don't lose data."""
    table = ThreadSafeHashTable(size=5)
    num_threads = 5
    items_per_thread = 20

    def insert_items(thread_id: int) -> None:
        for i in range(items_per_thread):
            key = f"thread_{thread_id}_item_{i}"
            value = f"value_{thread_id}_{i}"
            table[key] = value

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=insert_items, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    expected_count = num_threads * items_per_thread
    assert len(table) == expected_count

    for i in range(num_threads):
        for j in range(items_per_thread):
            key = f"thread_{i}_item_{j}"
            assert table[key] == f"value_{i}_{j}"


def test_concurrent_updates() -> None:
    """Test that concurrent updates work correctly."""
    table = ThreadSafeHashTable(size=3)
    table["counter"] = 0
    num_threads = 10
    increments_per_thread = 10

    def increment_counter() -> None:
        for _ in range(increments_per_thread):
            table.atomic_increment("counter", 1)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    expected_final = num_threads * increments_per_thread
    assert table["counter"] == expected_final


def test_multiprocessing_support() -> None:
    """Test that hash table works with multiprocessing."""
    table = ThreadSafeHashTable(size=5)

    processes = []
    for i in range(2):
        process = Process(target=process_worker, args=(i, table))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    expected_count = 2 * 10
    assert len(table) == expected_count

    for i in range(2):
        for j in range(10):
            key = f"process_{i}_item_{j}"
            assert table[key] == f"value_{i}_{j}"
