# Добавляет движение вверх, на указанную величину, перед первым слоем.

# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class backlashZ_first_layer(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Backlash Z First Layer",
			"key": "BacklashZFL",
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
					"default_value": 0.1,
					"minimum_value": "0",
					"maximum_value": "0.1"
				}
			}
		}"""

	def execute(self, data: list):
		
		backlash_Z=self.getSettingValueByKey("backlashZ")						#Получаем значение переменной из формы
		
		if backlash_Z > 0:
			
			layer = 2
			layer_lines = data[layer].split("\n")
			
			index = 0
			
			for line in layer_lines:
					
				if "G0" in line and "Z" in line:
					position_Z_in_line = line.rfind("Z")
					first_layer_Z=float(line[position_Z_in_line+1:])
					new_Z = float(first_layer_Z) - backlash_Z
					
					new_line = line[:position_Z_in_line+1] + str(new_Z)

					layer_lines.insert(index,new_line)	
					#layer_lines[index] =  new_line + "\n" + line
					data[layer] = '\n'.join(layer_lines)
					break
				index += 1
			
		return data
