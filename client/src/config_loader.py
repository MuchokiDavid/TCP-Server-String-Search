# src/config_loader.py
"""
Load configuration settings from an INI file and return them as a dictionary.

Return: 
    A dictionary containing the configuration settings loaded from the INI file.
"""

import configparser
from typing import Dict, Any
from pathlib import Path


def load_config() -> Dict[str, Any]:
    """Load configuration from INI file."""
    try:
        config = configparser.ConfigParser()
        # Get config.ini file
        base_dir = Path(__file__).parent.parent
        file_path = base_dir / "config.ini"
        # Read config.ini file
        config.read(file_path)
        return {
            "host": config.get("CLIENT", "HOST", fallback="127.0.0.1"),
            "port": config.getint("CLIENT", "PORT", fallback=8080),
            "ssl_enabled": config.getboolean("SSL", "SSL_ENABLED", fallback=False),
            "ssl_certificate": config.get("SSL", "SSL_CERT", fallback=""),
            "ssl_private_key": config.get("SSL", "SSL_KEY", fallback=""),
        }
    except Exception as e:
        print(f"Error loading configuration: {e}")
        raise
