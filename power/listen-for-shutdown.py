#!/usr/bin/env python


import RPi.GPIO as GPIO
import subprocess
import time

pin_number = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
	GPIO.wait_for_edge(pin_number, GPIO.FALLING)
	#GPIO.input(
	subprocess.call(["bash", "/home/pi/power_managment.sh"])
	#subprocess.call(['shutdown', '-h', 'now'], shell=False)
	time.sleep(3)


