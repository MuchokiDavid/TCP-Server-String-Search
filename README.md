# String Search Server

A high-performance TCP server for fast string existence checks in large files (250k+ records), supporting SSL encryption and configurable search modes.

## Key Features

  - **Blazing-fast searches**:
      - 0.5ms response (cached mode)
      - \<40ms response (uncached mode)
  - **Secure communications**:
      - Configurable SSL/TLS encryption
      - Self-signed certificates
  - **Thread-safe architecture**:
      - Handles unlimited concurrent connections
  - **Two search modes**:
      - `REREAD_ON_QUERY=False`: In-memory cached searches
      - `REREAD_ON_QUERY=True`: Real-time file rereading

## Installation

### Prerequisites

  - Python 3.8+
  - Linux system (tested on Ubuntu 20.04)

<!-- end list -->

```bash
# Unzip repository
Unzip the project files.

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
string_match_server/
├── client/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   └── client.py
│   ├── __init__.py
│   ├── config.ini
│   └── main.py
├── server/
│   ├── server/
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   ├── exception.py
│   │   ├── search_algorithm.py
│   │   ├── server.py
│   │   └── utils.py
│   ├── __init__.py
│   ├── config.ini
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_server.py
├── security/
│   ├── server.crt
│   └── server.key
├── install/
│   ├── commands.md
│   ├── setup_deamon.sh
│   ├── Linux_deamon_logs.png
│   ├── string_search.service
│   └── INSTALL.md
├── data/
│   ├── 10k.txt
│   ├── 50k.txt
│   ├── 100k.txt
│   ├── 200k.txt
│   └── 500k.txt
├── docs/
│   └── speed_report.pdf
├── README.md
└── requirements.txt
```

## Server Configuration

Edit `server/config.ini`:

```ini
[FILES]
linuxpath = /path/to/200k.txt

[QUERY]
REREAD_ON_QUERY = False

[SERVER]
HOST = 0.0.0.0
PORT = 44445

[SSL]
SSL_ENABLED = True
SSL_CERT = /path/to/server.crt
SSL_KEY = /path/to/server.key

[LOGGING]
DEBUG = True
```

## Usage

### As a Standalone Server

```bash
python server/main.py
```

### As a Systemd Service

```bash
# Copy service file
sudo cp install/string_search_server.service /etc/systemd/system/

# Reload and start
sudo systemctl daemon-reload
sudo systemctl start string_search
sudo systemctl enable string_search
```

## Testing

### Unit Tests

```bash
pytest tests/ --cov=src --cov-report=html
```

### Load Testing

```bash
locust -f tests/load_test.py --host=ssl://localhost:44445
```

## Running the Client

```bash
# From project root
python client/main.py
```

## Client Configuration

Edit `client/config.ini`:

```ini
[CLIENT]
HOST = 0.0.0.0
PORT = 44445

[SSL]
SSL_ENABLED = True
SSL_CERT = /path/to/server.crt
SSL_KEY = /path/to/server.key
```

## Search Algorithms

The server implements multiple search strategies:

1.  **Set Membership** - Default for cached mode
2.  **Binary Search** - For sorted static files
3.  **Linear Search** - For dynamic files
4.  **Jump Search** - Operates by dividing the array into smaller blocks of a fixed size, then jumping from block to block.
5.  **Exponential Search** - Starts from the first element and exponentially increases the range, then performs a binary search.

## Security Considerations

  - All network traffic is encrypted when SSL is enabled.
  - Input sanitization prevents buffer overflow attacks.
  - Rate limiting is recommended for public-facing deployments.

## Troubleshooting

| Error                  | Solution                                    |
| :--------------------- | :------------------------------------------ |
| `ssl.SSLEOFError`      | Verify certificate paths and permissions    |
| `Address already in use` | Wait 60s for socket timeout or change port |
| High CPU usage         | Reduce `max_threads` in config              |
| `FileNotFoundError`    | Ensure the file is in the config path       |