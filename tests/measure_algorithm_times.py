#!/usr/bin/env python3
"""
Script to measure actual execution times of search algorithms.
"""
import time
import statistics
from pathlib import Path
import os

from server.server.search_algorithms import (
    linear_search,
    binary_search,
    jump_search,
    search_in_set,
    exponential_search
)

# Number of iterations for more accurate timing
ITERATIONS = 1000

def load_test_data():
    """Load test data from the sample file."""
    test_file_path = os.path.join(os.path.dirname(__file__), "testdata/sample.txt")
    with open(test_file_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def measure_algorithm(algorithm, data, target):
    """Measure execution time of an algorithm."""
    times = []
    
    for _ in range(ITERATIONS):
        start_time = time.perf_counter()
        result = algorithm(target, data)
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convert to milliseconds
    
    return {
        "min": min(times),
        "max": max(times),
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "found": result
    }

def main():
    """Run timing measurements for all algorithms."""
    # Load test data
    data = load_test_data()
    
    # Select target string (middle of data)
    target = data[len(data) // 2]
    
    # Define algorithms to test
    algorithms = {
        "Linear Search": linear_search,
        "Binary Search": binary_search,
        "Jump Search": jump_search,
        "HashSet Search": search_in_set,
        "Exponential Search": exponential_search
    }
    
    # Run measurements
    results = {}
    for name, algorithm in algorithms.items():
        print(f"Measuring {name}...")
        results[name] = measure_algorithm(algorithm, data, target)
    
    # Print results
    print("\nAlgorithm Performance Results (milliseconds):")
    print("-" * 80)
    print(f"{'Algorithm':<20} {'Mean':>10} {'Median':>10} {'Min':>10} {'Max':>10} {'Found':>10}")
    print("-" * 80)
    
    for name, stats in results.items():
        print(f"{name:<20} {stats['mean']:>10.6f} {stats['median']:>10.6f} {stats['min']:>10.6f} {stats['max']:>10.6f} {stats['found']:>10}")
    
    # Thresholds from search_algorithms.py
    cached_threshold = 0.5    # milliseconds
    uncached_threshold = 40.0  # milliseconds
    
    print("\nThreshold Analysis:")
    print("-" * 80)
    print(f"{'Algorithm':<20} {'Mean (ms)':>10} {'% of Cached':>12} {'% of Uncached':>14} {'Status':>20}")
    print("-" * 80)
    
    for name, stats in results.items():
        mean = stats['mean']
        cached_pct = (mean / cached_threshold) * 100
        uncached_pct = (mean / uncached_threshold) * 100
        
        if mean <= cached_threshold:
            status = "✓ Meets All"
        elif mean <= uncached_threshold:
            status = "! Meets Uncached Only"
        else:
            status = "✗ Fails Both"
            
        print(f"{name:<20} {mean:>10.6f} {cached_pct:>12.2f}% {uncached_pct:>14.2f}% {status:>20}")

if __name__ == "__main__":
    main()