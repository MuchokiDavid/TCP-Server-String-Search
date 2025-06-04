"""
Unit tests for search algorithms module.
"""
import pytest
from server.server.search_algorithms import (
    linear_search,
    binary_search,
    jump_search,
    search_in_set,
    exponential_search
)


class TestSearchAlgorithms:
    """Test class for search algorithms."""

    @pytest.fixture
    def sample_data(self):
        """Fixture providing sample data for testing search algorithms."""
        return [
            "apple",
            "banana",
            "cherry",
            "date",
            "elderberry",
            "fig",
            "grape",
            "honeydew",
            "kiwi",
            "lemon"
        ]

    def test_linear_search_found(self, sample_data):
        """Test linear search when target exists."""
        assert linear_search("cherry", sample_data) is True

    def test_linear_search_not_found(self, sample_data):
        """Test linear search when target doesn't exist."""
        assert linear_search("mango", sample_data) is False

    def test_binary_search_found(self, sample_data):
        """Test binary search when target exists."""
        assert binary_search("cherry", sample_data) is True

    def test_binary_search_not_found(self, sample_data):
        """Test binary search when target doesn't exist."""
        assert binary_search("mango", sample_data) is False

    def test_jump_search_found(self, sample_data):
        """Test jump search when target exists."""
        assert jump_search("cherry", sample_data) is True

    def test_jump_search_not_found(self, sample_data):
        """Test jump search when target doesn't exist."""
        assert jump_search("mango", sample_data) is False

    def test_search_in_set_found(self, sample_data):
        """Test set search when target exists."""
        assert search_in_set("cherry", sample_data) is True

    def test_search_in_set_not_found(self, sample_data):
        """Test set search when target doesn't exist."""
        assert search_in_set("mango", sample_data) is False

    def test_search_in_set_with_list(self, sample_data):
        """Test set search with a list of items."""
        assert search_in_set(["cherry"], sample_data) is True
        assert search_in_set(["mango"], sample_data) is False
        assert search_in_set(["cherry", "banana"], sample_data) is True
        assert search_in_set(["mango", "orange"], sample_data) is False

    def test_exponential_search_found(self, sample_data):
        """Test exponential search when target exists."""
        assert exponential_search("cherry", sample_data) is True

    def test_exponential_search_not_found(self, sample_data):
        """Test exponential search when target doesn't exist."""
        assert exponential_search("mango", sample_data) is False

    def test_empty_data(self):
        """Test all search algorithms with empty data."""
        empty_data = []
        assert linear_search("test", empty_data) is False
        assert binary_search("test", empty_data) is False
        assert jump_search("test", empty_data) is False
        assert search_in_set("test", empty_data) is False
        assert exponential_search("test", empty_data) is False

    def test_edge_cases(self):
        """Test edge cases for search algorithms."""
        single_item = ["test"]
        
        # Test with single item list
        assert linear_search("test", single_item) is True
        assert binary_search("test", single_item) is True
        assert jump_search("test", single_item) is True
        assert search_in_set("test", single_item) is True
        assert exponential_search("test", single_item) is True
        
        # Test with first and last items
        data = ["first", "middle", "last"]
        assert linear_search("first", data) is True
        assert linear_search("last", data) is True
        assert binary_search("first", data) is True
        assert binary_search("last", data) is True
        assert jump_search("first", data) is True
        assert jump_search("last", data) is True
        assert exponential_search("first", data) is True
        assert exponential_search("last", data) is True