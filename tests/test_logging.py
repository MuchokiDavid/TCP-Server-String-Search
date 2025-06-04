"""
Unit tests for verifying logging functionality in the string match server.
"""
import logging
import pytest
from unittest.mock import patch, MagicMock

from server.server.server import StringSearchServer
from server.server.utils import create_secure_ssl_context
from server.server.exceptions import InvalidPayloadError


class TestLoggingOutput:
    """Test class for verifying logging output from various components."""

    @pytest.fixture
    def mock_logger(self):
        """Fixture to create and configure a mock logger for testing."""
        logger = MagicMock(spec=logging.Logger)
        return logger

    def test_server_logs_search_query(self, mock_logger):
        """Test that the server logs search queries properly."""
        with patch('server.server.server.logger', mock_logger):
            server = StringSearchServer()
            mock_sock = MagicMock()
            mock_sock.recv.return_value = b"test_string"
            
            # Mock methods to prevent actual execution
            server._strip_exceeding_received_data = MagicMock(return_value="test_string")
            server._search_string = MagicMock(return_value=(True, 0.5))
            server._load_file_contents = MagicMock(return_value=["test_string"])
            
            # Execute the method that should produce logs
            server.handle_client(mock_sock, ("127.0.0.1", 12345))
            
            # Verify logging calls
            mock_logger.info.assert_any_call("Search query from %s: %s", ("127.0.0.1", 12345), "test_string")
            mock_logger.info.assert_any_call("Searching for string: %s", "test_string")
            mock_logger.info.assert_any_call("%s- %s", "STRING EXISTS", "200:OK")

    def test_server_logs_error_on_invalid_payload(self, mock_logger):
        """Test that the server logs errors for invalid payloads."""
        with patch('server.server.server.logger', mock_logger):
            server = StringSearchServer()
            mock_sock = MagicMock()
            
            # Setup to trigger an error
            server._strip_exceeding_received_data = MagicMock(side_effect=InvalidPayloadError("Invalid payload"))
            
            # Execute the method that should produce error logs
            server.handle_client(mock_sock, ("127.0.0.1", 12345))
            
            # Verify error logging
            mock_logger.error.assert_called_with("Invalid payload: %s", "Invalid payload")

    def test_ssl_context_logs_configuration(self, mock_logger):
        """Test that SSL context creation logs configuration details."""
        cert_path = 'test_cert.pem'
        key_path = 'test_key.pem'
        
        with patch('server.server.utils.logger', mock_logger):
            with patch('server.server.utils.os.path.exists', return_value=True):
                with patch('server.server.utils.SSL_CERT', cert_path):
                    with patch('server.server.utils.SSL_KEY', key_path):
                        with patch('server.server.utils.ssl.create_default_context') as mock_create_context:
                            with patch('server.server.utils._verify_certificate_chain'):
                                # Setup mock SSL context
                                mock_context = MagicMock()
                                mock_create_context.return_value = mock_context
                                
                                # Call the function that should log SSL configuration
                                create_secure_ssl_context()
                                
                                # Verify the exact format of logging calls as they appear in utils.py
                                mock_logger.info.assert_any_call("SSL context created with secure configuration:")
                                # Note: f-strings in the code are converted to formatted strings in the log calls
                                mock_logger.info.assert_any_call(f"  - Certificate: {cert_path}")
                                mock_logger.info.assert_any_call(f"  - Private key: {key_path}")