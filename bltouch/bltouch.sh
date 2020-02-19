#------------------- Параметры -------------------------------------------------------

MIN_X=20				#Минимальная координата X
MIN_Y=20				#Минимальная координата Y

MAX_X=230				#Максимальная координата X
MAX_Y=170				#Максимальная координата Y

POINTS_X=10				#Точек измерения вдоль оси X
POINTS_Y=7				#Точек измерения вдоль оси Y

file_data="bltouch_lerdge_output"	#Файл вывода данных от Lerdge
file_mesh="bltouch_mesh"		#Файл сетки координат
gnuplot_script="bltouch_gnuplot"	#Сценарий для программы построения поверхности
file_png="bltouch_plot"			#Файл вывода изображения поверхности

$temperatura=25				#Температура нагрева стола
#-------------------------------------------------------------------------------------


time_stamp=$(date +%F-%H-%M)					#Дата и время	

stty 115200 -F /dev/ttyUSB0 raw -echo				#Задаем параметры порта UART
sleep 3

cat /dev/ttyUSB0 > "$file_data"_"$time_stamp" &			#Сбор данных вывода результатов в файл

if [[ $temperatura -gt 25 ]]					#Греть ли стол		
	then echo "M140 S$temperatura" > /dev/ttyUSB0
fi

echo "G28" > /dev/ttyUSB0					#Обнуляем оси

if [[ $POINTS_X -gt 1 ]]
	then STEP_X=$(( ($MAX_X-$MIN_X) / ($POINTS_X-1) ))	#Расчет шага по оси X
	else STEP_X=$MAX_X
fi

if [[ $POINTS_Y -gt 1 ]]
	then STEP_Y=$(( ($MAX_Y-$MIN_Y) / ($POINTS_Y-1) ))	#Расчет шага по оси Y
	else STEP_Y=$MAX_Y
fi

Y=$MIN_Y
while [[ $Y -le $MAX_Y ]]
	do
		X=$MIN_X
		while [[ $X -le $MAX_X ]]
			do
				echo "G30 X$X Y$Y P1" > /dev/ttyUSB0
				X=$(( $X + $STEP_X ))
			done
		Y=$(( $Y + $STEP_Y ))
	done 

echo ; echo ------------------ ; read -p "Нажмите ENTER после завершения измерений"
killall -q cat

echo "#BL-TOUCH MESH" > "$file_mesh"_"$time_stamp"

i=1
cat "$file_data"_"$time_stamp" | while read line
do
	if [[ `echo $line | grep -c "Starts probing"` = 0 ]] && [[ `echo $line | grep -c "position of the Z-axis"` = 1 ]]
		then
			line=`echo $line | sed s/"Z-axis"//g`
			line=`echo $line | sed s/[^0-9.:,-]//g`
			line=`echo $line | sed 's/\(:\|\,\)/ /g'`
			echo $line >> "$file_mesh"_"$time_stamp"
			
			i=$(( $i + 1 ))
			if [[ $i = $(($POINTS_X + 1)) ]]; then i=1; echo "" >> "$file_mesh"_"$time_stamp"; fi
		fi
done

path1="$HOME/bltouch/$file_mesh"_"$time_stamp"
path2="$HOME/bltouch/$file_png"_"$time_stamp".png
gnuplot -e "file_mesh=\"$path1\"" -e "file_out=\"$path2\"" "$gnuplot_script"
