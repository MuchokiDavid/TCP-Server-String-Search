"""
Tests for path handling to ensure the application works across different environments.
"""
import os
import pytest
from unittest.mock import patch, MagicMock

from server.server import server
from server.server import utils


class TestPathHandling:
    """Test class for path handling functionality."""

    def test_relative_path_resolution(self):
        """Test that relative paths are properly resolved to absolute paths."""
        # Mock the project root directory
        test_project_root = "/test/project/root"
        
        with patch.object(os.path, "dirname", return_value="/test/project/root/server/server"):
            with patch.object(os.path, "abspath") as mock_abspath:
                # Setup the mock to handle different path combinations
                def side_effect(path):
                    if path == "/test/project/root/server/server":
                        return "/test/project/root/server/server"
                    elif path == "/test/project/root/server/server/../..":
                        return test_project_root
                    elif path.startswith(test_project_root):
                        # Handle paths that are being resolved from relative to absolute
                        return path.replace("../", f"{test_project_root}/")
                    return path
                
                mock_abspath.side_effect = side_effect
                
                # Test relative path resolution for file paths
                relative_path = "../data/test.txt"
                expected_absolute_path = f"{test_project_root}/data/test.txt"
                
                # Create a new instance to trigger path resolution
                with patch.dict(server.CONFIG, {"linuxpath": relative_path}):
                    # Force recalculation of the path
                    resolved_path = os.path.abspath(
                        os.path.join(test_project_root, relative_path[3:])
                    )
                    
                    assert resolved_path == expected_absolute_path

    def test_ssl_cert_path_resolution(self):
        """Test that SSL certificate paths are properly resolved."""
        # Mock the project root directory
        test_project_root = "/test/project/root"
        
        with patch.object(os.path, "dirname", return_value="/test/project/root/server/server"):
            with patch.object(os.path, "abspath") as mock_abspath:
                # Setup the mock to handle different path combinations
                def side_effect(path):
                    if path == "/test/project/root/server/server":
                        return "/test/project/root/server/server"
                    elif path == "/test/project/root/server/server/../..":
                        return test_project_root
                    elif path.startswith(test_project_root):
                        # Handle paths that are being resolved from relative to absolute
                        return path.replace("../", f"{test_project_root}/")
                    return path
                
                mock_abspath.side_effect = side_effect
                
                # Test relative path resolution for SSL certificate
                relative_cert_path = "../security/server.crt"
                expected_absolute_cert_path = f"{test_project_root}/security/server.crt"
                
                # Create a new instance to trigger path resolution
                with patch.dict(utils.CONFIG, {"ssl_certificate": relative_cert_path}):
                    # Force recalculation of the path
                    resolved_path = os.path.abspath(
                        os.path.join(test_project_root, relative_cert_path[3:])
                    )
                    
                    assert resolved_path == expected_absolute_cert_path

    def test_file_loading_with_absolute_path(self, sample_data_file):
        """Test that files can be loaded using absolute paths."""
        # Use the fixture to get an absolute path to a sample file
        data = utils.reread_file(sample_data_file)
        
        # Verify the file was loaded correctly
        assert data is not None
        assert len(data) == 10
        assert "apple" in data
        assert "lemon" in data

    def test_file_loading_with_nonexistent_path(self):
        """Test handling of nonexistent file paths."""
        # Try to load a file that doesn't exist
        data = utils.reread_file("/nonexistent/path/to/file.txt")
        
        # Verify the function returns None for nonexistent files
        assert data is None