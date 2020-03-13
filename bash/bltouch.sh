#!/bin/bash

min_move=10
max_move=50
repeats=10
center_X="125"
center_Y="90"

stty 115200 -F /dev/ttyUSB0 raw -echo
sleep 3
echo "G28 XY" > /dev/ttyUSB0
echo "G0 X${center_X} Y${center_Y}" > /dev/ttyUSB0
echo "G28 Z" > /dev/ttyUSB0
echo "G0 F3000 Z10" > /dev/ttyUSB0

for ((i=1; i < $repeats; i++))
	do
		random_move_X=`shuf -i $min_move-$max_move -n 1`
		random_sign_X=`shuf -i 0-1 -n 1`
		if [[ "$random_sign_X" = "0" ]]
			then
				sign_X="-"
			else
				sign_X=""
		fi

		random_move_Y=`shuf -i $min_move-$max_move -n 1`
                random_sign_Y=`shuf -i 0-1 -n 1`
                if [[ "$random_sign_Y" = "0" ]]
                        then
                                sign_Y="-"
                        else 
                                sign_Y=""
                fi
		echo "G0 F3000 X${signX}${random_move_X} Y${sign_Y}${random_move_Y} R" > /dev/ttyUSB0
		#read -p "Нажмите ENTER чтобы продолжить"
		echo "M400" > /dev/ttyUSB0
		echo "M114 L" > /dev/ttyUSB0
		echo "G30 X${center_X} Y${center_Y}" > /dev/ttyUSB0
done