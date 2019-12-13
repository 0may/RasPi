#!/usr/bin/python3

import time
import VL53L1X
import simpleaudio as sa


def getDistanceVarianceFilter():
	global distIdx
	global distances
	global m
	global m2
	global v2

	distance_in_mm = tof.get_distance() # grab distance in mm

	if distance_in_mm > 0:

		# compute variance
		m = m + 0.2*distance_in_mm - 0.2*distances[distIdx]
		m2 = m2 + 0.2*distance_in_mm*distance_in_mm - 0.2*distances[distIdx]*distances[distIdx]
		v2 = m2 - m*m

		# update distances buffer
		distances[distIdx] = distance_in_mm
		distIdx = (distIdx + 1) % 5

#		print("{}  {}  {}".format(distance_in_mm, m, v2), end="...")

		# if variance is small enough, then trust the measurements
		if v2 < 10000.0:
			return m
		else:
			return 4000
	else:
		return 4000



distances = [4000, 4000, 4000, 4000, 4000]
distIdx = 0

m = 4000
m2 = 4000*4000
v2 = 0


# load wav file
soundObject = sa.WaveObject.from_wave_file('/media/usb/fuck.wav')


# init ranging device
try:
	print("\n>> Ranging device info")
	tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
	tof.open() 	     # Initialise the i2c bus and configure the sensor
	time.sleep(0.2)
except:
	print("\n!! Failed to open ranging device. Exiting !!")
	raise SystemExit


tof.set_timing(66000, 70)
tof.start_ranging(3) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range


playObject = soundObject.play()

run = True

while run:

	try:
		dist = getDistanceVarianceFilter()

		if dist < 2000.0 and not playObject.is_playing():
			playObject = soundObject.play()

		time.sleep(0.02)

	except KeyboardInterrupt:
		print("\n>> Exiting")
		run = False
		playObject.stop()
		time.sleep(0.1)


tof.stop_ranging() # Stop ranging
