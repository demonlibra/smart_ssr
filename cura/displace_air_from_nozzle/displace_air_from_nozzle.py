# Выдавить заданную длину пластика и сделать ретракт в указанном месте

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
					"default_value": 6,
					"minimum_value": "0"
				},
				"speeddisplace":
				{
					"label": "Speed displace",
					"description": "Speed to displace the air from nozzle",
					"unit": "mm/s",
					"type": "int",
					"default_value": 10,
					"minimum_value": "1"
				},
				"retractlength":
				{
					"label": "Retract Length",
					"description": "Length of retract",
					"unit": "mm",
					"type": "float",
					"default_value": 2,
					"minimum_value": "0"
				},
				"retractspeed":
				{
					"label": "Retract Speed",
					"description": "Retract speed",
					"unit": "mm/s",
					"type": "int",
					"default_value": 25,
					"minimum_value": "1"
				},
				"positionX":
				{
					"label": "Position X",
					"description": "Position X",
					"unit": "mm",
					"type": "float",
					"default_value": 125
				},
				"positionY":
				{
					"label": "Position Y",
					"description": "Position Y",
					"unit": "mm",
					"type": "float",
					"default_value": 70
				},
				"positionZ":
				{
					"label": "Position Z",
					"description": "Position Z",
					"unit": "mm",
					"type": "float",
					"default_value": 40
				},
				"positionspeed":
				{
					"label": "Speed movement",
					"description": "Speed movement",
					"unit": "mm/s",
					"type": "int",
					"default_value": 30
				},
				"pause":
				{
					"label": "Pause",
					"description": "Pause after displace",
					"unit": "s",
					"type": "int",
					"default_value": 1,
					"minimum_value": "0"
				}
			}
		}"""

	def execute(self, data: list):
		
		length=self.getSettingValueByKey("filamentlength")
		
		speed_displace=self.getSettingValueByKey("speeddisplace")
		speed_displace=speed_displace*60 
		
		retract=self.getSettingValueByKey("retractlength")
		
		retract_speed=self.getSettingValueByKey("retractspeed")
		retract_speed=retract_speed*60
		
		position_X=self.getSettingValueByKey("positionX")
		position_Y=self.getSettingValueByKey("positionY")
		position_Z=self.getSettingValueByKey("positionZ")
		
		position_speed=self.getSettingValueByKey("positionspeed")
		position_speed=position_speed*60
		
		pause=self.getSettingValueByKey("pause")
		
		if length > 0:
		
			layer=data[1]
			layer_lines = data[1].split("\n")
			
			index=0
			
			for line in layer_lines:
				
				if "G92" in line:
					
					new_lines = "M17" + "\n"
					new_lines = new_lines + "G0 F" + str(position_speed) + " X" + str(position_X) + " Y" + str(position_Y) + " Z" + str(position_Z) + "\n"
					new_lines = new_lines + "G1 F" + str(speed_displace) + " E" + str(length) + " R" + "\n"
					new_lines = new_lines + "G92 E0" + "\n"
					new_lines = new_lines + "G1 F" + str(retract_speed) + " E-" + str(retract)
					if pause > 0:
						new_lines = new_lines + "\n" + "M0 S" + str(pause)
					layer_lines[index+1] =  layer_lines[index+1] + "\n" + new_lines
					data[1] = '\n'.join(layer_lines)
					break
				index += 1
			
		return data