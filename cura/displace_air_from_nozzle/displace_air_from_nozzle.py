# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class displace_air_from_nozzle(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Displace Air from the Nozzle",
			"key": "displace_air",
			"metadata": {},
			"version": 2,
			"settings":
			{
				"filamentlength":
				{
					"label": "Filament Length",
					"description": "Length of filament to displace the air from nozzle",
					"unit": "mm",
					"type": "float",
					"default_value": 5,
					"minimum_value": "0"
				},
				"speeddisplace":
				{
					"label": "Speed displace",
					"description": "Speed to displace the air from nozzle",
					"unit": "mm",
					"type": "int",
					"default_value": 500,
					"minimum_value": "100"
				},
				"retractlength":
				{
					"label": "Retract Length",
					"description": "Length of retract",
					"unit": "mm",
					"type": "float",
					"default_value": 1,
					"minimum_value": "0"
				},
				"retractspeed":
				{
					"label": "Retract Speed",
					"description": "Retract speed",
					"unit": "mm",
					"type": "int",
					"default_value": 1500,
					"minimum_value": "100"
				}
			}
		}"""

	def execute(self, data: list):
		
		length=self.getSettingValueByKey("filamentlength")
		speed=self.getSettingValueByKey("speeddisplace")
		
		retract=self.getSettingValueByKey("retractlength")
		retract_speed=self.getSettingValueByKey("retractspeed")
		
		if length > 0:
		
			layer=data[1]
			layer_lines = data[1].split("\n")
			
			index=0
			
			for line in layer_lines:
				
				if "M82" in line:
					new_lines = "M17 E" + "\n"
					new_lines = new_lines + "G1 F" + str(speed) + " E" + str(length) + " R" + "\n"
					new_lines = new_lines + "G1 F" + str(retract_speed) + " E-" + str(retract) + " R" + "\n"
					layer_lines[index] =  new_lines + layer_lines[index]

				index += 1
			
			data[1] = '\n'.join(layer_lines)
			
		return data