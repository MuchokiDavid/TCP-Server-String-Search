"""
Pytest configuration file with shared fixtures.
"""
import os
import pytest
import tempfile
import shutil


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def sample_data_file(test_data_dir):
    """Create a sample data file for testing."""
    file_path = os.path.join(test_data_dir, "sample_data.txt")
    with open(file_path, "w") as f:
        f.write("\n".join([
            "apple",
            "banana",
            "cherry",
            "date",
            "elderberry",
            "fig",
            "grape",
            "honeydew",
            "kiwi",
            "lemon"
        ]))
    return file_path


@pytest.fixture(scope="session")
def ssl_test_files(test_data_dir):
    """Create temporary SSL certificate and key files for testing."""
    import subprocess
    
    cert_path = os.path.join(test_data_dir, "test.crt")
    key_path = os.path.join(test_data_dir, "test.key")
    
    # Generate self-signed certificate for testing
    subprocess.run([
        "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
        "-keyout", key_path,
        "-out", cert_path,
        "-subj", "/CN=localhost",
        "-days", "1"
    ], check=True)
    
    return {"cert": cert_path, "key": key_path}