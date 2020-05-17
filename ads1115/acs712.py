import board
import busio
import time

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)

file = open("/home/pi/ads1115/acs712_zero_value","r")
zeropoint = float(file.readlines()[-1])
file.close
print("zero value = ", zeropoint)

duration = 5
average = [0]*duration
for j in range(duration):

	onesecond = [0]*10
	for i in range(10):
		chan = AnalogIn(ads, ADS.P0)
		onesecond[i] = (chan.voltage - zeropoint)/0.185
		time.sleep(0.1)

	average[j] = round(sum(onesecond)/len(onesecond),2)

file = open("/home/pi/ads1115/acs712_log","w")
for element in average:
	file.write(str(element))
	file.write('\n')
file.close
print(average)
