"""
A collection of helper functions related to file reading and processing
Includes error handling and logging.
"""

import os
from typing import List, Optional
import logging
import ssl
from pathlib import Path

from . import config_loader

CONFIG: dict = config_loader.load_config()
"""
Load the configuration settings using the `config_loader` module and retrieve
configuration variables
"""
SSL_CERT: str = CONFIG["ssl_certificate"]
SSL_KEY: str = CONFIG["ssl_private_key"]

config_dir: str = os.path.dirname(os.path.abspath(__file__))
project_root: str = os.path.abspath(os.path.join(config_dir, "../.."))

# Replace relative paths in the config with absolute paths
if SSL_CERT.startswith("../"):
    SSL_CERT = os.path.abspath(
        os.path.join(project_root, SSL_CERT[3:])
    )
if SSL_KEY.startswith("../"):
    SSL_KEY = os.path.abspath(
        os.path.join(project_root, SSL_KEY[3:])
    )


logger = logging.getLogger("string_match_server")


def reread_file(file_path: str) -> Optional[List[str]]:
    """
    Reads a file each line and returns a list of stripped lines.

    Args:
        file_path (str): Path to the file.

    Returns:
        Optional[List[str]]: List of lines in the file, or None on failure.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            return [line for line in lines if line]  # filter out empty lines
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
    return None


def get_file_size(file_path: str) -> Optional[int]:
    """
    Attempt to read a file and return the length of the content.

    Args:
        file_path - the path to the file to be read

    Return
        The length of the content of the file, or None if an error occurs.
    """
    return len(reread_file(file_path)) if file_path else None


def create_secure_ssl_context() -> ssl.SSLContext:
    """
    Create a secure SSL context with proper security configurations.

    Returns:
        Properly configured SSL context for server use

    Raises:
        ssl.SSLError: If SSL configuration fails
        FileNotFoundError: If certificate files are not found
    """
    try:
        # Create secure context for server
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        # Set minimum TLS version to 1.2 (disable older, insecure versions)
        context.minimum_version = ssl.TLSVersion.TLSv1_2

        # Disable weak protocols and ciphers
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_SINGLE_DH_USE
        context.options |= ssl.OP_SINGLE_ECDH_USE
        context.options |= ssl.OP_NO_COMPRESSION  # Prevent CRIME attacks

        # Set secure cipher suites (disable weak ciphers)
        context.set_ciphers(
            "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS"
        )

        # Verify certificate files exist before loading
        if not os.path.exists(SSL_CERT):
            raise FileNotFoundError(f"SSL certificate file not found: {SSL_CERT}")
        if not os.path.exists(SSL_KEY):
            raise FileNotFoundError(f"SSL private key file not found: {SSL_KEY}")

        # Load server certificate and private key
        context.load_cert_chain(SSL_CERT, SSL_KEY)

        # Log SSL configuration
        logger.info("SSL context created with secure configuration:")
        logger.info(f"  - Minimum TLS version: {context.minimum_version}")
        logger.info(f"  - SSL options: {context.options}")
        logger.info(f"  - Certificate: {SSL_CERT}")
        logger.info(f"  - Private key: {SSL_KEY}")

        # Verify certificate chain
        _verify_certificate_chain(SSL_CERT)

        return context

    except ssl.SSLError as e:
        logger.error(f"SSL context creation failed: {e}")
        raise
    except FileNotFoundError as e:
        logger.error(f"Certificate file error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating SSL context: {e}")
        raise ssl.SSLError(f"SSL configuration failed: {e}")


def _verify_certificate_chain(cert_path: str) -> None:
    """
    Verify the SSL certificate chain and log certificate details.

    Parameters:
        cert_path: Path to the certificate file
    """
    try:
        import subprocess
        import tempfile

        # Use openssl to verify certificate (if available)
        result = subprocess.run(
            ["openssl", "x509", "-in", cert_path, "-text", "-noout"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            # Extract certificate information
            cert_info = result.stdout
            if "Subject:" in cert_info:
                subject_line = [
                    line for line in cert_info.split("\n") if "Subject:" in line
                ][0]
                logger.info(f"Certificate subject: {subject_line.strip()}")

            if "Not After" in cert_info:
                expiry_line = [
                    line for line in cert_info.split("\n") if "Not After" in line
                ][0]
                logger.info(f"Certificate expiry: {expiry_line.strip()}")
        else:
            logger.warning("Could not verify certificate with openssl")

    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        logger.debug("Certificate verification with openssl not available")
    except Exception as e:
        logger.debug(f"Certificate verification failed: {e}")
