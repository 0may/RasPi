##############################################################################
# Software License Agreement (BSD License)
#
# Copyright (c) 2018 Oliver Mayer, Academy of Fine Arts Nuremberg.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##############################################################################
 
import sys
import pygame as pg
import os
import time
import thread
import random
import VL53L1X
import yaml


### function to play an audio file with pygame
def play_music(music_file):

	clock = pg.time.Clock()
	try:
		pg.mixer.music.load(music_file)
	except pg.error:
		print("File {} not found! {}".format(music_file, pg.get_error()))
		return

	pg.mixer.music.play()

	while pg.mixer.music.get_busy():
		clock.tick(30)

### function to adjust volume based on range measurements
def rangingThread(threadName, delay):
	global runTriggerThread
	global distances
	global distIdx
	global distMin
	global distMax
	global volume
	global volumeMin
	global volumeMax
	global volumeUpdateRate
	global range
	global debug

	print("\n>> Ranging device info")
	tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
	tof.open() 	     # Initialise the i2c bus and configure the sensor
	tof.start_ranging(range) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range

	while runTriggerThread:
		distance_in_mm = tof.get_distance() # Grab the range in mm

		if distance_in_mm > 0:

			distances[distIdx] = distance_in_mm
			distIdx = (distIdx + 1) % 5

			distsSorted = sorted(distances)
			distSmooth = (distsSorted[1] + distsSorted[2] + distsSorted[3])/3.0

			distStr = "{} mm".format(distSmooth)

			if distSmooth < distMin:
				distSmooth = distMin
			elif distSmooth > distMax:
				distSmooth = distMax

			distSmooth -= distMin

			volume = (volumeMin + (volumeMax-volumeMin)*(1.0 - distSmooth/(distMax-distMin)))*volumeUpdateRate + volume*(1.0-volumeUpdateRate)
			volume = round(volume, 2)

			if debug != 0:
				print("volume: {}  --  distance: {}".format(volume, distStr))

			pg.mixer.music.set_volume(volume)

		time.sleep(delay)

	tof.stop_ranging() # Stop ranging





### init global variables with default values

samplingrate = 44100 # in Hz
bitsize = -16        # signed 16 bit
channels = 2         # 1 is mono, 2 is stereo
buffer = 2048        # number of samples (experiment to get right sound)

volumeMin = 0.2
volumeMax = 1.0
volumeUpdateRate = 0.7

distances = [2000, 2000, 2000, 2000, 2000]
distIdx = 0
distMin = 200
distMax = 700

range = 2
debug = 0
randomPlay = 0

### read setting from file

try:
	with open("/brainspeakers/brainspeakers_settings.yml", 'r') as ymlfile:
		settings = yaml.load(ymlfile)

	samplingrate = settings['sampling_rate']
	bitsize = settings['bitsize']
	channels = settings['channels']
	buffer = settings['buffersize']
	volumeMin = settings['volume_min']
	volumeMax = settings['volume_max']
	volumeUpdateRate = settings['volume_update_rate']
	distMin = settings['distance_min']
	distMax = settings['distance_max']
	range = settings['range_mode']
	debug = settings['print_debug_info']
	randomPlay = settings['random_play']
except:
	print("Failed to read settings from \'brainspeakers_settings.yml\' file. Make sure that all parameters are defined correctly. Using default values!")



### clamp values

if volumeMin > 1.0:
	volumeMin = 1.0
elif volumeMin < 0.0:
	volumeMin = 0.0

if volumeMax > 1.0:
	volumeMax = 1.0
elif volumeMax < volumeMin:
	volumeMax = volumeMin

if volumeUpdateRate > 1.0:
	volumeUpdateRate = 1.0
elif volumeUpdateRate < 0.0:
	volumeUpdateRate = 0.0

if range < 1 or range > 3:
	range = 2


### print settings

print("\n>> Settings:")
print("volume min:         {}".format(volumeMin))
print("volume max:         {}".format(volumeMax))
print("volume update rate: {}".format(volumeUpdateRate))
print("distance min:       {} mm".format(distMin))
print("distance max:       {} mm".format(distMax))
print("pg sampling rate:   {} Hz".format(samplingrate))
print("pg sample size:     {} Bits".format(bitsize))
print("pg channels:        {} Bits".format(channels))
print("pg buffer size:     {} samples".format(buffer))
print("ranging mode:       {}".format(range))
print("random play:        {}".format(randomPlay))
print("print debug info:   {}\n".format(debug))


### init pygame

volume = volumeMin

pg.mixer.pre_init(samplingrate, bitsize, channels, buffer)
pg.mixer.init(samplingrate, bitsize, channels, buffer)
pg.mixer.music.set_volume(volume)


### get audio file list

mp3s = []

for file in os.listdir("/brainspeakers/soundfiles"):
	if file.endswith(".mp3"):
		mp3s.append("/brainspeakers/soundfiles/" + file)

if len(mp3s) == 0:
	print "\n!! No MP3 files found. Exiting !!"
	raise SystemExit

print("\n>> Found {} MP3 files:".format(len(mp3s)))
print mp3s


### start ranging thread for dynamic volume

runTriggerThread = True

try:
	thread.start_new_thread( rangingThread, ("Ranging Thread", 0.07, ) )
	print "\n>> Starting ranging thread: OK"
	time.sleep(0.2)
except:
	print "\n!! Failed to start ranging thread. Exiting !!"
	raise SystemExit


### start playing audio files

print("\n>> Start playing...")


if randomPlay == 1:

	while 1:
		title = random.choice(mp3s)

		try:
       			play_music(title)
		except KeyboardInterrupt:
			print("\n>> Exiting")
			runTriggerThread = False
			pg.mixer.music.fadeout(1000)
			pg.mixer.music.stop()
			time.sleep(0.1)
			raise SystemExit
else:

	mp3Idx = 0

	while 1:
		title = mp3s[mp3Idx]
		mp3Idx = (mp3Idx + 1) % len(mp3s)

		try:
       			play_music(title)
		except KeyboardInterrupt:
			print("\n>> Exiting")
			runTriggerThread = False
			pg.mixer.music.fadeout(1000)
			pg.mixer.music.stop()
			time.sleep(0.1)
			raise SystemExit
