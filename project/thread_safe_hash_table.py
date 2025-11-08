from typing import Any, List, Tuple, Iterator, Optional, Dict
from multiprocessing import Manager


class ThreadSafeHashTable:
    """
    A thread-safe hash table implemented using multiprocessing Manager
    Based on the architecture from task 5 with buckets and linked lists concept
    """

    def __init__(self, size: int = 10) -> None:
        """
        Initialize thread-safe hash table with specified size

        Args:
            size: Number of buckets in the hash table
        """
        self.size: int = size
        self.manager = Manager()

        self._length = self.manager.Value("i", 0)

        # Use Any for Manager objects, as they have specific types
        self.buckets: Any = self.manager.list()
        self.bucket_locks: Any = self.manager.list()

        for i in range(size):
            # Each bucket stores key-value pairs and maintains order for iteration
            bucket_data: Dict[str, Any] = {
                "data": self.manager.dict(),
                "key_order": self.manager.list(),
            }
            self.buckets.append(bucket_data)
            self.bucket_locks.append(self.manager.Lock())

        # Protects only the length counter; per-bucket locks protect writes
        self.global_lock = self.manager.Lock()

    def _hash(self, key: Any) -> int:
        """
        Compute bucket index for a key.

        Args:
            key: Key to hash

        Returns:
            Bucket index between 0 and size-1
        """
        return hash(key) % self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set key-value pair. Supports table[key] = value syntax

        Args:
            key: Key to set
            value: Value to associate with key
        """
        index: int = self._hash(key)

        # Writes use per-bucket lock
        with self.bucket_locks[index]:
            bucket = self.buckets[index]
            data_dict = bucket["data"]
            key_order_list = bucket["key_order"]

            is_new = key not in data_dict
            data_dict[key] = value
            if is_new:
                key_order_list.append(key)
                with self.global_lock:
                    self._length.value += 1

    def __getitem__(self, key: Any) -> Any:
        """
        Get value for key. Supports value = table[key] syntax

        Args:
            key: Key to look up

        Returns:
            Value associated with key

        Raises:
            KeyError: If key is not found
        """
        index: int = self._hash(key)

        # Lock-free reads (reading does not mutate data)
        bucket = self.buckets[index]
        data_dict = bucket["data"]
        if key not in data_dict:
            raise KeyError(f"Key '{key}' not found")
        return data_dict[key]

    def __delitem__(self, key: Any) -> None:
        """
        Delete key-value pair. Supports del table[key] syntax.

        Args:
            key: Key to delete

        Raises:
            KeyError: If key is not found
        """
        index: int = self._hash(key)

        # Deletes use per-bucket lock
        with self.bucket_locks[index]:
            bucket = self.buckets[index]
            data_dict = bucket["data"]
            key_order_list = bucket["key_order"]

            if key not in data_dict:
                raise KeyError(f"Key '{key}' not found")

            del data_dict[key]

            # manager.list remove is linear, acceptable here
            if key in key_order_list:
                key_order_list.remove(key)

            with self.global_lock:
                self._length.value -= 1

    def __contains__(self, key: Any) -> bool:
        """
        Check if key exists. Supports key in table syntax.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise
        """
        index: int = self._hash(key)

        # Lock-free reads
        bucket = self.buckets[index]
        data_dict = bucket["data"]
        return key in data_dict

    def __len__(self) -> int:
        """
        Get number of key-value pairs.

        Returns:
            Number of elements in hash table
        """
        return self._length.value

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over keys in hash table (forward direction through buckets).

        Returns:
            Iterator over all keys
        """
        # Snapshot iteration to avoid long-held locks during traversal
        all_keys: List[Any] = []
        for i in range(self.size):
            bucket = self.buckets[i]
            key_order_list = bucket["key_order"]
            all_keys.extend(list(key_order_list))

        for key in all_keys:
            yield key

    def reverse_iter(self) -> Iterator[Any]:
        """
        Iterate over keys in hash table (reverse direction through buckets).

        Returns:
            Iterator over all keys from end to start
        """
        # Reverse snapshot without holding per-bucket locks
        all_keys: List[Any] = []
        for i in range(self.size - 1, -1, -1):
            bucket = self.buckets[i]
            key_order_list = bucket["key_order"]
            reversed_keys = list(key_order_list)
            reversed_keys.reverse()
            all_keys.extend(reversed_keys)

        for key in all_keys:
            yield key

    def keys(self) -> List[Any]:
        """
        Get all keys in hash table.

        Returns:
            List of all keys
        """
        return list(self)

    def values(self) -> List[Any]:
        """
        Get all values in hash table.

        Returns:
            List of all values
        """
        return [self[key] for key in self]

    def items(self) -> List[Tuple[Any, Any]]:
        """
        Get all key-value pairs in hash table.

        Returns:
            List of (key, value) tuples
        """
        return [(key, self[key]) for key in self]
