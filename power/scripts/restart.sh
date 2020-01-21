echo "M999" > /dev/ttyUSB0
sudo service octoprint stop
sudo python /home/pi/neo_off.py
sudo reboot
