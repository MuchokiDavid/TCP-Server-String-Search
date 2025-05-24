"""
Summary of the benchmark tests for search algorithms.
This module includes tests for linear search, binary search, jump search,
search in set, and exponential search algorithms.
Each test uses pytest-benchmark to measure performance against a sample dataset.
The sample content is loaded from a file, and the target string is selected
from the middle of the content to ensure it exists.
The tests assert that the search algorithms return True when the target string is found.
"""
import os
import pytest

from server.server.search_algorithms import (
    linear_search,
    binary_search,
    jump_search,
    search_in_set,
    exponential_search
)

# Load sample content for benchmarking
@pytest.fixture(scope="module")
def sample_content():
    """
    Load sample content from a file for benchmarking.
    Returns:
        List[str]: List of strings from the file, excluding empty lines.
    """
    # Ensure the test file exists in the expected location
    # Adjust the path as necessary for your project structure
    test_file_path = os.path.join(os.path.dirname(__file__), "testdata/sample.txt")
    assert os.path.exists(test_file_path)
    with open(test_file_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# Target search string that should exist in the content
@pytest.fixture(scope="module")
def target_string(sample_content):
    """
    Select a target string from the sample content for benchmarking.
    Returns:
        str: A string from the middle of the sample content.
    """
    return sample_content[len(sample_content) // 2]  # Pick a middle string


def test_linear_search_benchmark(benchmark, sample_content, target_string):
    """
    Benchmark test for linear search algorithm.
    Args:
        benchmark: pytest-benchmark fixture for measuring performance.
        sample_content: List[str]: List of strings to search in.
        target_string: str: String to search for.
    """
    result = benchmark(lambda: linear_search(target_string, sample_content))
    assert result is True

def test_binary_search_benchmark(benchmark, sample_content, target_string):
    """ Benchmark test for binary search algorithm.
    Args:
        benchmark: pytest-benchmark fixture for measuring performance.
        sample_content: List[str]: List of strings to search in.
        target_string: str: String to search for.
    """
    result = benchmark(lambda: binary_search(target_string, sample_content))
    assert result is True

def test_jump_search_benchmark(benchmark, sample_content, target_string):
    """ Benchmark test for jump search algorithm.
    Args:
        benchmark: pytest-benchmark fixture for measuring performance.
        sample_content: List[str]: List of strings to search in.
        target_string: str: String to search for.
    """
    result = benchmark(lambda: jump_search(target_string, sample_content))
    assert result is True

def test_search_in_set_benchmark(benchmark, sample_content, target_string):
    """ Benchmark test for search in set algorithm.
    Args:
        benchmark: pytest-benchmark fixture for measuring performance.
        sample_content: List[str]: List of strings to search in.
        target_string: str: String to search for.
    """
    result = benchmark(lambda: search_in_set(target_string, sample_content))
    assert result is True

def test_exponential_search_benchmark(benchmark, sample_content, target_string):
    """ Benchmark test for exponential search algorithm.
    Args:
        benchmark: pytest-benchmark fixture for measuring performance.
        sample_content: List[str]: List of strings to search in.
        target_string: str: String to search for.
    """
    result = benchmark(lambda: exponential_search(target_string, sample_content))
    assert result is True
