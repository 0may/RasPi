# RasPi
Raspberry Pi apps

This repository hosts the code of small Raspberry Pi projects.

## Mounting USB devices with *usbmount*

Many projects here require data on a USB device for changing the content of mostly media files in the most simple way. A convenient utility is *usbmount*. It mounts a USB device automatically to `/media/usb`. Type
```
sudo apt-get install usbmount
```
on the commandline to install.

#### Fix for Raspbian Stretch

On Raspbian Stretch, you need to fix an issue with filesystem namespaces:

Create a directory and file `/etc/systemd/system/systemd-udevd.service.d/myoverride.conf` and edit the content of the file to contain
```
[Service]
MountFlags=shared
```
Then restart the systemd-udevd service by typing
```
sudo service systemd-udevd restart
```
on the commandline.

The original post of this fix can be found here:

https://unix.stackexchange.com/questions/330094/udev-rule-to-mount-disk-does-not-work/330156#330156
