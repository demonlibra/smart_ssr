# Добавляет код перед и после движения по Z при смене слоя

# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class code_around_Z(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Code around Z move",
			"key": "codearoundZ",
			"metadata": {},
			"version": 2,
			"settings":
			{
				"before_move":
				{
					"label": "Insert before Z move",
					"description": "Insert before Z move",
					"unit": "",
					"type": "str",
					"default_value": "M150 B250 S250"
				},
				"after_move":
				{
					"label": "Insert after Z move",
					"description": "Insert after Z move",
					"unit": "",
					"type": "str",
					"default_value": "M150 S0;M150 S250"
				}
			}
		}"""

	def execute(self, data: list):
		
		before_move=self.getSettingValueByKey("before_move")
		after_move=self.getSettingValueByKey("after_move")
		
		after_move=after_move.split(";")
		before_move=before_move.split(";")
		
		if 1 > 0:
			
			number_of_layers = len(data)

			for i in range(2,number_of_layers-2):

				layer_lines = data[i].split("\n")
				index = len(layer_lines)-4

				if "G0" in layer_lines[index] and "Z" in layer_lines[index]:
					j = 0
					for line_after in after_move:
						layer_lines.insert(index+1+j,line_after)
						j += 1
					k = 0
					for line_before in before_move:
						layer_lines.insert(index+k,line_before)
						k += 1
				data[i] = '\n'.join(layer_lines)
				
		return data