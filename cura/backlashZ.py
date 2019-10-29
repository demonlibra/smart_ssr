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
				"backlash_Z":
				{
					"label": "Backlash Z",
					"description": "Backlash Z",
					"unit": "mm",
					"type": "float",
					"default_value": 0.05
				}
			}
		}"""

	def execute(self, data: list):
		
		backlash=self.getSettingValueByKey("backlash_Z")
		
		flag = True
		index=0
		
		for layer in data:
			
			if not flag:
				break
				
			new_layer=""
			lines = layer.split("\n")
			
			for line in lines:
				if "G0" in line and flag:
					position_Z_in_line = line.rfind("Z")
					first_layer_Z=float(line[position_Z_in_line+1:])
					new_line = line[0:position_Z_in_line] + "Z" + str(first_layer_Z - backlash)
					new_layer += new_line + "\n" + line + "\n"
					flag = False
				else:
					new_layer += line + "\n"
					
			data[index] = new_layer
			
			index+=1

		return data