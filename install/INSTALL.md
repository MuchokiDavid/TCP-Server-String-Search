# String Match Server - Installation Guide

This document provides instructions for installing and running the String Match Server application as a daemon service on Linux systems.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- systemd (for service management)
- Root or sudo access on your Linux system

## Installation Steps

### 1. Open the project repository

```bash
cd string_match_server
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the application

Review and modify the configuration files as needed:

- Server configuration: `server/config.ini`
- Client configuration: `client/config.ini`

### 6. Create a system service file

Create a systemd service file for the string match server:

```bash
sudo nano /etc/systemd/system/string-match-server.service
```

Add the following content to the file (adjust paths as necessary):

```
[Unit]
Description=String Match Server
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/string_match_server
ExecStart=/usr/bin/python3 /path/to/string_match_server/server/main.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 7. Enable and start the service

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable string-match-server.service

# Start the service
sudo systemctl start string-match-server.service
```

### 8. Verify the service is running

```bash
# Check service status
sudo systemctl status string-match-server.service

# View logs
sudo journalctl -u string-match-server.service
```

## Usage

### Running the client

```bash
cd string_match_server
python client/main.py
```

### Service Management Commands

- Start the service: `sudo systemctl start string-match-server.service`
- Stop the service: `sudo systemctl stop string-match-server.service`
- Restart the service: `sudo systemctl restart string-match-server.service`
- Enable automatic startup: `sudo systemctl enable string-match-server.service`
- Disable automatic startup: `sudo systemctl disable string-match-server.service`
- Check service status: `sudo systemctl status string-match-server.service`

## Troubleshooting

### Service fails to start

Check the logs for detailed error information:

```bash
sudo journalctl -u string-match-server.service -e
```

Common issues:
- Incorrect paths in the service file
- Missing dependencies
- Permission issues
- Configuration errors

### Permission Issues

If you encounter permission issues, make sure:
- The specified user has access to the application directory
- The application has read/write permissions for any data directories it needs
- Security certificates have proper permissions (usually 600 or 400)

```bash
# Fix permissions for security certificates
sudo chmod 600 /path/to/string_match_server/security/server.key
sudo chmod 644 /path/to/string_match_server/security/server.crt
```