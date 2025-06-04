#!/bin/bash
set -euo pipefail # Exit on error, treat unset variables as errors, and handle pipe failures

# Determine the script's directory to reliably locate source files
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# --- Configuration File Setup ---
# Source: Assumes 'config' directory is a sibling of the 'install' directory (where this script resides)
# e.g., project_root/config/default_config.ini
#       project_root/install/setup_daemon.sh
DEFAULT_CONFIG_SRC="${SCRIPT_DIR}/../config/default_config.ini"

# Destination: Standard system path for application configuration
TARGET_CONFIG_DIR="/etc/string_match_server/server"
TARGET_CONFIG_FILE="${TARGET_CONFIG_DIR}/config.ini"

# Ensure target configuration directory exists
if [ ! -d "${TARGET_CONFIG_DIR}" ]; then
    echo "Creating configuration directory: ${TARGET_CONFIG_DIR}"
    # This script is expected to be run with sudo for system-wide installation
    mkdir -p "${TARGET_CONFIG_DIR}"
fi

# Copy default config if target config does not exist
if [ ! -f "${TARGET_CONFIG_FILE}" ]; then
    if [ -f "${DEFAULT_CONFIG_SRC}" ]; then
        echo "Copying default configuration from '${DEFAULT_CONFIG_SRC}' to '${TARGET_CONFIG_FILE}'"
        cp "${DEFAULT_CONFIG_SRC}" "${TARGET_CONFIG_FILE}"
        chmod 600 "${TARGET_CONFIG_FILE}"
    else
        echo "Error: Default configuration file not found at '${DEFAULT_CONFIG_SRC}'" >&2
        exit 1
    fi
else
    echo "Configuration file already exists at '${TARGET_CONFIG_FILE}'. Skipping copy."
fi

# --- Systemd Service Installation ---
# Source: Assumes 'string_match_server.service' is in the same 'install' directory as this script
SERVICE_FILE_BASENAME="string_match_server.service"
SERVICE_FILE_SRC="${SCRIPT_DIR}/${SERVICE_FILE_BASENAME}"

# Destination: Standard system path for systemd service files
TARGET_SYSTEMD_DIR="/etc/systemd/system"
TARGET_SERVICE_FILE="${TARGET_SYSTEMD_DIR}/${SERVICE_FILE_BASENAME}"

# Install service file
if [ -f "${SERVICE_FILE_SRC}" ]; then
    echo "Copying service file from '${SERVICE_FILE_SRC}' to '${TARGET_SERVICE_FILE}'"
    cp "${SERVICE_FILE_SRC}" "${TARGET_SERVICE_FILE}"

    echo "Reloading systemd daemon..."
    systemctl daemon-reload

    echo "Enabling string_match_server service..."
    systemctl enable "${SERVICE_FILE_BASENAME}" # Use the service file basename
else
    echo "Error: Service file not found at '${SERVICE_FILE_SRC}'" >&2
    exit 1
fi

echo "Daemon setup completed successfully."