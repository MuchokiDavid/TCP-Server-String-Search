"""
Unit tests for the config_loader module.
"""
import os
import pytest
from unittest.mock import patch, mock_open

from server.server import config_loader


class TestConfigLoader:
    """Test class for the config_loader module."""

    @pytest.fixture
    def mock_config_path(self, tmp_path):
        """Create a temporary config file path for testing."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        config_file = config_dir / "config.ini"
        return str(config_file)

    def test_load_config_with_valid_file(self, mock_config_path):
        """Test loading a valid configuration file."""
        config_content = """
        [SERVER]
        HOST = 127.0.0.1
        PORT = 8080
        
        [REQUEST]
        MAX_PAYLOAD_SIZE = 1024
        
        [LOGGING]
        DEBUG = False
        
        [QUERY]
        REREAD_ON_QUERY = False
        
        [SSL]
        SSL_ENABLED = True
        SSL_CERT = ../security/server.crt
        SSL_KEY = ../security/server.key
        
        [FILES]
        linuxpath = ../data/10k.txt
        """
        
        with patch("builtins.open", mock_open(read_data=config_content)):
            with patch("os.path.exists", return_value=True):
                with patch.object(config_loader, "CONFIG_PATH", mock_config_path):
                    config = config_loader.load_config()
                    
                    # Verify config values
                    assert config["host"] == "127.0.0.1"
                    assert config["port"] == 8080
                    assert config["max_payload"] == 1024
                    assert config["debug"] is False
                    assert config["reread_on_query"] is False
                    assert config["ssl_enabled"] is True
                    assert config["ssl_certificate"] == "../security/server.crt"
                    assert config["ssl_private_key"] == "../security/server.key"
                    assert config["linuxpath"] == "../data/10k.txt"

    def test_load_config_file_not_found(self):
        """Test behavior when config file is not found."""
        with patch("os.path.exists", return_value=False):
            with patch.object(config_loader, "CONFIG_PATH", "/nonexistent/path"):
                with pytest.raises(FileNotFoundError):
                    config_loader.load_config()

    def test_load_config_with_environment_variables(self, mock_config_path):
        """Test that environment variables override config file values."""
        config_content = """
        [SERVER]
        HOST = 127.0.0.1
        PORT = 8080
        """
        
        env_vars = {
            "STRING_MATCH_HOST": "0.0.0.0",
            "STRING_MATCH_PORT": "9090"
        }
        
        with patch("builtins.open", mock_open(read_data=config_content)):
            with patch("os.path.exists", return_value=True):
                with patch.object(config_loader, "CONFIG_PATH", mock_config_path):
                    with patch.dict(os.environ, env_vars):
                        config = config_loader.load_config()
                        
                        # Verify environment variables override config file
                        assert config["host"] == "0.0.0.0"
                        assert config["port"] == 9090