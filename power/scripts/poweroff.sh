echo "M81" > /dev/ttyUSB0
sudo service octoprint stop
sudo python /home/pi/neo_off.py
sudo poweroff -p
