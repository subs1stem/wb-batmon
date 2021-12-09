#!/bin/bash
apt install python3-dev

echo 'Creating service...'
cp -u -r service/wb-batmon.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable wb-batmon.service

cp -u -r source /mnt/data/etc/wb-batmon && cd /mnt/data/etc/wb-batmon || exit

echo 'Installing venv...'
python3 -m venv venv
source venv/bin/activate

echo 'Installing requirements...'
pip install -r requirements.txt
deactivate

echo '--------------------------------------------------------------------'
echo 'Done. Edit the settings.py file at the path /mnt/data/etc/wb-batmon.'
echo 'Use "systemctl start wb-batmon.service" for running module.'
