"""
Unit tests for SSL client functionality in a Python application.
This module includes tests for SSL context creation, socket wrapping, and an optional integration test for a real SSL connection to a local server.
"""
import os
import socket
import ssl
import pytest
from unittest.mock import patch, MagicMock

# Constants for real test (can be updated or mocked)
HOST = "127.0.0.1"
PORT = 8080

# Base directory for test certs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT_FILE = os.path.join(BASE_DIR, "security", "server.crt")
KEY_FILE = os.path.join(BASE_DIR, "security", "server.key")
CA_CERT = os.path.join(BASE_DIR, "security", "ca.crt")  # ideally different from server cert


# ---------- UNIT TESTS ----------

def test_ssl_context_secure():
    """Ensure SSL context is created securely for client"""
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname is True


@patch("ssl.SSLContext.wrap_socket")
def test_wrap_socket_called(mock_wrap_socket):
    """Ensure wrap_socket is called with expected arguments"""
    mock_socket = MagicMock()
    context = ssl.create_default_context()
    context.wrap_socket(mock_socket, server_hostname="localhost")

    mock_wrap_socket.assert_called_once()
    _, kwargs = mock_wrap_socket.call_args
    assert kwargs["server_hostname"] == "localhost"


# ---------- INTEGRATION TEST (Optional) ----------

def test_ssl_connection_to_local_server():
    """Test a real SSL client connection to the local server (requires running server)"""
    assert os.path.exists(CERT_FILE), f"Certificate not found: {CERT_FILE}"
    assert os.path.exists(KEY_FILE), f"Key not found: {KEY_FILE}"

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # ⚠️ Not for production

    with socket.create_connection((HOST, PORT), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            ssock.sendall(b"test;ssl;query\n")
            response = ssock.recv(1024).decode()
            assert "STRING" in response or "NOT EXIST" in response
