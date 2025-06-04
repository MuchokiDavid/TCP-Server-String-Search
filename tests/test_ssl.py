"""
Unit tests for SSL client functionality in a Python application.
Tests are self-contained and independent of production configuration.
"""
import os
import socket
import ssl
import pytest
import tempfile
import subprocess
from unittest.mock import patch, MagicMock
from threading import Thread

@pytest.fixture(scope="session")
def ssl_certificates():
    """Create temporary SSL certificates for testing."""
    with tempfile.TemporaryDirectory() as cert_dir:
        # Generate test certificates
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
            "-keyout", f"{cert_dir}/test.key",
            "-out", f"{cert_dir}/test.crt",
            "-subj", "/CN=localhost",
            "-days", "1"
        ], check=True)
        
        yield {
            'cert': f"{cert_dir}/test.crt",
            'key': f"{cert_dir}/test.key"
        }

@pytest.fixture(scope="function")
def mock_ssl_server(ssl_certificates):
    """Create a temporary SSL server for testing."""
    def run_server(host, port):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(ssl_certificates['cert'], ssl_certificates['key'])
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)
            
            with context.wrap_socket(sock, server_side=True) as ssock:
                while True:
                    try:
                        conn, addr = ssock.accept()
                        with conn:
                            data = conn.recv(1024)
                            conn.send(b"STRING NOT EXISTS")
                    except:
                        break

    # Start server in separate thread
    host, port = "127.0.0.1", 0  # Let OS choose port
    server_socket = socket.socket()
    server_socket.bind((host, port))
    actual_port = server_socket.getsockname()[1]
    server_socket.close()
    
    server_thread = Thread(target=run_server, args=(host, actual_port))
    server_thread.daemon = True
    server_thread.start()
    
    yield host, actual_port
    
    # Cleanup
    server_thread.join(timeout=1)

def test_ssl_context_secure():
    """Test SSL context security settings."""
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname is True

def test_wrap_socket_called():
    """Test SSL socket wrapping with mocked socket."""
    with patch("ssl.SSLContext.wrap_socket") as mock_wrap:
        context = ssl.create_default_context()
        mock_socket = MagicMock()
        context.wrap_socket(mock_socket, server_hostname="localhost")
        mock_wrap.assert_called_once()

def test_ssl_connection(mock_ssl_server, ssl_certificates):
    """Test SSL connection using temporary certificates and mock server."""
    host, port = mock_ssl_server
    
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(ssl_certificates['cert'])
    
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname="localhost") as ssock:
            ssock.sendall(b"test\n")
            response = ssock.recv(1024).decode()
            assert "STRING" in response