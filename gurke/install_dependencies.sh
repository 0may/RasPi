#!/bin/sh

apt install usbmount

mkdir /etc/systemd/system/systemd-udevd.service.d

cp -v myoverride.conf /etc/systemd/system/systemd-udevd.service.d

apt install python3 python3-pip

pip3 install simpleaudio

pip3 install smbus2

pip3 install vl53l1x

