echo "Pushed button - "`date` >> /home/pi/button

if [ -c /dev/ttyUSB0 ]
	then
		#stty 115200 -F /dev/ttyUSB0 raw -echo
		check_octo_connection=`curl -H "X-Api-Key: YOUR_API_KEY_FROM_OCTOPRINT_CONFIG" -X GET localhost:5000/api/printer`

		if [ "$check_octo_connection" != "Printer is not operational" ]			#If YES - OctoPrint is connected with Lerdge
			then
				echo "Lerdge is in ON state and connected with OctoPrint"
				sudo service octoprint stop
				echo "Send command M81 to turning off"
				echo "M81" > /dev/ttyUSB0
				sudo python /home/pi/neo_off.py
				sudo poweroff -p
			else
				echo "M115" > /dev/ttyUSB0;
				check_uart=`cat -v < /dev/ttyUSB0 & sleep 1 && kill %%`
				if [ "$check_uart" ]
					then
						echo "Lerdge in ON state and Not connected to Octoprint"
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
		fi

fi
