sudo apt update
sudo apt upgrade
sudo apt install git -y
sudo pip3 install netifaces

sudo nano /lib/systemd/system/hassio-rpi-bluetooth-extender.service
sudo chmod 644 /lib/systemd/system/hassio-rpi-bluetooth-extender.service
sudo systemctl daemon-reload
sudo systemctl enable hassio-rpi-bluetooth-extender.service