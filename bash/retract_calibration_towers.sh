# --- Объединение gcode с разными значениями ретракта после слайсера CURA --- #

# --- Как пользоваться? --- #

	# 1. Создайте gcode с разными значениями ретракта для модели "retract_calibration_towers.stl"
	# 2. Проверьте параметры ниже
	# 2. Запустите сценарий в терминале командой "bash retract_calibration_towers.sh"


# --- Проверьте параметры --- #

	path="$HOME"									#Путь к файлам gcode с разными ретрактами ($HOME - домашний каталог)

	retract[0]="05.gcode"							#Имена файлов
	retract[1]="10.gcode"
	retract[2]="15.gcode"
	retract[3]="20.gcode"
	#retract[4]="xxx.gcode"							#Шаблон имени файла
	
	result="$HOME/retract_calibration_towers.gcode"	#Путь и имя файла на выходе сценария

	step_layers=50									#Шагов между кубиками (для модели "retract_calibration_towers.stl" равно 50 при высоте слоя 0.2)

# ========================================================================== #

# --- Текст сценария обработки --- #

row_num_start=1
next_layer=$step_layers
i=0

for file in "${retract[@]}";																			#Цикл обработки каждого файла
	do
		if ! [ -f "$path/$file" ]																		#Проверка существования файла
			then
				echo "!!! Указанный файл \"$path/$file\" не существует"
				echo "!!! Проверьте параметры и запустие сценарий еще раз"
				exit
			fi
			
		i=$((i + 1))
				
		next_layer=$(($step_layers * i + 1))															#Расчет номера слоя смены значения ретракта
		row_num_next=`cat "$path/$file" | grep -n "LAYER:"$next_layer | sed 's/^\([0-9]\+\):.*$/\1/'`	#Получение номера строки в файле
		sed -n $row_num_start,"$row_num_next"p "$path/$file" >> "$result"								#Извлечение части gcode и запись в файл
		row_num_start=$row_num_next
	done
	
echo "Объединение gcode с разными значениями ретракта после слайсера CURA"
echo "Завершено"