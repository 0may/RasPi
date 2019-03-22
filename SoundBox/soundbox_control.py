##############################################################################
# Software License Agreement (BSD License)
#
# Copyright (c) 2017 Oliver Mayer, Academy of Fine Arts Nuremberg.
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

import RPi.GPIO as GPIO
import simpleaudio as sa


# use board numbering of GPIO pins
GPIO.setmode(GPIO.BOARD)

# pins on Raspberry Pi for button input
buttonPin1 = 11
buttonPin2 = 13
buttonPin3 = 15
buttonPin4 = 19
buttonPin5 = 21
buttonPin6 = 23

# pins on Raspberry Pi for switching buttons' LEDs
ledPin1 = 8
ledPin2 = 10
ledPin3 = 12
ledPin4 = 22
ledPin5 = 24
ledPin6 = 26

# load tracks to audio objects
track1 = sa.WaveObject.from_wave_file('/media/usb/track1.wav')
track2 = sa.WaveObject.from_wave_file('/media/usb/track2.wav')
track3 = sa.WaveObject.from_wave_file('/media/usb/track3.wav')
track4 = sa.WaveObject.from_wave_file('/media/usb/track4.wav')
track5 = sa.WaveObject.from_wave_file('/media/usb/track5.wav')
track6 = sa.WaveObject.from_wave_file('/media/usb/track6.wav')

# setup button pins with pull-up resistors 
# -> buttons connect to button pin and to GND
GPIO.setup(buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# setup LED pins
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)
GPIO.setup(ledPin3, GPIO.OUT)
GPIO.setup(ledPin4, GPIO.OUT)
GPIO.setup(ledPin5, GPIO.OUT)
GPIO.setup(ledPin6, GPIO.OUT)

# initialize LED pins to LOW = LEDs off
GPIO.output(ledPin1, GPIO.LOW)
GPIO.output(ledPin2, GPIO.LOW)
GPIO.output(ledPin3, GPIO.LOW)
GPIO.output(ledPin4, GPIO.LOW)
GPIO.output(ledPin5, GPIO.LOW)
GPIO.output(ledPin6, GPIO.LOW)


# test if button pins for going LOW
# then turn on button LED by setting its pin to HIGH.
# play corresponding track and wait until finished.
# Then turn off button LED by setting its pin to LOW.
# ... loop forever
while 1:

	if GPIO.input(buttonPin1) == GPIO.LOW:
		GPIO.output(ledPin1, GPIO.HIGH)
		play_obj = track1.play()
		play_obj.wait_done()
		GPIO.output(ledPin1, GPIO.LOW)

	elif GPIO.input(buttonPin2) == GPIO.LOW:
		GPIO.output(ledPin2, GPIO.HIGH)
		play_obj = track2.play()
		play_obj.wait_done()
		GPIO.output(ledPin2, GPIO.LOW)

	elif GPIO.input(buttonPin3) == GPIO.LOW:
		GPIO.output(ledPin3, GPIO.HIGH)
		play_obj = track3.play()
		play_obj.wait_done()
		GPIO.output(ledPin3, GPIO.LOW)

	elif GPIO.input(buttonPin4) == GPIO.LOW:
		GPIO.output(ledPin4, GPIO.HIGH)
		play_obj = track4.play()
		play_obj.wait_done()
		GPIO.output(ledPin4, GPIO.LOW)

	elif GPIO.input(buttonPin5) == GPIO.LOW:
		GPIO.output(ledPin5, GPIO.HIGH)
		play_obj = track5.play()
		play_obj.wait_done()
		GPIO.output(ledPin5, GPIO.LOW)

	elif GPIO.input(buttonPin6) == GPIO.LOW:
		GPIO.output(ledPin6, GPIO.HIGH)
		play_obj = track6.play()
		play_obj.wait_done()
		GPIO.output(ledPin6, GPIO.LOW)

	


