#!/bin/bash
# Script to run all performance tests and generate reports

# Set Python path
export PYTHONPATH=/home/dave/develop/code/tests/string_match_server

echo "===== Running Algorithm Time Measurements ====="
python3 tests/measure_algorithm_times.py

echo -e "\n===== Generating Performance Charts ====="
python3 tests/generate_performance_chart.py

echo -e "\n===== Performance Testing Complete ====="
echo "Results available in docs/ directory"