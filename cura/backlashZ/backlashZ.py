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
		
		backlash_Z=self.getSettingValueByKey("backlashZ")
		
		if backlash_Z > 0:
			
			number_of_layers = len(data)

			for i in range(2,number_of_layers-2):								#Перебираем слои

				layer_lines = data[i].split("\n")
				index = len(layer_lines)-4

				if "G0" in layer_lines[index] and "Z" in layer_lines[index]:
					new_line = layer_lines[index]
					new_Z = float(new_line[new_line.find("Z")+1:]) + backlash_Z
					new_Z = round(new_Z,2)
					new_line = new_line[:new_line.find("Z")+1] + str(new_Z)
					layer_lines.insert(index,new_line)

				data[i] = '\n'.join(layer_lines)
				
		return data