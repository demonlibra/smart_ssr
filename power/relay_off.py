#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import ConfigParser

config = ConfigParser.RawConfigParser()            #воспользуемся конфигом
config.read("/home/pi/global_config.conf")         #считаем конфиг
pin_number = config.getint("relay_pins", "relay1") #пина из конфига присвоем переменной pin_number

print "use pin:"+str(pin_number)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_number, GPIO.OUT)   #устанавливаем пин на выходной сигнал
GPIO.output(pin_number, GPIO.LOW)  #ставим логический ноль на выходе
