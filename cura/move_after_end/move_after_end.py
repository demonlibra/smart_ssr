# Переместить ось Z на заданное расстояние от детали в конце печати
# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class move_after_end(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Move axis in the end",
			"key": "moveafterend",
			"metadata": {},
			"version": 2,
			"settings":
			{
				"increase_z":
				{
					"label": "Increase Z",
					"description": "Increase distance between nozzle and model",
					"unit": "mm",
					"type": "float",
					"default_value": 50
				},
				
				"min_z":
				{
					"label": "Minimum Z",
					"description": "Minimum Z position",
					"unit": "mm",
					"type": "float",
					"default_value": 100
				}
			}
		}"""

	def execute(self, data: list):
		
		increase_z=self.getSettingValueByKey("increase_z")
		min_z=self.getSettingValueByKey("min_z")
		
		layer_last_Z = data[-4].split("\n")
	
		for line in layer_last_Z:
			if "G0" in line and "Z" in line:
				new_Z = float(line[line.find("Z")+1:]) + increase_z
				
				if new_Z < min_z:
					new_Z = min_z
					
				new_line = "G0 Z" + str(new_Z)
		
		last_layer = data[-2].split("\n")
		last_layer.insert(-1,new_line)
		data[-2] = '\n'.join(last_layer)
		
		return data
