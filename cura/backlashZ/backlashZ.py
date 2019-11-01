# Добавляет движение вниз при каждой смене слоя

# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class backlashZ(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Backlash Z",
			"key": "BacklashZ",
			"metadata": {},
			"version": 2,
			"settings":
			{
				"backlashZ":
				{
					"label": "Backlash Z",
					"description": "Backlash Z",
					"unit": "mm",
					"type": "float",
					"default_value": 0.05,
					"minimum_value": "0"
				}
			}
		}"""

	def execute(self, data: list):
		
		backlash_Z=self.getSettingValueByKey("backlashZ")						#Получаем значение переменной из формы
		
		if backlash_Z > 0:
			
			number_of_layers = len(data)										#Получаем количество элементов в списке данных (слоев)

			for i in range(2,number_of_layers-2):								#Перебираем список/слои

				layer_lines = data[i].split("\n")								#Формируем из слоя список 
				index = len(layer_lines)-4										#Номер существующей строки с перемещением по Z

				if "G0" in layer_lines[index] and "Z" in layer_lines[index]:	#Выполнять только если строка содержит G0 и Z
					new_line = layer_lines[index]								#Получаем строку с перемещением по Z
					new_Z = float(new_line[new_line.find("Z")+1:]) + backlash_Z	#Выделяем значение Z и вычисляем новое значение 
					new_Z = round(new_Z,2)	#Округляем Z до сотых
					new_line = new_line[:new_line.find("Z")+1] + str(new_Z)		#Формируем новую строку для вставки в список
					layer_lines.insert(index,new_line)							#Вставляем новую строку в список со сдвигом

				data[i] = '\n'.join(layer_lines)								#Объединяем список в данные и возвращаем в слой
				
		return data