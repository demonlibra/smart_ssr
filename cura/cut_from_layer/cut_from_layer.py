# Добавляет движение вниз при каждой смене слоя

# This PostProcessing Plugin script is released 
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

class cut_from_layer(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Cut From Layer",
			"key": "cutfromlayer",
			"metadata": {},
			"version": 2,
			"settings":
			{
				"layer":
				{
					"label": "Cut From Layer",
					"description": "Cut from layer",
					"type": "int",
					"default_value": 2,
					"minimum_value": "2"
				}
			}
		}"""

	def execute(self, data: list):
		
		layer_cut=self.getSettingValueByKey("layer")						#Получаем значение переменной из формы
		
		if layer_cut > 2:
			
			number_of_layers = len(data)
			index = layer_cut + 2
			data = data[:index] + data[number_of_layers-1:]
				
		return data