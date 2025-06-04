"""
Load configuration settings from an INI file and return them as a dictionary.

Return: 
    A dictionary containing the configuration settings loaded from the INI file.
"""
import configparser
import os
from typing import Dict, Any
from pathlib import Path

# Define constants for testing
CONFIG_PATH = None  # Will be set dynamically or overridden in tests
ENV_PREFIX = "STRING_MATCH_"  # Environment variable prefix

def load_config() -> Dict[str, Any]:
    """Load configuration from INI file."""

    # Try to find config.ini relative to the package root
    base_dir = Path(__file__).parent.parent
    file_path = CONFIG_PATH if CONFIG_PATH else base_dir / "config.ini"

    try:
        config = configparser.ConfigParser()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file not found: {file_path}")
        # Read config file
        config.read(file_path)
        
        # Create config dictionary with proper type conversion
        config_dict = {
            "host": config.get("SERVER", "HOST", fallback="127.0.0.1"),
            "port": config.getint("SERVER", "PORT", fallback=8080),
            "ssl_enabled": config.getboolean("SSL", "SSL_ENABLED", fallback=False),
            "max_payload": config.getint("REQUEST", "MAX_PAYLOAD_SIZE", fallback=1024),
            "ssl_certificate": config.get("SSL", "SSL_CERT", fallback=""),
            "ssl_private_key": config.get("SSL", "SSL_KEY", fallback=""),
            "debug": config.getboolean("LOGGING", "DEBUG", fallback=False),
            "log_file": config.get("LOGGING", "LOG_FILE", fallback=""),
            "linuxpath": config.get("FILES", "linuxpath", fallback=""),
            "reread_on_query": config.getboolean("QUERY", "REREAD_ON_QUERY", fallback=False),
        }
        
        # Override with environment variables if present
        for key in config_dict:
            env_var = f"{ENV_PREFIX}{key.upper()}"
            if env_var in os.environ:
                # Convert type based on the original value's type
                if isinstance(config_dict[key], bool):
                    config_dict[key] = os.environ[env_var].lower() in ('true', 'yes', '1')
                elif isinstance(config_dict[key], int):
                    config_dict[key] = int(os.environ[env_var])
                else:
                    config_dict[key] = os.environ[env_var]
                    
        return config_dict
    except Exception as e:
        print(f"Error loading config: {e}")
        raise