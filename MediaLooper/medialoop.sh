#!/bin/sh

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


amixer cset numid=3 1   # set to 2 for hdmi, 0 for auto
amixer scontrols
amixer sset 'PCM' 100%
clear

LOC=""
PLAYER=""
LOOPFLAG=""

if [ -d "/media/usb/videoloop" ]
then
	LOC="/media/usb/videoloop"
	PLAYER="omxplayer --adev both"
	LOOPFLAG="--loop"
elif [ -d "/media/usb/audioloop" ]
then
	LOC="/media/usb/audioloop"
	PLAYER="mplayer"
	LOOPFLAG="--loop=0"
else
	exit 1;
fi

while [ 1 ]
do
	SIFS=$IFS
	IFS=$(echo "\n\b")
	FILES=$(find $LOC/* -maxdepth 1 -type f)
	FILECOUNT=$(echo "$FILES" | wc -l)

	if [ $FILECOUNT -eq 1 ]
	then
		CMD="$PLAYER $LOOPFLAG $(echo "$FILES" | sed -r 's/ /\\ /g')"
		eval "$CMD"
		clear
	elif [ $FILECOUNT -gt 1 ]
	then
		for file in $FILES; do
			CMD="$PLAYER $(echo "$file" | sed -r 's/ /\\ /g')"
			eval "$CMD"
			clear
		done
	fi

	IFS=$SIFS
done

