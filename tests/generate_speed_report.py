#!/usr/bin/env python3
"""
Script to generate a comprehensive speed report with charts for the string match server.
This addresses the review comments about missing charts and threshold alignment.
"""
import json
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
from datetime import datetime

# Define thresholds from search_algorithms.py
THRESHOLDS = {
    'cached': 0.5,    # milliseconds
    'uncached': 40.0  # milliseconds
}

def run_benchmarks():
    """Run benchmarks on all search algorithms."""
    print("Running benchmarks on all search algorithms...")
    result = subprocess.run([
        "pytest", "tests/test_benchmark.py", 
        "--benchmark-json=benchmark_results.json"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error running benchmarks:")
        print(result.stderr)
        return None
    
    with open("benchmark_results.json", 'r') as f:
        return json.load(f)

def create_bar_chart(algorithms, times, output_dir):
    """Create a bar chart comparing algorithm performance."""
    plt.figure(figsize=(10, 6))
    
    # Create bars with custom colors
    bars = plt.bar(algorithms, times, color='skyblue')
    
    # Color bars based on performance
    for i, time in enumerate(times):
        if time <= THRESHOLDS['cached'] / 2:  # Significantly better than threshold
            bars[i].set_color('#4CAF50')  # Green
        elif time <= THRESHOLDS['cached']:
            bars[i].set_color('#8BC34A')  # Light green
        else:
            bars[i].set_color('#F44336')  # Red
    
    # Add threshold lines
    plt.axhline(y=THRESHOLDS['cached'], color='green', linestyle='-', 
                label=f"Cached Threshold ({THRESHOLDS['cached']} ms)")
    plt.axhline(y=THRESHOLDS['uncached'], color='red', linestyle='--', 
                label=f"Uncached Threshold ({THRESHOLDS['uncached']} ms)")
    
    # Add value labels on bars
    for bar, time in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width()/2., time + 0.001,
                f'{time:.3f} ms', ha='center', va='bottom', fontsize=9)
    
    # Format chart
    plt.xlabel('Search Algorithm')
    plt.ylabel('Execution Time (milliseconds)')
    plt.title('Search Algorithm Performance Comparison')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save chart
    plt.savefig(output_dir / "algorithm_bar_chart.png", dpi=300)
    print(f"Bar chart saved to {output_dir / 'algorithm_bar_chart.png'}")

def create_threshold_comparison_chart(algorithms, times, output_dir):
    """Create a chart showing performance relative to thresholds."""
    plt.figure(figsize=(10, 6))
    
    # Calculate percentage of threshold used
    cached_percentages = [time / THRESHOLDS['cached'] * 100 for time in times]
    uncached_percentages = [time / THRESHOLDS['uncached'] * 100 for time in times]
    
    # Set up bar positions
    x = np.arange(len(algorithms))
    width = 0.35
    
    # Create grouped bars
    plt.bar(x - width/2, cached_percentages, width, label='% of Cached Threshold', color='#2196F3')
    plt.bar(x + width/2, uncached_percentages, width, label='% of Uncached Threshold', color='#FF9800')
    
    # Add threshold line at 100%
    plt.axhline(y=100, color='red', linestyle='--', label="Threshold Limit")
    
    # Add value labels
    for i, (cached, uncached) in enumerate(zip(cached_percentages, uncached_percentages)):
        plt.text(i - width/2, cached + 1, f'{cached:.1f}%', ha='center', va='bottom', fontsize=8)
        plt.text(i + width/2, uncached + 0.1, f'{uncached:.1f}%', ha='center', va='bottom', fontsize=8)
    
    # Format chart
    plt.xlabel('Search Algorithm')
    plt.ylabel('Percentage of Threshold Used (%)')
    plt.title('Algorithm Performance Relative to Thresholds')
    plt.xticks(x, algorithms, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save chart
    plt.savefig(output_dir / "threshold_comparison_chart.png", dpi=300)
    print(f"Threshold comparison chart saved to {output_dir / 'threshold_comparison_chart.png'}")

def generate_speed_report(benchmark_data, output_dir):
    """Generate a comprehensive speed report with charts."""
    # Extract algorithm names and times
    algorithms = []
    times = []
    
    for bench in benchmark_data['benchmarks']:
        name = bench['name'].replace('test_', '').replace('_benchmark', '')
        # Convert to milliseconds
        time_ms = bench['stats']['mean'] * 1000
        algorithms.append(name)
        times.append(time_ms)
    
    # Create charts
    create_bar_chart(algorithms, times, output_dir)
    create_threshold_comparison_chart(algorithms, times, output_dir)
    
    # Generate markdown report
    report_path = output_dir / "Speed_Report.md"
    with open(report_path, 'w') as f:
        f.write("# String Match Server Speed Report\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        f.write("## Performance Requirements\n\n")
        f.write("The string match server must meet the following performance thresholds:\n\n")
        f.write(f"- **Cached Mode** (REREAD_ON_QUERY = False): < {THRESHOLDS['cached']} milliseconds per search\n")
        f.write(f"- **Uncached Mode** (REREAD_ON_QUERY = True): < {THRESHOLDS['uncached']} milliseconds per search\n\n")
        
        f.write("## Algorithm Performance Results\n\n")
        f.write("| Algorithm | Execution Time (ms) | % of Cached Threshold | % of Uncached Threshold | Status |\n")
        f.write("|-----------|--------------------|-----------------------|-------------------------|--------|\n")
        
        for algo, time in zip(algorithms, times):
            cached_pct = time / THRESHOLDS['cached'] * 100
            uncached_pct = time / THRESHOLDS['uncached'] * 100
            
            if time <= THRESHOLDS['cached']:
                status = "✅ Meets All Requirements"
            elif time <= THRESHOLDS['uncached']:
                status = "⚠️ Meets Uncached Only"
            else:
                status = "❌ Does Not Meet Requirements"
                
            f.write(f"| {algo} | {time:.3f} | {cached_pct:.1f}% | {uncached_pct:.1f}% | {status} |\n")
        
        f.write("\n## Performance Visualization\n\n")
        f.write("### Algorithm Execution Times\n\n")
        f.write("![Algorithm Performance Chart](algorithm_bar_chart.png)\n\n")
        
        f.write("### Threshold Comparison\n\n")
        f.write("![Threshold Comparison Chart](threshold_comparison_chart.png)\n\n")
        
        f.write("## Analysis\n\n")
        
        # Find fastest and slowest algorithms
        fastest_idx = times.index(min(times))
        slowest_idx = times.index(max(times))
        
        f.write(f"- **Fastest Algorithm**: {algorithms[fastest_idx]} ({times[fastest_idx]:.3f} ms)\n")
        f.write(f"- **Slowest Algorithm**: {algorithms[slowest_idx]} ({times[slowest_idx]:.3f} ms)\n")
        f.write(f"- **Performance Ratio**: {times[slowest_idx]/times[fastest_idx]:.1f}x difference between fastest and slowest\n\n")
        
        all_meet_cached = all(t <= THRESHOLDS['cached'] for t in times)
        all_meet_uncached = all(t <= THRESHOLDS['uncached'] for t in times)
        
        if all_meet_cached:
            f.write("✅ **All algorithms meet the cached threshold requirement.**\n\n")
        elif all_meet_uncached:
            f.write("⚠️ **All algorithms meet the uncached threshold, but some don't meet the cached threshold.**\n\n")
        else:
            f.write("❌ **Some algorithms do not meet the performance requirements.**\n\n")
        
        f.write("## Conclusion\n\n")
        if all_meet_cached:
            f.write(f"The performance testing demonstrates that all implemented search algorithms perform well within the required thresholds. ")
            f.write(f"The {algorithms[fastest_idx]} algorithm provides the best performance and is recommended for production use.\n")
        else:
            f.write("Further optimization is needed to ensure all algorithms meet the performance requirements.\n")
    
    print(f"Speed report generated at {report_path}")

def main():
    """Main function to run benchmarks and generate reports."""
    # Create output directory
    output_dir = Path("docs")
    output_dir.mkdir(exist_ok=True)
    
    # Run benchmarks
    benchmark_data = run_benchmarks()
    if benchmark_data:
        # Generate report
        generate_speed_report(benchmark_data, output_dir)
        print("Speed report generation complete!")
    else:
        print("Failed to run benchmarks. Make sure pytest and pytest-benchmark are installed.")

if __name__ == "__main__":
    main()