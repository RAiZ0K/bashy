#!/bin/bash

# Update and install dependencies
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y nodejs npm
sudo npm install -g pm2

pip3 install pyTelegramBotAPI

rm -r /root/bashy

read -p "Token: " token
read -p "iD: " chat_id

chat_id=$(echo "$chat_id" | tr -d '[]')

export TELEGRAM_TOKEN="$token"
export TELEGRAM_CHAT_ID="$chat_id"

pm2 start secure.py --name secure --interpreter=python3.10
