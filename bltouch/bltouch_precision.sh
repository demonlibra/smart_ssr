#!/bin/bash

#------------------- Параметры -------------------------------------------------------

min_X=30				#Минимальное хаотичное движение
max_X=230				#Максимальное хаотичное движение
min_Y=30
max_Y=170
repeats=10				#Количество повторов измерения в точке
center_X="147.5"				#Координата X центра
center_Y="71"				#Координата Y центра

mesure_X=122
mesure_Y=90
file_data="bltouch_lerdge_output"	#Файл вывода данных от Lerdge

#--------------------Сценарий---------------------------------------------------------

time_stamp=$(date +%F-%H-%M)					#Дата и время

#stty 115200 -F /dev/ttyUSB0 raw -echo
cat /dev/ttyUSB0 > "$file_data"_"$time_stamp" &			#Сбор данных вывода результатов в файл
sleep 3

echo "G0 Z20 R" > /dev/ttyUSB0
echo "G28 XY" > /dev/ttyUSB0					#Обнуление осей X и Y
echo "G0 X${center_X} Y${center_Y}" > /dev/ttyUSB0		#Перемещение головы в центр стола
echo "G28 Z" > /dev/ttyUSB0					#Обнуление оси Z
echo "G0 F3000 Z10" > /dev/ttyUSB0

for ((i=1; i <= $repeats; i++))
	do
		random_move_X=`shuf -i $min_X-$max_X -n 1`
		random_move_Y=`shuf -i $min_Y-$max_Y -n 1`
               	echo "G0 F3000 X${random_move_X} Y${random_move_Y}" > /dev/ttyUSB0
		#echo "M400" > /dev/ttyUSB0
		echo "G0 X${center_X} Y${center_Y}" > /dev/ttyUSB0
		echo "G30 X${mesure_X} Y${mesure_Y}" > /dev/ttyUSB0
done

echo ; echo ------------------ ; read -p "Нажмите ENTER после завершения измерений"
killall -q cat

touch $file_data_$time_stamp"_mesure"
cat "$file_data"_"$time_stamp" | while read line
do
	if [[ `echo $line | grep -c "Starts probing"` = 0 ]] && [[ `echo $line | grep -c "position of the Z-axis"` = 1 ]]
		then
			mesure="${line##*:}"
			echo "$mesure" >> $file_data_$time_stamp"_mesure"
	fi
done
