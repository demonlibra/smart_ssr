#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

pin_number = 17

print "Switch On/Off Relay"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_number, GPIO.OUT)	#устанавливаем пин на выходной сигнал

GPIO.output(pin_number, GPIO.HIGH)	#ставим логическую единицу на выходе
time.sleep(3)
GPIO.output(pin_number, GPIO.LOW)	#ставим логическую единицу на выходе
