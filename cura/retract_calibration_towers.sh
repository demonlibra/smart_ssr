#Обработка файлов retract_calibration_towers.gcode с разными значениями ретракта для CURA

							#Имена файлов
retract[0]="05.gcode"
retract[1]="10.gcode"
retract[2]="15.gcode"
retract[3]="20.gcode"

result="retract_test.gcode"	#Итоговый файл

step_layers=50				#Шагов между кубиками

row_num_start=1
next_layer=$step_layers

for file in "${retract[@]}";
	do
		i=$((i + 1))
				
		#echo "next="$next_layer
		
		next_layer=$(($step_layers * i + 1))
		
		row_num_next=`cat "$file" | grep -n "LAYER:"$next_layer | sed 's/^\([0-9]\+\):.*$/\1/'`
		
		sed -n $row_num_start,"$row_num_next"p $file >> retract_test.gcode
		
		row_num_start=$row_num_next
		
		#echo $file
		#echo $row_num_start
		#echo
	done