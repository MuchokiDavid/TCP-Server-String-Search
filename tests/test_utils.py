"""
Unit tests for the utils.py module.
"""
import os
import ssl
import pytest
from unittest import mock

from server.server import utils # Assuming utils.py is in server.server

# Mock constants from utils.py as they are loaded at module level
@pytest.fixture(autouse=True)
def mock_utils_constants(monkeypatch):
    monkeypatch.setattr(utils, "SSL_CERT", "dummy_cert.pem")
    monkeypatch.setattr(utils, "SSL_KEY", "dummy_key.pem") # Ensure these are mock paths
    # Mock logger to prevent actual logging during tests and allow inspection
    mock_logger = mock.MagicMock()
    monkeypatch.setattr(utils, "logger", mock_logger)
    return mock_logger

class TestCreateSecureSSLContext:

    @mock.patch("ssl.create_default_context")
    @mock.patch("os.path.exists")
    @mock.patch("server.server.utils._verify_certificate_chain") # Mock helper
    def test_create_secure_ssl_context_success(
        self, mock_verify_chain, mock_os_exists, mock_create_default_context, mock_utils_constants
    ):
        """
        Test successful creation of a secure SSL context.
        """
        mock_context_instance = mock.MagicMock(spec=ssl.SSLContext)
        mock_create_default_context.return_value = mock_context_instance
        mock_os_exists.return_value = True # Both cert and key exist

        context = utils.create_secure_ssl_context()

        mock_create_default_context.assert_called_once_with(ssl.Purpose.CLIENT_AUTH)
        assert context.minimum_version == ssl.TLSVersion.TLSv1_2
        assert context.options & ssl.OP_NO_SSLv2
        assert context.options & ssl.OP_NO_SSLv3
        assert context.options & ssl.OP_SINGLE_DH_USE
        # assert context.options & ssl.OP_SINGLE_ECDH_USE # This option might not be explicitly set if covered by ciphers
        assert context.options & ssl.OP_NO_COMPRESSION
        context.set_ciphers.assert_called_once_with(
            "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:!aNULL:!MD5:!DSS"
        )
        mock_os_exists.assert_any_call("dummy_cert.pem")
        mock_os_exists.assert_any_call("dummy_key.pem")
        context.load_cert_chain.assert_called_once_with("dummy_cert.pem", "dummy_key.pem")
        mock_verify_chain.assert_called_once_with("dummy_cert.pem")

        # Check that relevant info logs were made
        mock_utils_constants.info.assert_any_call("SSL context created with secure configuration:")
        mock_utils_constants.info.assert_any_call(f"  - Minimum TLS version: {ssl.TLSVersion.TLSv1_2}")
        mock_utils_constants.info.assert_any_call(f"  - Certificate: dummy_cert.pem")
        mock_utils_constants.info.assert_any_call(f"  - Private key: dummy_key.pem")


    @mock.patch("ssl.create_default_context")
    @mock.patch("os.path.exists")
    def test_create_secure_ssl_context_cert_not_found(
        self, mock_os_exists, mock_create_default_context, mock_utils_constants
    ):
        """
        Test FileNotFoundError when SSL certificate is not found.
        """
        mock_context_instance = mock.MagicMock(spec=ssl.SSLContext)
        mock_create_default_context.return_value = mock_context_instance
        mock_os_exists.side_effect = lambda path_arg: path_arg != "dummy_cert.pem" # Cert doesn't exist

        with pytest.raises(FileNotFoundError, match="SSL certificate file not found: dummy_cert.pem"):
            utils.create_secure_ssl_context()

        mock_utils_constants.error.assert_any_call(f"Certificate file error: SSL certificate file not found: dummy_cert.pem")


    @mock.patch("ssl.create_default_context")
    @mock.patch("os.path.exists")
    def test_create_secure_ssl_context_key_not_found(
        self, mock_os_exists, mock_create_default_context, mock_utils_constants
    ):
        """
        Test FileNotFoundError when SSL private key is not found.
        """
        mock_context_instance = mock.MagicMock(spec=ssl.SSLContext)
        mock_create_default_context.return_value = mock_context_instance
        mock_os_exists.side_effect = lambda path_arg: path_arg != "dummy_key.pem" # Key doesn't exist

        with pytest.raises(FileNotFoundError, match="SSL private key file not found: dummy_key.pem"):
            utils.create_secure_ssl_context()

        mock_utils_constants.error.assert_any_call(f"Certificate file error: SSL private key file not found: dummy_key.pem")


    @mock.patch("ssl.create_default_context")
    @mock.patch("os.path.exists")
    def test_create_secure_ssl_context_ssl_error_on_load_cert(
        self, mock_os_exists, mock_create_default_context, mock_utils_constants
    ):
        """
        Test ssl.SSLError during load_cert_chain.
        """
        mock_context_instance = mock.MagicMock(spec=ssl.SSLContext)
        mock_create_default_context.return_value = mock_context_instance
        mock_os_exists.return_value = True
        mock_context_instance.load_cert_chain.side_effect = ssl.SSLError("Failed to load certs")

        with pytest.raises(ssl.SSLError, match="Failed to load certs"):
            utils.create_secure_ssl_context()

        mock_utils_constants.error.assert_any_call("SSL context creation failed: ('Failed to load certs',)")


    @mock.patch("ssl.create_default_context")
    def test_create_secure_ssl_context_ssl_error_on_create(
        self, mock_create_default_context, mock_utils_constants
    ):
        """
        Test ssl.SSLError during ssl.create_default_context.
        """
        mock_create_default_context.side_effect = ssl.SSLError("Context creation failed")

        with pytest.raises(ssl.SSLError, match="Context creation failed"):
            utils.create_secure_ssl_context()

        mock_utils_constants.error.assert_any_call("SSL context creation failed: ('Context creation failed',)")


    @mock.patch("ssl.create_default_context")
    @mock.patch("os.path.exists")
    @mock.patch("server.server.utils._verify_certificate_chain")
    def test_create_secure_ssl_context_generic_exception(
        self, mock_verify_chain, mock_os_exists, mock_create_default_context, mock_utils_constants
    ):
        """
        Test handling of a generic Exception during SSL context setup.
        It should be caught and re-raised as an ssl.SSLError.
        """
        mock_context_instance = mock.MagicMock(spec=ssl.SSLContext)
        mock_create_default_context.return_value = mock_context_instance
        mock_os_exists.return_value = True
        # Simulate an unexpected error, e.g., during set_ciphers
        mock_context_instance.set_ciphers.side_effect = Exception("Unexpected problem")

        with pytest.raises(ssl.SSLError, match="SSL configuration failed: Unexpected problem"):
            utils.create_secure_ssl_context()

        mock_utils_constants.error.assert_any_call("Unexpected error creating SSL context: Unexpected problem")


    @mock.patch("ssl.create_default_context")
    @mock.patch("os.path.exists")
    @mock.patch("server.server.utils._verify_certificate_chain")
    def test_verify_certificate_chain_called(
        self, mock_verify_chain, mock_os_exists, mock_create_default_context
    ):
        """
        Test that _verify_certificate_chain is called.
        """
        mock_context_instance = mock.MagicMock(spec=ssl.SSLContext)
        mock_create_default_context.return_value = mock_context_instance
        mock_os_exists.return_value = True

        utils.create_secure_ssl_context()
        mock_verify_chain.assert_called_once_with("dummy_cert.pem")