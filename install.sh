#!/bin/bash

echo 'Creating service...'
cp -u -r service/wb-batmon.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable wb-batmon.service

cp -u -r source /opt/wb-batmon && cd /opt/wb-batmon/ || exit

echo 'Installing venv...'
python3 -m venv venv
source venv/bin/activate

echo 'Installing requirements...'
pip install -r requirements.txt
deactivate

echo 'Done. Edit the settings.py file at the path /opt/wb-batmon.
Use "systemctl start wb-batmon.service" for running module.'
