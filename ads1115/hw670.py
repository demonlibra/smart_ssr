import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

# Data collection setup
RATE = 860
SAMPLES = 50 

# Create the I2C bus with a fast frequency
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)

# ADC Configuration
ads.mode = Mode.CONTINUOUS
ads.data_rate = RATE

data = [None] * SAMPLES
current = []
j = 0
while j < 5:
	start = time.monotonic()

	# Read the same channel over and over
	for i in range(SAMPLES):
		data[i] = chan0.voltage
		time.sleep(0.0011)

	end = time.monotonic()
	total_time = end - start

	print("Time of capture: {}s".format(total_time))
	print("Sample rate requested={} actual={}".format(RATE, SAMPLES / total_time))
	#print(data)

	#print("maximum =", max(data)
	#print("minimum =", min(data)

	current.append(round(0.707 * (max(data) - min(data)) / 2, 1))
	print("current = ", current[-1])

	time.sleep(1)
	j += 1

#export data to file
file = open("/home/pi/ads1115/hw670.log", "w")
for element in current:
	file.write(str(element))
	file.write('\n')
file.close
