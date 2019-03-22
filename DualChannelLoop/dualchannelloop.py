####################################################################
# Copyright (C) 2018 Oliver Mayer <mayer@adbk-nuernberg.de>
#
# This program is free software. It comes without any warranty, to
# to the extend permitted by applicable law. You can redistribute it
# and or modify it under the terms of the Do What The Fuck You Want
# To public license, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.
####################################################################

import pygame as pg
import time

pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

#lsound = pg.mixer.Sound('/media/usb/left.wav')
lsound = pg.mixer.Sound('/home/pi/left.wav')
lchannel = lsound.play(-1)
lchannel.set_volume(1.0, 0.0)

#rsound = pg.mixer.Sound('/media/usb/right.wav')
rsound = pg.mixer.Sound('/home/pi/right.wav')
rchannel = rsound.play(-1)
rchannel.set_volume(0.0, 1.0)

while True:
    time.sleep(3)
