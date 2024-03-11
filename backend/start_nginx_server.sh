#!/bin/bash

# Check root privileges (required for restarting Nginx)
if [ "$(whoami)" != "root" ]; then
  echo "This script requires root privileges. Please run with sudo."
  exit 1
fi

# Define server_name (replace with your domain or IP)
server_name="your_domain.com"

# Create a temporary server block file
server_block_file="/tmp/nginx.conf"
cat << EOF > "$server_block_file"
server {
  listen 80;
  server_name $server_name;

  location / {
    proxy_pass http://127.0.0.1:8000;
    include /etc/nginx/proxy_params;
  }
}
EOF

# Test Nginx configuration syntax
nginx -t -c "$server_block_file"

# Reload Nginx configuration if syntax is valid
if [ $? -eq 0 ]; then
  echo "Configuration syntax valid. Reloading Nginx..."
  systemctl reload nginx
else
  echo "Error in configuration file. Please check the syntax."
  rm "$server_block_file"
  exit 1
fi

# Clean up temporary file
rm "$server_block_file"

echo "Nginx server running with port forwarding (http://80 -> http://127.0.0.1:8000)"
