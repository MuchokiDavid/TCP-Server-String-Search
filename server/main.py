from server import server
from server import config_loader

"""
Load the configuration file and extract the host and port values to bind the IP and port.
The configuration file is loaded using the `config_loader.load_config()` function.
The host value is stored in `BIND_IP` and the port value is stored in `BIND_PORT`.
"""
CONFIG: dict = config_loader.load_config()
BIND_IP: str = CONFIG["host"]
BIND_PORT: int = CONFIG["port"]
DEBUG: bool= CONFIG["debug"]

if __name__ == '__main__':
    """
    Run the server with the specified host IP, port, and debug mode.
    If the script is executed directly, start the server.
    @param BIND_IP - The IP address to bind the server to.
    @param BIND_PORT - The port number to bind the server to.
    @param DEBUG - Boolean flag indicating whether to run the server in debug mode or not.
    """
    server.start(host=BIND_IP, port=BIND_PORT, debug=DEBUG)
