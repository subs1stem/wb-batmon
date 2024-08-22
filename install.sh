#!/bin/bash

echo 'Installing Python and necessary packages...'
apt update
apt install -y python3-dev python3-venv python3-pip

echo 'Creating systemd service symlink...'
ln -s /opt/wb-batmon/systemd/wb-batmon.service /etc/systemd/system/wb-batmon.service
systemctl daemon-reload
systemctl enable wb-batmon.service

echo 'Setting up virtual environment...'
python3 -m venv /opt/wb-batmon/venv
source /opt/wb-batmon/venv/bin/activate

echo 'Installing Python dependencies...'
pip install -r /opt/wb-batmon/requirements.txt
deactivate

echo 'Copying .env.example to .env...'
cp /opt/wb-batmon/.env.example /opt/wb-batmon/.env

echo '---------------------------------------------------------------------------'
echo 'Installation complete!'
echo 'Please configure the .env file located at: /opt/wb-batmon/.env'
echo 'To start the wb-batmon service, use: systemctl start wb-batmon.service'
