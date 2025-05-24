#!/bin/bash
# Validate config first
if [ ! -f "/etc/string_match_server/server/config.ini" ]; then
    cp config/default_config.ini /etc/string_match_server/server/config.ini
    chmod 600 /etc/string_match_server/server/config.ini
fi

# Install service
cp install/string_match_server.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable string_match_server