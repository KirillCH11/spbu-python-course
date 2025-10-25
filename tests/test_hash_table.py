import pytest
from project.hash_table import HashTable


class TestHashTable:
    def test_basic_operations(self):
        """Test basic hash table operations"""
        table = HashTable()

        table["name"] = "Kirill"
        table["age"] = 19
        table["city"] = "St. Petersburg"

        assert table["name"] == "Kirill"
        assert table["age"] == 19
        assert table["city"] == "St. Petersburg"

        assert len(table) == 3

        assert "name" in table
        assert "country" not in table

    def test_update_value(self):
        """Test value update functionality"""
        table = HashTable()
        table["key"] = "old_value"
        table["key"] = "new_value"

        assert table["key"] == "new_value"
        assert len(table) == 1

    def test_key_error(self):
        """Test KeyError for non-existent keys"""
        table = HashTable()

        with pytest.raises(KeyError):
            _ = table["nonexistent"]

        with pytest.raises(KeyError):
            del table["nonexistent"]

    def test_deletion(self):
        """Test element deletion"""
        table = HashTable()
        table["a"] = 1
        table["b"] = 2

        del table["a"]

        assert "a" not in table
        assert "b" in table
        assert len(table) == 1

    def test_collision_resolution(self):
        """Test collision resolution mechanism"""
        table = HashTable(size=2)

        table["x"] = 1
        table["y"] = 2
        table["z"] = 3

        assert table["x"] == 1
        assert table["y"] == 2
        assert table["z"] == 3
        assert len(table) == 3

    def test_forward_iterator(self):
        """Test forward iterator functionality"""
        table = HashTable()
        table["a"] = 1
        table["b"] = 2
        table["c"] = 3

        keys = []
        for key in table:
            keys.append(key)

        assert set(keys) == {"a", "b", "c"}

    def test_reverse_iterator(self):
        """Test reverse iterator functionality"""
        table = HashTable()
        table["a"] = 1
        table["b"] = 2
        table["c"] = 3

        keys = []
        for key in table.reverse_iter():
            keys.append(key)

        assert set(keys) == {"a", "b", "c"}

    def test_keys_values_items(self):
        """Test keys(), values(), and items() methods"""
        table = HashTable()
        table["a"] = 1
        table["b"] = 2

        assert set(table.keys()) == {"a", "b"}
        assert set(table.values()) == {1, 2}
        assert set(table.items()) == {("a", 1), ("b", 2)}

    def test_empty_table(self):
        """Test behavior of empty hash table"""
        table = HashTable()

        assert len(table) == 0
        assert list(table) == []
        assert list(table.reverse_iter()) == []
        assert table.keys() == []
        assert table.values() == []
        assert table.items() == []
