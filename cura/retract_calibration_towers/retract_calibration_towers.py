#Создание файла gcode для настройки ретрактов.
#Сценарий заменяет дистанцию ретрактов, заданных в параметрах материала

# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class retract_calibration_towers(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Retract Calibration Towers",
			"key": "retract_calibration",
			"metadata": {},
			"version": 2,
			"settings":
			{
				"steps":
				{
					"label": "Elements",
					"description": "Elements in tower",
					"unit": "",
					"type": "int",
					"default_value": 9,
					"minimum_value": "1"
				},
				"layers_step":
				{
					"label": "Layers in step",
					"description": "Number of layers in one step",
					"unit": "",
					"type": "int",
					"default_value": 50,
					"minimum_value": "0"
				},
				"initial_retract":
				{
					"label": "First step retract ",
					"description": "Retract distance in first step",
					"unit": "mm",
					"type": "float",
					"default_value": 0.5,
					"minimum_value": "0.1"
				},
				"retract_step":
				{
					"label": "Change retract",
					"description": "Value for change retract in each step",
					"unit": "mm",
					"type": "float",
					"default_value": 0.5,
					"minimum_value": "0.1"
				},
				"cut_gcode":
                {
                    "label": "Cut gcode",
                    "description": "Cut gcode after last element",
                    "type": "bool",
                    "default_value": true
                }
			}
		}"""

	def execute(self, data: list):
		
		steps = self.getSettingValueByKey("steps")										#Количество элементов башни
		layers_step = self.getSettingValueByKey("layers_step")							#Количество слоёв на элемент
		initial_retract = self.getSettingValueByKey("initial_retract")					#Длина ретракта на 1-м элементе
		retract_step = self.getSettingValueByKey("retract_step")						#Увеличение длины ретракта на следующем элементе
		cut_gcode = self.getSettingValueByKey("cut_gcode")								#Обрезать gcode после последнего элемента
		
		if steps > 0:
			
			step = 1
			retract = initial_retract
			layer_step_start = 1
			layer_step_finish = layers_step + 2
			E_before = 0.0
			E_now = 0.0
			
			while step <= steps:														#Цикл перебора элеметов
				
				for layer in range(layer_step_start,layer_step_finish):					#Цикл перебора слоев в элементе

					layer_lines = data[layer].split("\n")								#Формируем список из данных слоя
					index = 0
					
					for line in layer_lines:											#Цикл перебора строк в слое
						
						if "G1" in line and "E" in line:
							E_now = float(line[line.find("E")+1:])						#Длина ретракта в строке
							
						if E_before > E_now:											#Если координата оси экструдера данной строки меньше предыдущей, то это ретракт 
							new_line = line[:line.find("E")+1] + str(E_before - retract)	#Замена длины ретракта на заданную в параметрах сценария
							layer_lines[index] = new_line								#Замена строки в слое

						E_before = E_now												#Текущая позиция оси экструдера для последующего сравнения
						index += 1														#Номер строки в слое

					data[layer] = '\n'.join(layer_lines)								#Объединяем строки и возвращаем в слой
					
				layer_step_start = layer_step_finish									#Последний номер слоя в элементе как первый в следующем элементе
				layer_step_finish = layer_step_finish + layers_step						#Номер последнего слоя для следующего элемента
				step += 1																#Следущий элемент
				retract += retract_step													#Длина ретракта для следующего элемента
			
			if cut_gcode:																#Обрезка gcode после обработки заданного количества элементов
				number_of_layers = len(data)											#Количество элементов в списке данных (слоев)
				data = data[:layer_step_start] + data[number_of_layers-1:]
			
		return data
