echo "Pushed button - "`date` >> /home/pi/button
if [ -c /dev/ttyUSB0 ]
	then
		#stty 115200 -F /dev/ttyUSB0 raw -echo
		echo "M115" > /dev/ttyUSB0;
		check=`cat -v < /dev/ttyUSB0 & sleep 1 && kill %%`

		if [ "$check" ]
			then
				echo "Lerdge in ON state"
				echo "Send command M81 to turning off"
				
				echo "M81" > /dev/ttyUSB0
				sudo service octoprint stop
				sudo python /home/pi/neo_off.py
				sudo poweroff -p

			else
				echo "Lerdge in Off state"
				echo "Switch on SSR Relay module"
				
				python /home/pi/relay_lerdge_on.py
			fi
	else
		python /home/pi/relay_lerdge_on.py
fi
