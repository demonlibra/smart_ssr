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
chan2 = AnalogIn(ads, ADS.P2)	# Input for HW670

# ADC Configuration
ads.mode = Mode.CONTINUOUS
ads.data_rate = RATE

#Read from file last zero value for DC sensor ACS712
file = open("/home/pi/ads1115/acs712_zero_value","r")
zeropoint = float(file.readlines()[-1])
file.close
print("zero value ACS712 = ", zeropoint, '\n')

acs712 = []
hw670 = []
acs712_moment = []
hw670_moment = []

start = time.monotonic()

try:
	time.sleep( 1 - time.time()%1 )		# Synchronize with second start x.000000000000
	while True:

		count = 0			# Counting measures

		# ACS712 - DC
		while time.time()%1 < 0.5:
			acs712_moment.append( (chan0.voltage - zeropoint) / 0.185 )
			count += 1
			try:
				time.sleep( count * sample_time - time.time()%1 )
			except ValueError:
				nothing_to_do = 0

		acs712.append(round( sum(acs712_moment) / len(acs712_moment) ,3 ))
		acs712_moment.clear()

		print('ACS712 - end time:', time.strftime("%H:%M:%S"), 'counts=', count, 'Idc = ', acs712[-1])

		# HW670 - AC
		while 0.5 < time.time()%1 < 1.0:
			hw670_moment.append(chan2.voltage)

			count += 1
			try:
				time.sleep( count * sample_time - time.time()%1 )
			except ValueError:
				nothing_to_do = 0

		hw670.append(round( 0.707 * (max(hw670_moment) - min(hw670_moment)) / 2, 3 ))
		hw670_moment.clear()

		print('HW670  - end time:', time.strftime("%H:%M:%S"), 'counts=', count, 'Iac = ', hw670[-1], '\n' )

except KeyboardInterrupt:

	file = open("/home/pi/ads1115/acs712_log","w")
	for element in acs712:
		file.write(str(element))
		file.write('\n')
	file.close

	file = open("/home/pi/ads1115/hw670_log","w")
	for element in hw670:
		file.write(str(element))
		file.write('\n')
	file.close

#print("ACS712:", acs712)
#print("HW670:", hw670)

end = time.monotonic()
total_time = end - start
print("\nTotal time:", total_time)
