# Deployment commands to Linux Deamon

### 1. Copy the service file to systemd directory

```bash
sudo cp string-match-server.service /etc/systemd/system/
```

### 2. Reload systemd to recognize the new service

```bash
sudo systemctl daemon-reload
```

### 3. Enable the service to start on boot

```bash
sudo systemctl enable string-match-server
```

### 4. Start the service

```bash
sudo systemctl start string-match-server
```

### 5. Check the status

```bash
sudo systemctl status string-match-server
```

### 6. View logs

```bash
sudo journalctl -u string-match-server -f
```

## Other useful commands:

### Stop the service:

```bash
 sudo systemctl stop string-match-server
```

### Restart the service:

```bash
sudo systemctl restart string-match-server
```

### Disable auto-start on boot:

```bash
sudo systemctl disable string-match-server
```

### View recent logs:

```bash
sudo journalctl -u string-match-server --since "1 hour ago"
```
