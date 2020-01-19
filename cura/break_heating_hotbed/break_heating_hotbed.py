# Добавляет движение вверх, на указанную величину, перед первым слоем.

# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class break_heating_hotbed(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Break Heating HotBed",
			"key": "break_M190",
			"metadata": {},
			"version": 2,
			"settings":
			{
				"number":
				{
					"label": "Number of break",
					"description": "Number of break for heating HotBed (M190)",
					"unit": "",
					"type": "int",
					"default_value": 10,
					"minimum_value": "0"
				},
				"pause":
				{
					"label": "Pause",
					"description": "Pause after get temperature of HotBed",
					"unit": "s",
					"type": "int",
					"default_value": 0,
					"minimum_value": "0"
				},
				"pause_auto_calc":
                {
                    "label": "Automatic calculate pause",
                    "description": "When enabled, pause for normalisation of table temperature will calculate automaticaly ( time(s) = temperature / 2 )",
                    "type": "bool",
                    "default_value": true
                },
				"rgb_code":
				{
					"label": "Code for RGB strip",
					"description": "Insert code for RGB strip before heating",
					"unit": "",
					"type": "str",
					"default_value": "M150 R250 S250"
				}
			}
		}"""

	def execute(self, data: list):
		
		number = self.getSettingValueByKey("number")
		pause = self.getSettingValueByKey("pause")
		pause_auto_calc = self.getSettingValueByKey("pause_auto_calc")
		rgb_code = self.getSettingValueByKey("rgb_code")
		
		if number > 0:

			layer = 1
			layer_lines = data[layer].split("\n")
			
			index = 0
			
			for line in layer_lines:
			
				if "M190" in line:

					position_S_in_line = line.rfind("S")
					temperature = int(line[position_S_in_line+1:])
					step = (temperature - 25) / ( number + 1 )

					temp = 25
					new_lines = [rgb_code]
					i = 0
					
					while i <= number:

						temp += step
						new_lines.append(line[:position_S_in_line+1] + str(int(temp)))
						i += 1
					
					if pause_auto_calc:
						new_lines.append('M0 S' + str(int(temperature / 2)))
					elif pause > 0:
						new_lines.append('M0 S' + str(pause))
						
					layer_lines = new_lines + layer_lines
					data[layer] = '\n'.join(layer_lines)
					break

		index += 1
			
		return data
