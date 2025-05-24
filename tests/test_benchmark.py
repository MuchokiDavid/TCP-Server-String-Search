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
    test_file_path = os.path.join(os.path.dirname(__file__), "testdata/sample.txt")
    assert os.path.exists(test_file_path)
    with open(test_file_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# Target search string that should exist in the content
@pytest.fixture(scope="module")
def target_string(sample_content):
    return sample_content[len(sample_content) // 2]  # Pick a middle string


def test_linear_search_benchmark(benchmark, sample_content, target_string):
    result = benchmark(lambda: linear_search(target_string, sample_content))
    assert result is True

def test_binary_search_benchmark(benchmark, sample_content, target_string):
    result = benchmark(lambda: binary_search(target_string, sample_content))
    assert result is True

def test_jump_search_benchmark(benchmark, sample_content, target_string):
    result = benchmark(lambda: jump_search(target_string, sample_content))
    assert result is True

def test_search_in_set_benchmark(benchmark, sample_content, target_string):
    result = benchmark(lambda: search_in_set(target_string, sample_content))
    assert result is True

def test_exponential_search_benchmark(benchmark, sample_content, target_string):
    result = benchmark(lambda: exponential_search(target_string, sample_content))
    assert result is True
