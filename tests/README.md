# String Match Server Tests

This directory contains tests for the String Match Server project.

## Test Structure

- `test_utils.py`: Tests for utility functions
- `test_exceptions.py`: Tests for exception handling
- `test_benchmark.py`: Performance benchmarks for search algorithms
- `test_ssl.py`: Tests for SSL functionality
- `test_logging.py`: Tests for logging functionality
- `test_config_loader.py`: Tests for configuration loading
- `test_search_algorithms.py`: Tests for search algorithms
- `test_path_handling.py`: Tests for path handling across environments
- `conftest.py`: Shared pytest fixtures
- `coverage_report.py`: Script to generate test coverage reports

## Running Tests

To run all tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_utils.py
```

## Generating Coverage Reports

To generate a test coverage report:

```bash
python tests/coverage_report.py
```

This will run the tests with coverage measurement and generate an HTML report in the `coverage_html` directory.

## Test Data

Test data is stored in the `testdata` directory. The tests are designed to use this data or create temporary test data as needed.

## Environment Independence

The tests are designed to be environment-independent by:

1. Using temporary directories and files when needed
2. Using absolute paths or properly resolving relative paths
3. Using fixtures to set up and tear down test environments
4. Mocking external dependencies

## Adding New Tests

When adding new tests:

1. Follow the naming convention: `test_*.py` for test files and `test_*` for test functions
2. Use appropriate fixtures from `conftest.py`
3. Ensure tests are independent and can run in any order
4. Add appropriate assertions to verify expected behavior
5. Update this README if necessary