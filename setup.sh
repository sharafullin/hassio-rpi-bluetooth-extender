sudo apt update
sudo apt upgrade
sudo apt install git -y
sudo apt install redis-server
sudo pip3 install netifaces
sudo pip3 install paho-mqtt
sudo pip3 install delayed
sudo apt-get install sqlite3

sudo nano /lib/systemd/system/hassio-rpi-bluetooth-extender.service
sudo chmod 644 /lib/systemd/system/hassio-rpi-bluetooth-extender.service
sudo systemctl daemon-reload
sudo systemctl enable hassio-rpi-bluetooth-extender.service

sudo systemctl enable redis.service