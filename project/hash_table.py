from typing import Any, List, Tuple, Iterator, Optional


class HashTable:
    """
    A hash table implemented as a doubly linked list of buckets.
    Each bucket contains a doubly linked list for collision resolution.

    Supports dictionary-like interface with [] syntax.
    """

    def __init__(self, size: int = 10) -> None:
        """
        Initialize hash table with specified size.

        Args:
            size: Number of buckets in the hash table
        """
        self.size: int = size
        self.buckets: "BucketList" = BucketList(size)
        self._length: int = 0

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
        Set key-value pair. Supports table[key] = value syntax.

        Args:
            key: Key to set
            value: Value to associate with key
        """
        index: int = self._hash(key)
        bucket: "Bucket" = self.buckets.get_bucket(index)

        if bucket.collision_list.insert(key, value):
            self._length += 1

    def __getitem__(self, key: Any) -> Any:
        """
        Get value for key. Supports value = table[key] syntax.

        Args:
            key: Key to look up

        Returns:
            Value associated with key

        Raises:
            KeyError: If key is not found
        """
        index: int = self._hash(key)
        bucket: "Bucket" = self.buckets.get_bucket(index)

        value: Optional[Any] = bucket.collision_list.find(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")
        return value

    def __delitem__(self, key: Any) -> None:
        """
        Delete key-value pair. Supports del table[key] syntax.

        Args:
            key: Key to delete

        Raises:
            KeyError: If key is not found
        """
        index: int = self._hash(key)
        bucket: "Bucket" = self.buckets.get_bucket(index)

        if bucket.collision_list.remove(key):
            self._length -= 1
        else:
            raise KeyError(f"Key '{key}' not found")

    def __contains__(self, key: Any) -> bool:
        """
        Check if key exists. Supports key in table syntax.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise
        """
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        """
        Get number of key-value pairs.

        Returns:
            Number of elements in hash table
        """
        return self._length

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over keys in hash table (forward direction).

        Returns:
            Iterator over all keys
        """
        # Traversal of an external doubly linked list (buckets)
        current_bucket: Optional[Bucket] = self.buckets.head
        while current_bucket is not None:
            # Traversal of an internal doubly linked list (collisions)
            current_node: Optional[Node] = current_bucket.collision_list.head
            while current_node is not None:
                yield current_node.key
                current_node = current_node.next
            current_bucket = current_bucket.next

    def reverse_iter(self) -> Iterator[Any]:
        """
        Iterate over keys in hash table (reverse direction).

        Returns:
            Iterator over all keys from end to start
        """
        # Backtracking of an external doubly linked list (buckets)
        current_bucket: Optional[Bucket] = self.buckets.tail
        while current_bucket is not None:
            # Backtracking of an internal doubly linked list (collisions)
            current_node: Optional[Node] = current_bucket.collision_list.tail
            while current_node is not None:
                yield current_node.key
                current_node = current_node.prev
            current_bucket = current_bucket.prev

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


class Bucket:
    """
    A bucket in the hash table, representing one cell.
    Contains a doubly linked list for collision resolution.
    """

    def __init__(self, index: int) -> None:
        """
        Initialize bucket with index and empty collision list.

        Args:
            index: Index of this bucket in the table
        """
        self.index: int = index
        self.collision_list: "LinkedList" = (
            LinkedList()
        )  # An internal doubly linked list
        self.next: Optional["Bucket"] = None  # Link to the next bucket
        self.prev: Optional["Bucket"] = None  # Link to the previous bucket


class BucketList:
    """
    Outer doubly linked list representing all buckets in the hash table.
    This makes the table itself a doubly linked list.
    """

    def __init__(self, size: int) -> None:
        """
        Initialize the bucket list with specified number of buckets.

        Args:
            size: Number of buckets to create
        """
        self.head: Optional[Bucket] = None
        self.tail: Optional[Bucket] = None
        self._buckets: List[Bucket] = []  # For quick index access

        # Creating a doubly linked list of batches
        for i in range(size):
            new_bucket = Bucket(i)
            self._buckets.append(new_bucket)

            if self.head is None:
                self.head = new_bucket
                self.tail = new_bucket
            else:
                new_bucket.prev = self.tail
                if self.tail is not None:
                    self.tail.next = new_bucket
                self.tail = new_bucket

    def get_bucket(self, index: int) -> "Bucket":
        """
        Get bucket by index.

        Args:
            index: Bucket index (0 to size-1)

        Returns:
            Bucket at specified index
        """
        return self._buckets[index]


class Node:
    """
    A node in the doubly linked list for collision resolution.

    Each node stores a key-value pair and references to next and previous nodes.
    """

    def __init__(self, key: Any, value: Any) -> None:
        """
        Initialize node with key and value.

        Args:
            key: Key for the node
            value: Value for the node
        """
        self.key: Any = key
        self.value: Any = value
        self.next: Optional["Node"] = None
        self.prev: Optional["Node"] = None


class LinkedList:
    """
    Doubly linked list for collision resolution in a bucket.

    Supports forward and reverse iteration.
    """

    def __init__(self) -> None:
        """Initialize empty linked list."""
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    def insert(self, key: Any, value: Any) -> bool:
        """
        Insert or update key-value pair in list.

        Args:
            key: Key to insert or update
            value: Value to associate with key

        Returns:
            True if new key was inserted, False if existing key was updated
        """
        current: Optional[Node] = self.head

        # Search for existing key
        while current is not None:
            if current.key == key:
                current.value = value
                return False
            current = current.next

        # Key not found - insert new node
        new_node = Node(key, value)

        if self.head is None:
            # First node in list
            self.head = new_node
            self.tail = new_node
        else:
            # Append to end of list
            new_node.prev = self.tail
            if self.tail is not None:
                self.tail.next = new_node
            self.tail = new_node

        return True

    def find(self, key: Any) -> Optional[Any]:
        """
        Find value for key in list.

        Args:
            key: Key to find

        Returns:
            Value if key found, None otherwise
        """
        current: Optional[Node] = self.head

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def remove(self, key: Any) -> bool:
        """
        Remove key-value pair from list.

        Args:
            key: Key to remove

        Returns:
            True if key was found and removed, False otherwise
        """
        current: Optional[Node] = self.head

        while current is not None:
            if current.key == key:
                # Update previous node's next pointer
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                # Update next node's previous pointer
                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                return True

            current = current.next

        return False

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over keys in forward direction.

        Returns:
            Iterator over keys from head to tail
        """
        current: Optional[Node] = self.head
        while current is not None:
            yield current.key
            current = current.next

    def reverse_iter(self) -> Iterator[Any]:
        """
        Iterate over keys in reverse direction.

        Returns:
            Iterator over keys from tail to head
        """
        current: Optional[Node] = self.tail
        while current is not None:
            yield current.key
            current = current.prev
