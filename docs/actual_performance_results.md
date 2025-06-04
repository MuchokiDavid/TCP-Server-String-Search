# Actual Algorithm Performance Results

## Measurement Methodology

- **Test Environment**: Local development environment
- **Sample Size**: 1000 iterations per algorithm
- **Test Data**: Sample text file with 24 entries
- **Target String**: Middle entry in the sample data
- **Measurement**: Time in milliseconds using high-precision timer

## Performance Results

| Algorithm | Mean (ms) | Median (ms) | Min (ms) | Max (ms) | % of Cached Threshold | % of Uncached Threshold | Status |
|-----------|-----------|-------------|----------|----------|----------------------|-------------------------|--------|
| Linear Search | 0.000756 | 0.000597 | 0.000551 | 0.022080 | 0.15% | 0.00% | ✓ Meets All |
| Binary Search | 0.001898 | 0.001620 | 0.001529 | 0.029131 | 0.38% | 0.00% | ✓ Meets All |
| Jump Search | 0.001258 | 0.001067 | 0.001024 | 0.024785 | 0.25% | 0.00% | ✓ Meets All |
| HashSet Search | 0.001723 | 0.001397 | 0.001239 | 0.029122 | 0.34% | 0.00% | ✓ Meets All |
| Exponential Search | 0.002881 | 0.002488 | 0.001915 | 0.034699 | 0.58% | 0.01% | ✓ Meets All |

## Performance Analysis

All algorithms perform exceptionally well against the required thresholds:

- **Cached Threshold** (0.5 ms): All algorithms use less than 1% of the allowed time
- **Uncached Threshold** (40 ms): All algorithms use less than 0.01% of the allowed time

### Algorithm Ranking (by mean execution time)

1. **Linear Search**: 0.000756 ms (fastest)
2. **Jump Search**: 0.001258 ms
3. **HashSet Search**: 0.001723 ms
4. **Binary Search**: 0.001898 ms
5. **Exponential Search**: 0.002881 ms (slowest)

## Observations

- **Linear Search** performed best on this small dataset, which is contrary to theoretical expectations but common with small datasets where algorithm overhead matters more than asymptotic complexity
- **Exponential Search** was the slowest, likely due to its additional overhead that doesn't provide benefits on small datasets
- All algorithms are extremely fast, with execution times in the microsecond range (0.001-0.003 ms)
- The performance difference between algorithms is negligible for practical purposes with this dataset size

## Conclusion

All implemented search algorithms significantly outperform the required thresholds. For the current dataset size, Linear Search provides the best performance, but any of the algorithms would be suitable for production use as they all perform well within the requirements.