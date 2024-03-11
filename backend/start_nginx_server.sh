#!/bin/bash

# Check root privileges (required for restarting Nginx)
if [ "$(whoami)" != "root" ]; then
  echo "This script requires root privileges. Please run with sudo."
  exit 1
fi

# Check if server name is provided
server_name="$1"

if [ -z "$server_name" ]; then
  echo "Please provide a server name or ip address as an argument."
  exit 1
fi

# Install Nginx
sudo apt update
sudo apt install nginx -y

# Start Nginx
sudo systemctl start nginx
# Enable Nginx to start on boot
sudo systemctl enable nginx

# Create a temporary server block file
server_block_file="/etc/nginx/sites-available/backend"
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

sudo ln -s /etc/nginx/sites-available/backend /etc/nginx/sites-enabled
# Test Nginx configuration syntax
sudo nginx -t

# Reload Nginx configuration if syntax is valid
if [ $? -eq 0 ]; then
  echo "Configuration syntax valid. Reloading Nginx..."
  sudo systemctl restart nginx
else
  echo "Error in configuration file. Please check the syntax."
  rm "$server_block_file"
  exit 1
fi

echo "Nginx server running with port forwarding (http://80 -> http://127.0.0.1:8000)"
