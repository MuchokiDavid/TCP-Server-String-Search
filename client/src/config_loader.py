# src/config_loader.py
"""
Load configuration settings from an .ini file and return them as a dictionary.

Return: 
    A dictionary containing the configuration settings loaded from the .ini file.
"""

import configparser
from typing import Dict, Any
from pathlib import Path


def load_config() -> Dict[str, Any]:
    """Loads configuration from an INI file.
    Paths in the config are resolved relative to the config file's directory
    if they are not absolute.
    """
    base_dir = Path(__file__).parent.parent
    print(base_dir)
    file_path = base_dir / "config.ini"

    def resolve_path(path_str: str) -> str:
        if not path_str: # Handle empty path strings
            return ""
        p = Path(path_str)
        if p.is_absolute():
            return str(p)
        return str((file_path.parent / p).resolve())

    try:
        config = configparser.ConfigParser()
        config.read(file_path)
        return {
            "host": config.get("CLIENT", "HOST", fallback="127.0.0.1"),
            "port": config.getint("CLIENT", "PORT", fallback=8080),
            "ssl_enabled": config.getboolean("SSL", "SSL_ENABLED", fallback=False),
            "ssl_certificate": resolve_path(config.get("SSL", "SSL_CERT", fallback="")),
            "ssl_private_key": resolve_path(config.get("SSL", "SSL_KEY", fallback="")),
        }
    except Exception as e:
        print(f"Error loading configuration: {e}")
        raise
