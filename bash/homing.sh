#!/bin/bash

# Сценария для выполнения ручной процедуры регулировки стола
# ----------------------------------------------------------

# Параметры

usb=/dev/ttyUSB0		# Путь обращения к плате
uart_speed=115200		# Скорость порта UART (для LERDGE 115200)

# ----------------------------------------------------------

stty $uart_speed -F $usb raw -echo

echo "G28" > $usb
grep -m 1 'ok' < $usb >&2

clear
echo -n "Выполнить процедуру калибровки стола? (y) "
read answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]
	then
		while :
			do
				clear
				echo
				echo "Введите позицию или нажмите ввод для перемещения в безопасную зону."
				echo "-----------";echo "|1       2|";echo "|         |";echo "|    5    |";echo "|         |";echo "|3       4|";echo "-----------"
				echo -n "Переместить сопло в позицию: "
				read position
					
				if [ "$position" = 1 ]
					then
						echo "G0 F800 Z10" > $usb
						echo "G0 F1000 X20 Y20" > $usb
						echo "G0 F500 Z0" > $usb
						
				elif [ "$position" = 2 ]
					then
						echo "G0 F500 Z10" > $usb
						echo "G0 F1000 X200 Y20" > $usb
						echo "G0 F500 Z0" > $usb
				
				elif [ "$position" = 3 ]
					then
						echo "G0 F500 Z10" > $usb
						echo "G0 F1000 X200 Y175" > $usb
						echo "G0 F500 Z0" > $usb
						
				elif [ "$position" = 4 ]
					then
						echo "G0 F500 Z10" > $usb
						echo "G0 F1000 X20 Y175" > $usb
						echo "G0 F500 Z0" > $usb
						
				elif [ "$position" = 5 ]
					then
						echo "G0 F800 Z10" > $usb
						echo "G0 F1000 X110 Y95" > $usb
						echo "G0 F500 Z0" > $usb
				else
					echo "G0 F800 Z10 R" > $usb
					echo "G0 F500 X20 Y20 Z50" > $usb
					echo "M18" > $usb
					echo 1
					echo 2
				fi
			
		done
fi





