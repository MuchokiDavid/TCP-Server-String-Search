"""
Search algorithms module for string matching operations.
Contains various search algorithms implementations for finding strings in content.
"""

import bisect
import math
from typing import List, Optional, Union, Set
import warnings
from time import perf_counter

from . import config_loader

# Load the configuration using the `config_loader`
CONFIG: dict = config_loader.load_config()
DEBUG: bool = CONFIG["debug"]
MAX_TIMES = {
    'cached': 0.5,    # milliseconds
    'uncached': 40.0   # milliseconds
}


def linear_search(search_string: str, content: List[str]) -> bool:
    """
    Search for the given string in the file using linear algorithm.

    Arg:
        search_string (str)-> The string being searched.
        content (List[str])-> List of strings being searched

    Return:
        bool: True if found, False otherwise.
    """
    for line in content:
        if line.strip() == search_string:
            return True
    return False


def binary_search(search_string: str, content: List[str]) -> bool:
    """
    Search for the given string in the file using binary search algorithm.

    Arg:
        search_string (str)-> The string being searched.
        content (List[str])-> List of strings being searched

    Return:
        bool: True if found, False otherwise.
    """
    # Flatten if needed
    flat_content: List[str] = [
        item if isinstance(item, str) else item[0] for item in content
    ]

    # Sort content
    sorted_content: List[str] = sorted(flat_content)

    # Use bisect to find index
    index = bisect.bisect_left(sorted_content, search_string)
    return index != len(sorted_content) and sorted_content[index] == search_string

def jump_search(search_string: str, content: List[str]) -> Optional[bool]:
    """
    Search for the given string in the file using jump search algorithm.

    Arg:
        search_string (str)-> The string being searched.
        content (List[str])-> List of strings being searched

    Return:
        bool: True if found, False otherwise.
    """
    n: int = len(content)
    block_size: int = int(math.sqrt(n))
    prev: int = 0
    curr: int = 0
    content = sorted(content)

    # Jump ahead to find the block where the element may be present
    while curr < n and content[curr] <= search_string:
        prev = curr
        curr += block_size
        if curr >= n:
            curr = min(curr, n)

    # Perform a linear search within the block
    for i in range(prev, curr):
        if content[i] == search_string:
            return True

    return False

def search_in_set(search_item: Union[str, list], content: List[str]) -> bool:
    """
    Checks if a given item exists in the set.

    Args:
        search_item (Union[str, list]): Item to search for.
        content (List[str]): List of strings.

    Returns:
        bool: True if found, False otherwise.
    """
    if content:
        content = sorted(content)

    data_set: Set[str] = set(content)

    # Handle the case when search_item is a list
    if isinstance(search_item, list):
        # Convert the list to a tuple (which is hashable) or search for each item
        if len(search_item) == 1:
            return search_item[0] in data_set
        # If it's a multi-item list, we need to decide how to handle it
        # Example: Check if any item in the list is in the data_set
        return any(item in data_set for item in search_item)

    return search_item in data_set


def exponential_search(search_string: str, content: List[str]) -> bool:
    """
    Perform exponential search to find the target value in the given sorted list.

    Parameters:
        content (List[str]): The list to be searched.
        search_string (str): The value to be searched for.

    Returns:
        bool: True if found, False otherwise.
    """
    content = sorted(content)
    if not content:
        return False

    if content[0] == search_string:
        return True

    i = 1
    while i < len(content) and content[i] <= search_string:
        i *= 2

    result: bool = binary_search(search_string, content[i // 2 : min(i, len(content))])
    return result
