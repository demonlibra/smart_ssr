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
				"start_temp":
				{
					"label": "Break from temperature",
					"description": "Break from temperature",
					"unit": "C",
					"type": "int",
					"default_value": 25,
					"minimum_value": "20",
					"maximum_value": "100"
				},
				"number":
				{
					"label": "Number of break",
					"description": "Number of break for heating HotBed (M190)",
					"unit": "",
					"type": "int",
					"default_value": 10,
					"minimum_value": "3"
				},
				"pause_between_break":
				{
					"label": "Pause between break",
					"description": "Pause between break",
					"unit": "s",
					"type": "int",
					"default_value": 0,
					"minimum_value": "0"
				},
				"pause_before_print":
				{
					"label": "Pause before print",
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
		
		start_temp = self.getSettingValueByKey("start_temp")
		number = self.getSettingValueByKey("number")
		pause_between_break = self.getSettingValueByKey("pause_between_break")
		pause_before_print = self.getSettingValueByKey("pause_before_print")
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
					step = (temperature - start_temp) / (number - 1)

					if "M150" in rgb_code:
						new_lines = ['M150 S0',rgb_code]
					elif rgb_code:
						new_lines = [rgb_code]
					else:
						new_lines = []
						
					i = 1
					
					temp = start_temp
					while i <= number:

						new_lines.append(line[:position_S_in_line+1] + str(int(temp)))
						if pause_between_break > 0 and i < number:
							new_lines.append("M0 S" + str(pause_between_break))
						i += 1
						temp += step
					
					if pause_auto_calc:
						new_lines.append('M0 S' + str(int(temperature / 2)) + '; PAUSE')
					elif pause_before_print > 0:
						new_lines.append('M0 S' + str(pause_before_print) + '; PAUSE')
						
					layer_lines = new_lines + layer_lines
					data[layer] = '\n'.join(layer_lines)
					break

		index += 1
			
		return data
