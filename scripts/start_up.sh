#!bin/bash

echo "Updating system packages"

sudo apt update

sudo apt-get update

sudo apt upgrade -y

echo "Updated system packages"

echo "Installing AWS CLI"

sudo apt install awscli -y

echo "Installed AWS CLI"

echo "Installing Docker"

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

echo "Installed Docker"

echo "Installing pip"

sudo apt install python3-pip -y

echo "Installed pip"
