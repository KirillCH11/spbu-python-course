import pytest
import threading
import multiprocessing as mp
from typing import Any, List

from project.thread_safe_hash_table import ThreadSafeHashTable


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
        keys = list(table)
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


def test_table_iteration_through_buckets() -> None:
    """Test iteration goes through buckets properly (behavioral check)."""
    table = ThreadSafeHashTable(size=2)
    table["a"] = 1
    table["b"] = 2
    table["c"] = 3
    keys_forward = list(table)
    assert set(keys_forward) == {"a", "b", "c"}


def test_concurrent_insertions_strict_overlap() -> None:
    """
    Test that concurrent insertions don't lose data.
    Uses a barrier to force real-time overlap across threads.
    """
    table = ThreadSafeHashTable(size=5)
    num_threads = 5
    items_per_thread = 20
    start = threading.Barrier(num_threads)

    def insert_items(thread_id: int) -> None:
        start.wait()
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


def test_concurrent_insertions_and_deletions() -> None:
    """
    Test mixed operations: some threads insert, others delete.
    Threads overlap on the same key set to stress per-bucket locks.
    """
    table = ThreadSafeHashTable(size=5)
    common_keys = [f"k{i}" for i in range(60)]
    start = threading.Barrier(6)

    # Pre-fill part of the keys to ensure some deletes succeed
    for k in common_keys[:30]:
        table[k] = "init"

    def inserter(tid: int) -> None:
        """Insert/update items from a shared set"""
        start.wait()
        for k in common_keys:
            table[k] = f"v{tid}"

    def deleter() -> None:
        """Delete items from the same shared set"""
        start.wait()
        for k in common_keys:
            try:
                del table[k]
            except KeyError:
                pass

    threads = []
    for i in range(3):
        threads.append(threading.Thread(target=inserter, args=(i,)))
    for _ in range(3):
        threads.append(threading.Thread(target=deleter))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Consistency: either key is absent, or it is readable
    for k in common_keys:
        if k in table:
            _ = table[k]
        else:
            with pytest.raises(KeyError):
                _ = table[k]


def test_concurrent_access_under_contention() -> None:
    """
    Test high contention scenario where many threads access few buckets.
    Forces frequent locking but must remain consistent and not crash.
    """
    table = ThreadSafeHashTable(size=2)  # Only 2 buckets = high contention
    hot_keys = ["a", "b", "c"]
    start = threading.Barrier(6)

    def worker(tid: int) -> None:
        """All threads work on the same small set of keys"""
        start.wait()
        for i in range(200):
            k = hot_keys[i % len(hot_keys)]
            op = i % 3
            if op == 0:
                table[k] = f"{tid}:{i}"
            elif op == 1:
                if k in table:
                    _ = table[k]
            else:
                if k in table:
                    try:
                        del table[k]
                    except KeyError:
                        pass

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    final_size = len(table)
    assert isinstance(final_size, int) and final_size >= 0
    # Iteration and reverse iteration should not raise
    _ = list(table)
    _ = list(table.reverse_iter())


# Global reference for multiprocessing worker (avoid pickling the table)
_MP_TABLE_REF = None


def _proc_worker_mp_use_global(wid: int, count: int) -> None:
    """
    Top-level worker for multiprocessing test.
    Uses a global reference to the Manager-backed table to avoid pickling errors.
    """
    table = _MP_TABLE_REF
    for i in range(count):
        k = f"w{wid}_{i}"
        table[k] = f"val{wid}_{i}"
        assert table[k] == f"val{wid}_{i}"
        if i > 0:
            _ = k in table


def test_real_multiprocessing_support() -> None:
    """
    Test that hash table works in multi-process environment.
    Processes should see each other's changes via Manager-backed storage.
    """
    global _MP_TABLE_REF
    table = ThreadSafeHashTable(size=8)
    _MP_TABLE_REF = table  # expose proxy to child processes

    per_proc = 40
    procs = [
        mp.Process(target=_proc_worker_mp_use_global, args=(i, per_proc))
        for i in range(4)
    ]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
        assert p.exitcode == 0

    for w in range(4):
        for i in range(per_proc):
            k = f"w{w}_{i}"
            assert k in table
            assert table[k] == f"val{w}_{i}"


def test_len_consistency_after_parallel_changes() -> None:
    """
    Ensure the length counter does not leak and matches actual presence after parallel changes.
    """
    table = ThreadSafeHashTable(size=8)
    N = 200
    keys = [f"k{i}" for i in range(N)]
    for k in keys:
        table[k] = 0

    start = threading.Barrier(6)

    def toggler() -> None:
        """Toggle between set and delete on the same key set"""
        start.wait()
        for k in keys:
            if (hash(k) & 1) == 0:
                table[k] = 1
            else:
                try:
                    del table[k]
                except KeyError:
                    pass

    threads = [threading.Thread(target=toggler) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # length must be non-negative integer and equal to actual number of contained keys
    assert len(table) >= 0
    present = sum(1 for k in keys if k in table)
    assert len(table) == present
