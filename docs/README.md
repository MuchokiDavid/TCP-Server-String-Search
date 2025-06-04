# String Match Server Documentation

## Performance Requirements

The string match server must meet the following performance thresholds:

- **Cached Mode** (REREAD_ON_QUERY = False): < 0.5 milliseconds per search
- **Uncached Mode** (REREAD_ON_QUERY = True): < 40.0 milliseconds per search

## Performance Analysis

The [performance comparison chart](algorithm_performance_chart.png) shows how each search algorithm performs against these thresholds.

To generate updated performance charts:

```bash
# Run the performance chart generator
./tests/generate_performance_chart.py
```

## Key Findings

- All implemented search algorithms meet both the cached and uncached thresholds
- HashSet Search (search_in_set) is the fastest algorithm
- Even the slowest algorithm (linear search) performs well within the required thresholds

## Algorithm Comparison

See [performance_summary.md](performance_summary.md) for detailed metrics on each algorithm's performance relative to the required thresholds.