"""
This script sets up a client socket connection to a server with optional SSL encryption.
It loads configuration settings, such as host, port, and SSL settings, from a config file.
The script then creates an SSL context, loads the SSL certificate and private key.
Establish a socket connection to the server.
It sends data to the server and receives a response, printing it to the console.
The script runs in a loop, continuously accepting user input to send to the server.

Parameters:
    BIND_IP - The IP address to bind the socket to.
    BIND_PORT - The port to bind the socket to.
    SSL_ENABLED - A boolean indicating whether SSL encryption is enabled.
    SSL_CERT - The path to the SSL certificate file.
    SSL_KEY - The
"""
import os
import socket
import ssl
from typing import Optional

from . import config_loader

# Load configuration settings from config file.
CONFIG: dict = config_loader.load_config()
BIND_IP: str = CONFIG["host"]
BIND_PORT: int = CONFIG["port"]
SSL_ENABLED: bool = CONFIG["ssl_enabled"]
SSL_CERT: str = CONFIG["ssl_certificate"]
SSL_KEY: str = CONFIG["ssl_private_key"]

# Get the directory of the current configuration file.
config_dir: str = os.path.dirname(os.path.abspath(__file__))
# Determine the project root directory by moving two levels up from the configuration directory.
project_root: str = os.path.abspath(os.path.join(config_dir, "../.."))

# Replace relative paths in the config with absolute paths
if SSL_CERT.startswith("../"):
    SSL_CERT = os.path.abspath(os.path.join(project_root, SSL_CERT[3:]))

if SSL_KEY.startswith("../"):
    SSL_KEY = os.path.abspath(os.path.join(project_root, SSL_KEY[3:]))

# Create an SSL context with a specified protocol and load the certificate.
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.maximum_version = ssl.TLSVersion.TLSv1_3

context.load_cert_chain(SSL_CERT, SSL_KEY)

# Create a new socket using the AF_INET address family and SOCK_STREAM socket type.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data: str = ""

# Wrap the given socket for SSL/TLS encryption in server mode within a context manager.
while True:
    data = input()
    with socket.create_connection((BIND_IP, BIND_PORT)) as sock:
        try:
            ssock: Optional[ssl.SSLSocket] = None
            if SSL_ENABLED:
                # Wrap socket to secure the connection when SSL is enabled.
                ssock = context.wrap_socket(sock, server_hostname=BIND_IP)
                ssock.sendall(data.encode())
                response = ssock.recv(1024)
                print(response.decode())
            else:
                sock.sendall(data.encode())
                response = sock.recv(1024)
                print(response.decode())
        finally:
            # Closing socket
            sock.close()
