#!/usr/bin/env python3
"""
Script to generate a test coverage report for the string_match_server project.
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path


def run_coverage():
    """Run pytest with coverage and generate reports."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Ensure we're in the project root directory
    os.chdir(project_root)
    
    print("Running tests with coverage...")
    
    # Run pytest with coverage
    result = subprocess.run([
        "python", "-m", "pytest",
        "--cov=server",
        "--cov-report=term",
        "--cov-report=html:coverage_html",
        "tests/"
    ], capture_output=True, text=True)
    
    # Print the test results
    print(result.stdout)
    if result.stderr:
        print("Errors:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    
    # Check if coverage report was generated
    coverage_html = project_root / "coverage_html" / "index.html"
    if coverage_html.exists():
        print(f"Coverage report generated at: {coverage_html}")
        
        # Try to open the coverage report in a browser
        try:
            webbrowser.open(f"file://{coverage_html}")
            print("Coverage report opened in browser.")
        except Exception as e:
            print(f"Could not open browser: {e}")
            print(f"Please open {coverage_html} manually.")
    else:
        print("Failed to generate coverage report.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(run_coverage())