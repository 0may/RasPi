#!/bin/sh

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

