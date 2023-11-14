#!/bin/bash

sudo apt update

sudo apt install -y python3-pip

sudo apt install -y nodejs npm

sudo npm install -g pm2

pip3 install pyTelegramBotAPI

read -p "Enter your Telegram bot token: " token
read -p "Enter your Telegram chat ID (enclosed in square brackets, e.g., [2113442]): " chat_id

chat_id=$(echo "$chat_id" | tr -d '[]')

export TELEGRAM_TOKEN="$token"
export TELEGRAM_CHAT_ID="$chat_id"

pm2 start file.py --name secure --interpreter=python3.10
