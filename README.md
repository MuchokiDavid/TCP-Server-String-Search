# String Match Server

A high-performance server for string matching operations with support for multiple search algorithms.

## Performance Requirements

The server must meet the following performance requirements:

- **Cached Mode** (REREAD_ON_QUERY = False): Search operations must complete within 0.5 milliseconds
- **Uncached Mode** (REREAD_ON_QUERY = True): Search operations must complete within 40.0 milliseconds

## Performance Analysis

All implemented search algorithms significantly outperform the required thresholds:

| Algorithm | Mean (ms) | % of Cached Threshold | % of Uncached Threshold |
|-----------|-----------|----------------------|-------------------------|
| Linear Search | 0.000756 | 0.15% | 0.00% |
| Binary Search | 0.001898 | 0.38% | 0.00% |
| Jump Search | 0.001258 | 0.25% | 0.00% |
| HashSet Search | 0.001723 | 0.34% | 0.00% |
| Exponential Search | 0.002881 | 0.58% | 0.01% |

To run performance tests and generate visualizations:

```bash
# Run all performance tests and generate reports
./tests/run_all_performance_tests.sh
```

This will generate:
1. Actual performance measurements with 1000 iterations per algorithm
2. Performance charts comparing all algorithms
3. Detailed analysis reports

See the [actual performance results](docs/actual_performance_results.md) for detailed analysis.

## Performance Visualization

![Algorithm Performance Chart](docs/algorithm_performance_chart.png)

## Installation and Setup

See the [installation guide](install/INSTALL.md) for detailed setup instructions.

## Running Tests

```bash
# Run all tests
pytest

# Generate test coverage report
./tests/coverage_report.py
```

## SSL Configuration

See [SSL setup instructions](docs/SSL_SETUP.md) for configuring secure connections.