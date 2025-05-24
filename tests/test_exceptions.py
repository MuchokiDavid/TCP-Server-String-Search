"""
Test cases for the StringSearchServer class exceptions handling.
"""
import pytest
import socket
from unittest import mock
from server.server.server import StringSearchServer
from server.server.exceptions import InvalidPayloadError, FileAccessError


@pytest.fixture
def server():
    """
    Fixture to create an instance of StringSearchServer for testing.
    """
    # Create an instance of StringSearchServer
    return StringSearchServer()


def test_strip_exceeding_received_data_empty_payload(server):
    # Mock a socket that returns an empty payload
    mock_sock = mock.Mock()
    mock_sock.recv.return_value = b""

    with pytest.raises(InvalidPayloadError, match="Empty payload received"):
        server._strip_exceeding_received_data(mock_sock, 1024)


def test_strip_exceeding_received_data_decode_error(server):
    # Mock a socket that returns invalid UTF-8 bytes
    mock_sock = mock.Mock()
    # Invalid UTF-8 bytes
    mock_sock.recv.return_value = b"\x80\x81\x82"

    with pytest.raises(InvalidPayloadError):
        server._strip_exceeding_received_data(mock_sock, 1024)


def test_load_file_contents_file_not_found(server):
    # Simulate a FileNotFoundError when trying to read the file
    with mock.patch("server.server.utils.reread_file", side_effect=FileNotFoundError()):
        with pytest.raises(FileAccessError, match="File not found"):
            server._load_file_contents("nonexistent.txt")


def test_load_file_contents_generic_error(server):
    # Simulate a generic error when trying to read the file
    with mock.patch("server.server.utils.reread_file", side_effect=Exception("Boom")):
        with pytest.raises(FileAccessError, match="Failed to load file: Boom"):
            server._load_file_contents("somefile.txt")


def test_handle_client_empty_payload(server):
    # Mock a client connection with an empty payload
    mock_sock = mock.Mock()
    mock_sock.recv.return_value = b""
    mock_addr = ("127.0.0.1", 12345)

    server._strip_exceeding_received_data = mock.Mock(side_effect=InvalidPayloadError("Empty payload received"))

    server.handle_client(mock_sock, mock_addr)

    mock_sock.sendall.assert_called_with(b"ERROR: Empty payload received")
    mock_sock.close.assert_called_once()


def test_handle_client_valid_data(server):
    # Mock a valid client connection with a search request
    mock_sock = mock.Mock()
    mock_sock.recv.return_value = b"search:test"
    mock_sock.sendall = mock.Mock()
    mock_addr = ("127.0.0.1", 12345)

    server.handle_client(mock_sock, mock_addr)

    # Just ensure it responded, actual response content is not tested here
    mock_sock.sendall.assert_called()  
    mock_sock.close.assert_called_once()
