##############################################################################
# Software License Agreement (BSD License)
#
# Copyright (c) 2019 Oliver Mayer, Academy of Fine Arts Nuremberg  
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

import os
import sys
import subprocess
import lirc
import pygame
import time
import math

#vol = 99      #volume not working...
black = True
quit = False
switchChannel = False
omxplayer = "/path/to/modified/omxplayer" # adjust path to your modified omxplayer binary

movIdx = 1
movs = ["/media/usb/ch0.mp4", "/media/usb/ch1.mp4", "/media/usb/ch2.mp4", "/media/usb/ch3.mp4", "/media/usb/ch4.mp4", "/media/usb/ch5.mp4", "/media/usb/ch6.mp4", "/media/usb/ch7.mp4", "/media/usb/ch8.mp4", "/media/usb/ch9.mp4"]
movLengths = [0 for i in range(len(movs))]

# get movie lengths in seconds
for i in range(len(movs)):
	cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', movs[i]]
	cmdstr = ""
	for word in cmd:
		cmdstr += word + " "

	if (os.system(cmdstr) == 0):
		movLengths[i] = float(subprocess.check_output(cmd))
		print("Movie {} found: Length is {} secs").format(movs[i], movLengths[i])
	else:
		print("Movie {} not found!").format(movs[i])


# init lirc
sockid = lirc.init("omxTV")

# init pygame
pygame.init()
pygame.mouse.set_visible(False)

# use pygame to show black screen when no movie is shown
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((0, 0, 0))

t0 = time.time()

while not quit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit = True
			os.system('killall omxplayer.bin')

	ret = lirc.nextcode()

	if len(ret) > 0 and not quit:

		if ret[0] == 'power':
			if black:
				switchChannel = True
			else:
				os.system('killall omxplayer.bin')
				black = True

		elif ret[0] == 'ch0':
			movIdx = 0
			switchChannel = True
		elif ret[0] == 'ch1':
			movIdx = 1
			switchChannel = True
		elif ret[0] == 'ch2':
			movIdx = 2
			switchChannel = True
		elif ret[0] == 'ch3':
			movIdx = 3
			switchChannel = True
		elif ret[0] == 'ch4':
			movIdx = 4
			switchChannel = True
		elif ret[0] == 'ch5':
			movIdx = 5
			switchChannel = True
		elif ret[0] == 'ch6':
			movIdx = 6
			switchChannel = True
		elif ret[0] == 'ch7':
			movIdx = 7
			switchChannel = True
		elif ret[0] == 'ch8':
			movIdx = 8
			switchChannel = True
		elif ret[0] == 'ch9':
			movIdx = 9
			switchChannel = True
		elif ret[0] == 'chUp':
			movIdx = (movIdx + 1) % 10;
			switchChannel = True
		elif ret[0] == 'chDown':
			if (movIdx <= 0):
				movIdx = 9
			else:
				movIdx -= 1
			switchChannel = True
#		elif ret[0] == 'volUp':
#			if vol <= 90:
#				vol += 9
#				volstr = 'amixer sset \'PCM\' {}%'.format(vol)
#				os.system(volstr)
#		elif ret[0] == 'volDown':
#			if vol >= 9:
#				vol -= 9
#				volstr = 'amixer sset \'PCM\' {}%'.format(vol)
#				os.system(volstr)


		if switchChannel:
			os.system('killall omxplayer.bin')

			if movLengths[movIdx] > 0:
				black = False

				td = time.time() - t0

				ts = td % movLengths[movIdx]
				s = int(math.floor(ts))
				m = int(math.floor(s / 60))
				h = int(math.floor(m / 60))
				s = s % 60
				m = m % 60
				tstr = '{:02d}:{:02d}:{:02d}'.format(h, m, s)

				cmd = [omxplayer, '--no-osd', '--no-keys', '-b', '--loop', '-l', tstr,  movs[movIdx]]
				omxc = subprocess.Popen(cmd)
			else:
				black = True

			switchChannel = False

	time.sleep(0.05)


pygame.quit()
lirc.deinit()
