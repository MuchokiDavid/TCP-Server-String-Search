#!/usr/bin/env python3
"""
Simple script to generate a performance comparison chart for search algorithms.
"""
import json
import subprocess
import matplotlib.pyplot as plt
from pathlib import Path

# Define thresholds
THRESHOLDS = {
    'cached': 0.5,    # milliseconds
    'uncached': 40.0  # milliseconds
}

def main():
    """Run benchmarks and generate chart."""
    # Run pytest benchmark
    subprocess.run([
        "pytest", "tests/test_benchmark.py", 
        "--benchmark-json=benchmark_results.json"
    ], check=True)
    
    # Load results
    with open("benchmark_results.json", 'r') as f:
        data = json.load(f)
    
    # Extract data
    algorithms = []
    times = []
    
    for bench in data['benchmarks']:
        name = bench['name'].replace('test_', '').replace('_benchmark', '')
        time_ms = bench['stats']['mean'] * 1000  # Convert to milliseconds
        algorithms.append(name)
        times.append(time_ms)
    
    # Create chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, times, color='skyblue')
    
    # Add threshold lines
    plt.axhline(y=THRESHOLDS['cached'], color='green', linestyle='-', 
                label=f"Cached Threshold ({THRESHOLDS['cached']} ms)")
    plt.axhline(y=THRESHOLDS['uncached'], color='red', linestyle='--', 
                label=f"Uncached Threshold ({THRESHOLDS['uncached']} ms)")
    
    # Add labels
    for bar, time in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width()/2., time + 0.01,
                f'{time:.3f} ms', ha='center', va='bottom')
    
    # Format chart
    plt.xlabel('Search Algorithm')
    plt.ylabel('Time (ms)')
    plt.title('Search Algorithm Performance Comparison')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save chart
    output_dir = Path("docs")
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / "algorithm_performance_chart.png")
    
    # Create simple report
    with open(output_dir / "performance_summary.md", 'w') as f:
        f.write("# Algorithm Performance Summary\n\n")
        f.write("| Algorithm | Time (ms) | Meets Cached (<0.5ms) | Meets Uncached (<40ms) |\n")
        f.write("|-----------|----------|---------------------|---------------------|\n")
        
        for algo, time in zip(algorithms, times):
            cached = "✓" if time < THRESHOLDS['cached'] else "✗"
            uncached = "✓" if time < THRESHOLDS['uncached'] else "✗"
            f.write(f"| {algo} | {time:.3f} | {cached} | {uncached} |\n")
        
        f.write("\n![Performance Chart](algorithm_performance_chart.png)\n")
    
    print("Chart and summary created in docs/ directory")

if __name__ == "__main__":
    main()