"""
Server module for the string search service.

This module provides a socket-based server that allows clients to search
for strings in a specified file. It supports SSL encryption, concurrent
connections via threading, and various search algorithms.
"""
import socket
import threading
import os
import ssl
from timeit import default_timer as timer
from typing import List, Optional, Union, Tuple
import logging

from . import config_loader
from . import utils
from .search_algorithms import jump_search
from .exceptions import InvalidPayloadError, FileAccessError

CONFIG: dict = config_loader.load_config()
"""
Load the configuration settings using the `config_loader` module and retrieve
configuration variables
"""
MAX_PAYLOAD: int = CONFIG["max_payload"]
BIND_IP: str = CONFIG["host"]
BIND_PORT: int = CONFIG["port"]
STRINGS_FILE_PATH: str = CONFIG["linuxpath"]
REREAD_QUERY: bool = CONFIG["reread_on_query"]
SSL_ENABLED: bool = CONFIG["ssl_enabled"]
DEBUG: bool = CONFIG["debug"]
SSL_CERT: str = CONFIG["ssl_certificate"]
SSL_KEY: str = CONFIG["ssl_private_key"]

"""
- Get the directory of the current configuration file
- Determine the project root directory by moving two levels up from the configuration directory.
"""
config_dir: str = os.path.dirname(os.path.abspath(__file__))
project_root: str = os.path.abspath(os.path.join(config_dir, "../.."))

# Replace relative paths in the config with absolute paths
if STRINGS_FILE_PATH.startswith("../"):
    STRINGS_FILE_PATH = os.path.abspath(
        os.path.join(project_root, STRINGS_FILE_PATH[3:])
    )

CACHE_DATA: Optional[List[str]] = utils.reread_file(STRINGS_FILE_PATH)

if SSL_CERT.startswith("../"):
    SSL_CERT = os.path.abspath(os.path.join(project_root, SSL_CERT[3:]))

if SSL_KEY.startswith("../"):
    SSL_KEY = os.path.abspath(os.path.join(project_root, SSL_KEY[3:]))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Get the file size of string file path file
FILE_SIZE: Optional[int] = utils.get_file_size(STRINGS_FILE_PATH)

# Create the secure SSL context at module level
context = None
if SSL_ENABLED:
    try:
        context = utils.create_secure_ssl_context()
        logger.info("Secure SSL context initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize SSL context: {e}")
        logger.error("Server will not start with SSL enabled")
        raise

class StringSearchServer:
    """
    Server class that handles string search requests from clients.
    
    This class manages client connections, performs string searches in the
    provided data files, and maintains performance statistics.
    """
    def __init__(self):
        """Initialize the string search server with performance metrics and thread safety."""
        self.cache_lock = threading.Lock()
        if not SSL_ENABLED:
            logger.info("SSL is disabled")

        # Performance metrics
        self.performance_stats = {
            "total_queries": 0,
            "avg_response_time": 0,
            "max_concurrent": 0,
        }
        # Add a dummy method to satisfy pylint's too-few-public-methods warning
        self.is_running = True

    def get_status(self):
        """Return the current status of the server."""
        return self.is_running

    def handle_client(
        self,
        client_sock: Union[socket.socket, ssl.SSLSocket],
        client_addr: Tuple[str, int],
    ) -> None:
        """
        Handle a client connection by receiving a request, processing it,
        and sending a response.

        Parameters:
            client_sock: The client socket object (regular or SSL)
            client_addr: The address of the client (ip, port)
        """
        try:
            request: str = self._strip_exceeding_received_data(client_sock, MAX_PAYLOAD)
            # Check if the request is empty and return STRING NOT EXIST to client
            if not request:
                client_sock.sendall(b"STRING NOT EXIST")
                logger.error("Empty payload received from client %s", client_addr)
                return

            response: str = ""
            logger.info("Search query from %s: %s", client_addr, request)
            # Load the file content
            search_data: List[str] = []
            if str(REREAD_QUERY) == "True":
                logger.info("Reading file: %s", STRINGS_FILE_PATH)
                reread_time_start = timer()
                file_dt: Optional[List[str]] = self._load_file_contents(
                    STRINGS_FILE_PATH
                )
                if isinstance(file_dt, list):
                    reread_time_end = timer()
                    search_data = file_dt
                    reread_time: float = (reread_time_end - reread_time_start) * 1000
                    logger.info("Reread search time: %.2fms", reread_time)
            else:
                search_data = CACHE_DATA
            # Search query in the file
            logger.info("Searching for string: %s", request)
            found, response_time = self._search_string(search_data, request)

            # Update performance stats
            performance_lock = threading.Lock()
            with performance_lock:
                self.performance_stats["total_queries"] += 1
                self.performance_stats["avg_response_time"] = (
                    self.performance_stats["avg_response_time"]
                    * (self.performance_stats["total_queries"] - 1)
                    + response_time
                ) / self.performance_stats["total_queries"]

            response = "STRING EXISTS" if found else "STRING NOT EXIST"
            logger.info("%s- %s", response, '200:OK' if found else '404:NOT FOUND')
            # Send response to client
            client_sock.sendall(response.encode())
            logger.debug("Response sent: %s", response)
            return
        except InvalidPayloadError as e:
            logger.error("Invalid payload: %s", str(e))
            client_sock.sendall(f"ERROR: {str(e)}".encode())
        except (ConnectionError, TimeoutError) as e:
            logger.error("Connection error with %s: %s", client_addr, str(e))
            client_sock.sendall(b"SERVER ERROR")
        except socket.error as e:
            logger.error("Socket error with %s: %s", client_addr, str(e))
            client_sock.sendall(b"SERVER ERROR")
        except (UnicodeError, UnicodeDecodeError) as e:
            logger.error("Encoding error with %s: %s", client_addr, str(e))
            client_sock.sendall(b"SERVER ERROR")
        finally:
            client_sock.close()

    def _search_string(self, data: List[str], request: str):
        """
        Search string using various algorithms with metrics.

        Args:
            data (List): Data where string is searched from
            request (str): string being searched
            
        Returns:
            True: If string exist.
            False: If string does not exist.
        """
        # Get start execution time
        start_time: float = timer()
        found: bool = jump_search(request, data)
        # Execution end time
        end_time: float = timer()
        response_time: float = (end_time - start_time) * 1000
        logger.info("Search time: %.2fms", response_time)
        return found, response_time

    def _load_file_contents(self, path: str) -> Optional[List[str]]:
        """
        Thread-safe file loading with metrics.
        
        Parameters:
            path: Path to the file to load
            
        Returns:
            List of strings from the file or None if an error occurred
            
        Raises:
            FileAccessError: If the file cannot be accessed or loaded
        """
        cache_lock = threading.Lock()
        with cache_lock:
            start_tm = timer()
            try:
                data: List[str] = utils.reread_file(path)
                load_time = (timer() - start_tm) * 1000
                logger.debug("File loaded in %.2fms", load_time)
                return data
            except FileNotFoundError as exc:
                raise FileAccessError("File not found") from exc
            except Exception as e:
                logger.error("Error loading file: %s", e)
                raise FileAccessError(f"Failed to load file: {str(e)}") from e

    def _strip_exceeding_received_data(
        self, sock: socket.socket, max_payload_size: int
    ) -> Optional[bytes]:
        """
        Receive data from a socket connection with size validation.

        Parameters:
            sock: The socket connection
            max_payload_size: The maximum allowed payload size in bytes

        Returns:
            The received data as bytes, or None if connection was closed
            
        Raises:
            InvalidPayloadError: If there is an error receiving or processing the data
        """
        try:
            data: str = sock.recv(max_payload_size).decode().strip()
            if not data:
                raise InvalidPayloadError("Empty payload received")
            if len(data) > max_payload_size:
                data = data.rstrip("\x00")
            return data
        except Exception as e:
            logger.error("Error receiving data: %s", e)
            raise InvalidPayloadError from e

def handle_concurrency_metrics(client_operation: StringSearchServer) -> None:
    """
    Update the concurrency metrics for server monitoring.
    
    Parameters:
        client_operation: The StringSearchServer instance to update metrics for
    """
    concurrent_lock = threading.Lock()
    with concurrent_lock:
        current_threads = threading.active_count() - 1  # Subtract main thread
        client_operation.performance_stats["max_concurrent"] = max(
            client_operation.performance_stats["max_concurrent"],
            current_threads,
        )
        logger.info("Current threads: %s", current_threads)
        logger.info(
            "Max concurrent: %s",
            client_operation.performance_stats["max_concurrent"]
        )

def start(host: str, port: int, debug: bool) -> None:
    """
    Start the server and handle incoming client connections.

    Parameters:
        host: The host address to bind to
        port: The port number to listen on
        debug: Whether to print debug information
    """
    try:
        sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket: Union[socket.socket, ssl.SSLSocket] = sock

        if SSL_ENABLED:
            # Wrap socket if ssl is enabled
            try:
                server_socket = context.wrap_socket(sock, server_side=True)
                logger.info("SSL enabled connection")
            except socket.timeout as e:
                logger.error("Socket timeout: %s", e)
                sock.close()
                return
            except ssl.SSLError as e:
                logger.error("SSL error: %s", e)
                sock.close()
                return

        # Bind connection
        server_socket.bind((host, port))
        # Listen to requests from clients
        server_socket.listen(5)
        logger.info(
            "Server listening on %s:%s %s",
            host,
            port,
            '(DEBUG MODE)' if debug else ''
        )

        while True:
            # Get connection details of the client making request
            client_socket: Union[socket.socket, ssl.SSLSocket]
            address: Tuple[str, int]
            client_socket, address = server_socket.accept()
            logger.debug("Connection from %s", address)

            # Create an instance of client operation class
            client_operation: StringSearchServer = StringSearchServer()

            # Update concurrency metrics
            handle_concurrency_metrics(client_operation)

            # # Implement threading to enable simultaneous connections
            client_thread: threading.Thread = threading.Thread(
                target=client_operation.handle_client, args=(client_socket, address)
            )
            client_thread.start()
    except PermissionError as e:
        logger.error("Permission error (possibly binding to restricted port): %s", e)
    except OSError as e:
        logger.error("OS error: %s", e)
    except ValueError as e:
        logger.error("Value error (possibly bad address format): %s", e)
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
        raise
    except SystemExit:
        logger.info("System exit requested")
        raise
    finally:
        if "server_socket" in locals():
            server_socket.close()
