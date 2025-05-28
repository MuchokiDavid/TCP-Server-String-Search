"""
This script is the entry point for starting the server.
It loads the server configuration, including the host IP and port,
and starts the server with the specified settings.
"""
from server import server
from server.config_loader import load_config

# Load the configuration file and extract the host and port values to bind the IP and port.
CONFIG: dict = load_config()
BIND_IP: str = CONFIG["host"]
BIND_PORT: int = CONFIG["port"]
DEBUG: bool= CONFIG["debug"]

if __name__ == '__main__':
    """
    Run the server with the specified host IP, port, and debug mode.
    If the script is executed directly, start the server.
    This will bind the server to the specified IP and port,
    and enable debug mode if specified in the configuration.
    :return: None
    """
    server.start(host=BIND_IP, port=BIND_PORT, debug=DEBUG)
