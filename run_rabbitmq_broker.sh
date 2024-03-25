#!/bin/bash

# Check root privileges and exit if not root
if [ "$(whoami)" != "root" ]; then
  echo "This script requires root privileges. Please run with sudo."
  exit 1
fi

# get the arguments
distribution_name="$1"
user_name="$2"
password="$3"
queue_name="$4"

# Check if all arguments are provided
if [ -z "$distribution_name" ] || [ -z "$user_name" ] || [ -z "$password" ] || [ -z "$queue_name" ]; then
  echo "Please provide all arguments: distribution_name, user_name, password, queue_name"
  exit 1
fi

# Check if all arguments are provided
sudo apt update -y
sudo apt-get install curl gnupg -y
sudo apt-get install apt-transport-https -y

# Add RabbitMQ keys to trusted keys
curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
curl -1sLf "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf77f1eda57ebb1cc" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg > /dev/null
curl -1sLf "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/io.packagecloud.rabbitmq.gpg > /dev/null

# Add RabbitMQ repository definitions
definition_file="/etc/apt/sources.list.d/rabbitmq.list"
cat << EOF > "$definition_file"
deb [signed-by=/usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg] http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu distribution-name main
deb-src [signed-by=/usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg] http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu distribution-name main
deb [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ distribution-name main
deb-src [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ distribution-name main
EOF

# Replace "distribution-name" with the variable in the file
sudo sed -i "s/distribution-name/$distribution_name/g" /etc/apt/sources.list.d/rabbitmq.list

# Install RabbitMQ server
sudo apt-get update -y
sudo apt-get install -y erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
sudo apt-get install rabbitmq-server -y --fix-missing

# Start RabbitMQ server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# Create a new user, set permissions and create a queue
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmqctl add_user "$user_name" "$password"
sudo rabbitmqctl set_permissions -p "/" "$user_name" ".*" ".*" ".*"
sudo rabbitmqctl set_user_tags "$user_name" administrator
sudo curl -X PUT "http://localhost:15672/api/queues/%2F/$queue_name" \
  -u "$username:$password" -H 'Content-Type: application/json' \
  -d '{"durable": true}'

# Print success message
echo "RabbitMQ broker is successfully set up with user $user_name and queue $queue_name"
