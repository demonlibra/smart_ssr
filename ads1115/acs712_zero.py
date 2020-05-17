import board
import busio
import time

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

# Data collection setup
RATE = 860
sample_time = 1 / RATE		# Time for one measure

# Create the I2C bus with a fast frequency
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0 and 2
chan0 = AnalogIn(ads, ADS.P0)	# Input for ACS712

# ADC Configuration
ads.mode = Mode.CONTINUOUS
ads.data_rate = RATE

acs712_moment = []

count = 0			# Counting measures
time.sleep( 1 - time.time()%1 )	# Synchronize with second start x.000000000000

# ACS712 - DC
while count < RATE:
	acs712_moment.append(chan0.voltage)
	count += 1
	try:
		time.sleep( count * sample_time - time.time()%1 )
	except ValueError:
		nothing_to_do = 0

calibrate = sum(acs712_moment) / len(acs712_moment)

print('reference value = ', calibrate)
print(count)

file = open("/home/pi/ads1115/acs712_zero_value","a")	#Write zero value to file
file.write('\n' + str(calibrate))
file.close
