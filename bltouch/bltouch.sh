#------------------- Параметры -------------------------------------------------------

MIN_X=20							#Минимальная координата X
MIN_Y=20							#Минимальная координата Y

MAX_X=230							#Максимальная координата X
MAX_Y=180							#Максимальная координата Y

POINTS_X=10							#Точек измерения вдоль оси X
POINTS_Y=7							#Точек измерения вдоль оси Y

file_data="bltouch_lerdge_output"	#Файл вывода данных от Lerdge
file_mesh="bltouch_mesh"			#Файл сетки координат
file_plot="bltouch_plot"			#Сценарий для программы построения поверхности
file_png="bltouch_plot.png"			#Файл вывода изображения поверхности
#-------------------------------------------------------------------------------------
stty 115200 -F /dev/ttyUSB0 raw -echo
sleep 3
cat /dev/ttyUSB0 > "$file_data" &

STEP_X=$(( ($MAX_X-$MIN_X) / ($POINTS_X-1) ))
STEP_Y=$(( ($MAX_Y-$MIN_Y) / ($POINTS_Y-1) ))

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

echo "#BL-TOUCH MESH" > "$file_mesh"

i=1
cat "$file_data" | while read line
do
	if [[ `echo $line | grep -c "Starts probing"` = 0 ]] && [[ `echo $line | grep -c "position of the Z-axis"` = 1 ]]
		then
			line=`echo $line | sed s/"Z-axis"//g`
			line=`echo $line | sed s/[^0-9.:,-]//g`
			line=`echo $line | sed 's/\(:\|\,\)/ /g'`
			echo $line >> "$file_mesh"
			
			i=$(( $i + 1 ))
			if [[ $i = $(($POINTS_X + 1)) ]]; then i=1; echo "" >> "$file_mesh"; fi
		fi
done

gnuplot -e "file_mesh=\"$HOME/bltouch/$file_mesh\"" -e "file_out=\"$HOME/bltouch/$file_png\"" bltouch_plot
