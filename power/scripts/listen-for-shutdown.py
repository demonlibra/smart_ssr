#!/usr/bin/env python


import RPi.GPIO as GPIO
import subprocess
import time

pin_number = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	GPIO.wait_for_edge(pin_number, GPIO.FALLING)
	
	time.sleep(0.3)
	button_state = GPIO.input(pin_number)
	
	if not button_state:
		subprocess.call(["bash", "/home/pi/power_managment.sh"])
	time.sleep(5)




