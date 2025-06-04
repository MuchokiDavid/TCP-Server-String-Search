#!/usr/bin/env python3
"""
Script to generate performance comparison charts for search algorithms.
This script runs benchmarks on different search algorithms and generates
visual charts comparing their performance against the required thresholds.
"""
import os
import json
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Define the thresholds from search_algorithms.py
THRESHOLDS = {
    'cached': 0.5,    # milliseconds
    'uncached': 40.0  # milliseconds
}

def run_benchmarks():
    """Run pytest benchmarks and return the results."""
    project_root = Path(__file__).parent.parent
    
    # Run pytest with benchmark
    result = subprocess.run([
        "python", "-m", "pytest", 
        "tests/test_benchmark.py", 
        "--benchmark-json=benchmark_results.json"
    ], cwd=project_root, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error running benchmarks:")
        print(result.stderr)
        return None
    
    # Load benchmark results
    benchmark_file = project_root / "benchmark_results.json"
    if not benchmark_file.exists():
        print("Benchmark results file not found")
        return None
    
    with open(benchmark_file, 'r') as f:
        return json.load(f)

def generate_charts(benchmark_data):
    """Generate performance comparison charts from benchmark data."""
    if not benchmark_data or 'benchmarks' not in benchmark_data:
        print("No valid benchmark data found")
        return
    
    # Extract algorithm names and times
    algorithms = []
    times = []
    
    for bench in benchmark_data['benchmarks']:
        name = bench['name'].replace('test_', '').replace('_benchmark', '')
        # Convert to milliseconds for comparison with thresholds
        time_ms = bench['stats']['mean'] * 1000
        algorithms.append(name)
        times.append(time_ms)
    
    # Create the chart
    plt.figure(figsize=(12, 8))
    
    # Bar chart for algorithm comparison
    bars = plt.bar(algorithms, times, color='skyblue')
    
    # Add threshold lines
    plt.axhline(y=THRESHOLDS['cached'], color='green', linestyle='-', label=f"Cached Threshold ({THRESHOLDS['cached']} ms)")
    plt.axhline(y=THRESHOLDS['uncached'], color='red', linestyle='-', label=f"Uncached Threshold ({THRESHOLDS['uncached']} ms)")
    
    # Add value labels on top of bars
    for bar, time in zip(bars, times):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{time:.3f} ms', ha='center', va='bottom', rotation=0)
    
    # Highlight bars that meet the cached threshold
    for i, time in enumerate(times):
        if time <= THRESHOLDS['cached']:
            bars[i].set_color('lightgreen')
        elif time <= THRESHOLDS['uncached']:
            bars[i].set_color('orange')
        else:
            bars[i].set_color('salmon')
    
    # Add labels and title
    plt.xlabel('Search Algorithm')
    plt.ylabel('Execution Time (milliseconds)')
    plt.title('Search Algorithm Performance Comparison')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save the chart
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "docs"
    output_dir.mkdir(exist_ok=True)
    
    chart_path = output_dir / "algorithm_performance_chart.png"
    plt.savefig(chart_path)
    print(f"Performance chart saved to: {chart_path}")
    
    # Create a table comparing algorithms to thresholds
    create_performance_table(algorithms, times, output_dir)

def create_performance_table(algorithms, times, output_dir):
    """Create a markdown table comparing algorithm performance to thresholds."""
    with open(output_dir / "performance_comparison.md", 'w') as f:
        f.write("# Search Algorithm Performance Comparison\n\n")
        f.write("## Performance Metrics\n\n")
        f.write("| Algorithm | Execution Time (ms) | Meets Cached Threshold | Meets Uncached Threshold |\n")
        f.write("|-----------|--------------------|-----------------------|-------------------------|\n")
        
        for algo, time in zip(algorithms, times):
            meets_cached = "✅" if time <= THRESHOLDS['cached'] else "❌"
            meets_uncached = "✅" if time <= THRESHOLDS['uncached'] else "❌"
            f.write(f"| {algo} | {time:.3f} | {meets_cached} | {meets_uncached} |\n")
        
        f.write("\n\n## Threshold Requirements\n\n")
        f.write(f"- **Cached Threshold**: {THRESHOLDS['cached']} ms (for REREAD_ON_QUERY = False)\n")
        f.write(f"- **Uncached Threshold**: {THRESHOLDS['uncached']} ms (for REREAD_ON_QUERY = True)\n")
        
        f.write("\n\n## Performance Chart\n\n")
        f.write("![Algorithm Performance Chart](algorithm_performance_chart.png)\n")
    
    print(f"Performance comparison table saved to: {output_dir / 'performance_comparison.md'}")

if __name__ == "__main__":
    print("Running search algorithm benchmarks...")
    benchmark_data = run_benchmarks()
    if benchmark_data:
        print("Generating performance charts...")
        generate_charts(benchmark_data)
        print("Done!")
    else:
        print("Failed to run benchmarks. Make sure pytest and pytest-benchmark are installed.")
        print("Install with: pip install pytest pytest-benchmark matplotlib")