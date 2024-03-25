#!/bin/bash

# Check root privileges and exit if not root
if [ "$(whoami)" != "root" ]; then
  echo "This script requires root privileges. Please run with sudo."
  exit 1
fi

# get the arguments
user_name="$1"
password="$2"

# Check if all arguments are provided
if [ -z "$user_name" ] || [ -z "$password" ]; then
  echo "Please provide all arguments: user_name, password"
  exit 1
fi

# Install mosquitto broker
sudo apt update
sudo apt install mosquitto mosquitto-clients -y

# create a password file and add user
sudo cat << EOF > "/etc/mosquitto/passwd"
$user_name:$password
EOF

# encrypt the password file
sudo mosquitto_passwd -U "/etc/mosquitto/passwd"

config_file="/etc/mosquitto/conf.d/default.conf"
sudo cat << EOF > "$config_file"
allow_anonymous false
password_file /etc/mosquitto/passwd
listener 1883
EOF

# restart mosquitto broker
sudo systemctl restart mosquitto

# print success message
echo "Mosquitto broker is successfully set up with user $user_name"
