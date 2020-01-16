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
				}
			}
		}"""

	def execute(self, data: list):
		
		steps = self.getSettingValueByKey("steps")
		layers_step = self.getSettingValueByKey("layers_step")
		initial_retract = self.getSettingValueByKey("initial_retract")
		retract_step = self.getSettingValueByKey("retract_step")
		
		if steps > 0:
			
			number_of_layers = len(data)												#Получаем количество элементов в списке данных (слоев)
			
			step = 1
			retract = initial_retract
			layer_step_start = 1
			layer_step_finish = layers_step + 2
			E_before = 0.0
			E_now = 0.0
			
			while step <= steps:
				
				for layer in range(layer_step_start,layer_step_finish):					#Перебираем список/слои

					layer_lines = data[layer].split("\n")								#Формируем список из данных слоя
					index = 0
					
					for line in layer_lines:
						
						if "G1" in line and "E" in line:
							E_now = float(line[line.find("E")+1:])
							
						if E_before > E_now:
							#new_line = "Index=" + str(index) + " " + "step=" + str(step) + " " + str(E_before - retract)
							new_line = line[:line.find("E")+1] + str(E_before - retract)
							layer_lines[index] = new_line

						E_before = E_now
						index += 1

					data[layer] = '\n'.join(layer_lines)								#Объединяем список в данные и возвращаем в слой
					
				layer_step_start = layer_step_finish
				layer_step_finish = layer_step_finish + layers_step
				step += 1
				retract += retract_step

		return data
