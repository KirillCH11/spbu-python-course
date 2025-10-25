class HashTable:
    """A simple hash table implementation using separate chaining with doubly linked lists"""

    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size
        self._length = 0

    def _hash(self, key):
        """Compute the hash value for a key"""
        return hash(key) % self.size

    def __setitem__(self, key, value):
        """Set the value for a key using table[key] = value syntax"""
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = _LinkedList()

        if self.table[index].insert(key, value):
            self._length += 1

    def __getitem__(self, key):
        """Get the value for a key using table[key] syntax"""
        index = self._hash(key)

        if self.table[index] is None:
            raise KeyError(f"Key '{key}' not found")

        value = self.table[index].find(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")

        return value

    def __delitem__(self, key):
        """Delete a key-value pair using del table[key] syntax"""
        index = self._hash(key)

        if self.table[index] is None:
            raise KeyError(f"Key '{key}' not found")

        if self.table[index].remove(key):
            self._length -= 1
        else:
            raise KeyError(f"Key '{key}' not found")

    def __contains__(self, key):
        """Check if a key exists in the hash table using 'key in table' syntax"""
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def __len__(self):
        """Return the number of key-value pairs in the hash table"""
        return self._length

    def __iter__(self):
        """Return a forward iterator for keys"""
        return self._ForwardIterator(self)

    def keys(self):
        """Return a list of all keys in the hash table"""
        return [key for key in self]

    def values(self):
        """Return a list of all values in the hash table"""
        return [self[key] for key in self]

    def items(self):
        """Return a list of all key-value pairs in the hash table"""
        return [(key, self[key]) for key in self]

    def reverse_iter(self):
        """Return a reverse iterator for keys"""
        return self._ReverseIterator(self)

    class _ForwardIterator:
        """Forward iterator for traversing the hash table"""

        def __init__(self, hash_table):
            self.hash_table = hash_table
            self.bucket_index = 0
            self.current_node = None
            self._find_first_element()

        def _find_first_element(self):
            """Find the first non-empty element in the hash table"""
            while self.bucket_index < self.hash_table.size and (
                self.hash_table.table[self.bucket_index] is None
                or self.hash_table.table[self.bucket_index].head is None
            ):
                self.bucket_index += 1

            if self.bucket_index < self.hash_table.size:
                self.current_node = self.hash_table.table[self.bucket_index].head

        def __iter__(self):
            return self

        def __next__(self):
            if self.current_node is None:
                raise StopIteration

            key = self.current_node.key
            self.current_node = self.current_node.next

            if self.current_node is None:
                self.bucket_index += 1
                self._find_first_element()

            return key

    class _ReverseIterator:
        """Reverse iterator for traversing the hash table from the end"""

        def __init__(self, hash_table):
            self.hash_table = hash_table
            self.bucket_index = hash_table.size - 1
            self.current_node = None
            self._find_last_element()

        def _find_last_element(self):
            """Find the last non-empty element in the hash table"""
            while self.bucket_index >= 0 and (
                self.hash_table.table[self.bucket_index] is None
                or self.hash_table.table[self.bucket_index].tail is None
            ):
                self.bucket_index -= 1

            if self.bucket_index >= 0:
                self.current_node = self.hash_table.table[self.bucket_index].tail

        def __iter__(self):
            return self

        def __next__(self):
            if self.current_node is None:
                raise StopIteration

            key = self.current_node.key
            self.current_node = self.current_node.prev

            if self.current_node is None:
                self.bucket_index -= 1
                self._find_last_element()

            return key


class _Node:
    """A node in the doubly linked list"""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class _LinkedList:
    """Doubly linked list for collision resolution"""

    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, key, value):
        """Insert or update a key-value pair in the list"""
        current = self.head

        while current is not None:
            if current.key == key:
                current.value = value
                return False
            current = current.next

        new_node = _Node(key, value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        return True

    def find(self, key):
        """Find a value by key in the list"""
        current = self.head

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def remove(self, key):
        """Remove a key-value pair from the list"""
        current = self.head

        while current is not None:
            if current.key == key:
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                return True

            current = current.next

        return False
