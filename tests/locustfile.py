import socket
import ssl
import random
import time
from typing import List

from locust import User, task, between

# Configuration
HOST = "127.0.0.1"
PORT = 8080
USE_SSL = True
CERT_FILE = "../security/server.crt"
KEY_FILE = "../security/server.key"
MAX_PAYLOAD = 1024


# Base samples provided by the user
def create_test_string() -> List[str]:
    """Generates a list of 1000 random samples from the base samples list.
    
    Returns:
        A list of 1000 randomly selected samples from the base_samples list.
    """
    base_samples: List[str] = [
        "1;0;1;11;0;10;5;0;",
        "20;0;11;21;0;18;3;0;",
        "21;0;1;21;0;5;30;0;",
        "22;0;21;11;0;7;4;0;",
        "23;0;23;11;0;200;5;0;",
        "24;0;21;21;0;2;3;0;",
        "25;0;16;21;0;164;0;",
        "1;0;16;16;0;14;30;",
        "2;0;16;21;0;14;3;0;",
        "3;0;1;28;0;19;4;0;",
        "4;0;1;26;0;5;5;0",
        "5;0;1;28;0;19;4;0;",
        "6;0;21;26;0;19;4;0;",
        "7;0;21;26;0;19;4;0;",
        "8;0;23;6;0;20;5;0;",
        "9;0;6;11;0;18;4;0;",
        "10;0;23;16;0;22;4;0;",
        "11;0;23;28;0;24;3;0;",
        "12;0;1;28;0;19;4;0;",
        "13;0;11;26;0;23;3;0;",
        "14;0;23;16;0;22;4;0;",
        "15;0;21;11;0;7;3;0;",
        "16;0;1;26;0;18;5;0;",
        "17;0;16;21;0;18;3;0;",
        "18;0;21;28;0;22;3;0;",
        "19;0;6;11;0;19;5;0;",
    ]

    # Extend the list to 1000 entries by randomly sampling
    random.seed(42)  # For reproducibility
    return [random.choice(base_samples) for _ in range(1000)]


TEST_STRINGS: List[str] = create_test_string()

not_found: List[str] = []
found: List[str] = []

"""
   A class for a socket client that can connect to a server, send and receive messages, and close the connection.
   - `connect()`: Establishes a connection to the server.
   - `send_and_receive(message: str) -> str`: Sends a message to the server and receives a response.
   - `close()`: Closes the connection to the server.
"""


class SocketClient:
    def __init__(self):
        self.sock = None

    def connect(self) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if USE_SSL:
                context = ssl._create_unverified_context()
                self.sock = context.wrap_socket(sock, server_hostname=HOST)
            else:
                self.sock = sock
            self.sock.connect((HOST, PORT))
        except Exception as e:
            raise ConnectionError(f"Connection failed: {e}")

    def send_and_receive(self, message: str) -> str:
        try:
            self.sock.sendall(message.encode())
            response = self.sock.recv(MAX_PAYLOAD).decode()
            return response
        except Exception as e:
            raise IOError(f"Send/receive failed: {e}")

    def close(self):
        if self.sock:
            self.sock.close()


class SocketUser(User):
    wait_time = between(0.5, 2.0)

    def on_start(self) -> None:
        self.client: SocketClient = SocketClient()

    @task
    def search_string(self) -> None:
        query: str = random.choice(TEST_STRINGS)
        start_time: float = time.time()
        try:
            self.client.connect()
            response = self.client.send_and_receive(query)
            total_time: float = (time.time() - start_time) * 1000  # ms

            # Use simple logging instead of events API
            if response in ["STRING EXISTS", "STRING NOT EXISTS"]:
                print(f"Success: {query} -> {response} ({total_time:.2f}ms)")
                if response == "STRING EXISTS":
                    found.append(query)
                else:
                    not_found.append(query)
                print(f"Found: {len(found)}")
                print(f"Not Found: {len(not_found)}")
                print(f"Total: {len(found) + len(not_found)}")

            else:
                raise ValueError(f"Unexpected response: {response}")
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            print(f"Error: {query} -> {str(e)} ({total_time:.2f}ms)")
        finally:
            self.client.close()
