#!/bin/bash

# Update and install dependencies
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y nodejs npm
sudo npm install -g pm2

# Install Python packages
pip3 install pyTelegramBotAPI

# Move files from 'bashy' directory to the root directory
mv bashy/* /root

# Remove 'bashy' directory and its contents
rm -r bashy

# Prompt for Telegram token and chat ID
read -p "Token: " token
read -p "iD: " chat_id

# Remove square brackets from chat ID
chat_id=$(echo "$chat_id" | tr -d '[]')

# Set environment variables
export TELEGRAM_TOKEN="$token"
export TELEGRAM_CHAT_ID="$chat_id"

cd

pm2 start /root/secure.py --name secure --interpreter=python3.10
