# omxTV

Emulates a TV with 10 channels provided by video files on an USB storage device. Channels are switched using a remote control and [LIRC](http://www.lirc.org/) and an IR receiver like the [TSOP4838](https://www.conrad.de/de/ir-empfaenger-sonderform-axial-bedrahtet-38-khz-950-nm-vishay-tsop4838-171115.html).

## Hooking up the IR receiver with Raspberry Pi

The OUT pin of the IR receiver goes to GPIO pin 18 on the Raspberry Pi. VCC goes to 3.3V (GPIO pin 1) and GND to GPIO pin 6.

## Setting up LIRC on a Raspberry Pi 3

The following steps are taken from https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b

Install LIRC by typing on the commandline
```
$ sudo apt-get update
$ sudo apt-get install lirc
```

Add the following lines to `/etc/modules` file
```
lirc_dev
lirc_rpi gpio_in_pin=18 gpio_out_pin=17
```

Add the following lines to `/etc/lirc/hardware.conf` file
```
LIRCD_ARGS="--uinput --listen"
LOAD_MODULES=true
DRIVER="default"
DEVICE="/dev/lirc0"
MODULES="lirc_rpi"
```

Update the following line in `/boot/config.txt`
```
dtoverlay=lirc-rpi,gpio_in_pin=18,gpio_out_pin=17
```

Update the following lines in /etc/lirc/lirc_options.conf
```
driver    = default
device    = /dev/lirc0
```
Restart LIRC service by typing on the commandline
```
$ sudo /etc/init.d/lircd stop
$ sudo /etc/init.d/lircd start
```

Check status to see if LIRC is running
```
$ sudo /etc/init.d/lircd status
```

Reboot before testing
```
$ reboot
```

To test if lirc driver is working
```
$ sudo /etc/init.d/lircd stop
$ mode2 -d /dev/lirc0
```
Then you should see output like below
```
<press a key in remote and you should see multple lines like below>
pulse 560
space 1706
pulse 535
```
Stop the LIRC service and record a custom remote/register a remote device
```
$ sudo /etc/init.d/lircd stop
$ sudo irrecord -d /dev/lirc0 ~/lircd.conf
```
Follow the instruction prompted by the above command carefully.
At the end ~/lircd.conf file will be generated. Make sure to record the number keys as KEY_0, KEY_1, ... KEY_9 as well as keys KEY_CHANNELUP, KEY_CHANNELDOWN, KEY_POWER, KEY_VOLUMEUP and KEY_VOLUMEDOWN.

Backup the original lircd.conf and copy new one to lirc directory, then restart LIRC service.
```
$ sudo mv /etc/lirc/lircd.conf /etc/lirc/lircd_original.conf
$ sudo cp ~/lircd.conf /etc/lirc/lircd.conf
$ sudo /etc/init.d/lircd start
```

you can test if the recorded remote works by running
```
$ irw
```
and watch output when keys on the remote control are pressed.

## Setting up LIRC for omxTV

When everything works fine, copy the file *lircrc* to the directory `/etc/lirc/`. This file specifies the messages that are sent to omxTV when buttons on the remote are pressed.

## Preparing the USB storage device

omxTV requires video files in `/media/usb` with names *ch0.mp4*, *ch1.mp4*, ... for channels 0 to 9. The video format should be MP4 with H264 codec. Use e.g. the *usbmount* utility to automount to `/media/usb`.

## Modifying OMXPlayer

omxTV uses a modified version of [OMXPlayer](https://github.com/popcornmix/omxplayer/), because it starts the video files at a position depending on the running time of the program to emulate the continuous behaviour of TV broadcast. The standard OMXPlayer always loops from the specified starting position in the video, while omxTV need a video to start from the beginning when the video file ends. Therefore, you need to change a line of code and build the player from scratch.

To modify OMXPlayer, download the repository at https://github.com/popcornmix/omxplayer/ follow the instructions for building on a Raspberry Pi **without installing** to keep the original OMXPlayer of the system if present. When the built is successful, open `omxplayer.cpp` and change the line `m_loop_from = m_incr;` to `m_loop_from = m_incr;` (currently line 759). If line number has changed, look for the code block below, where the line is already changed:
```
case 'l':
  {
    if(strchr(optarg, ':'))
    {
      unsigned int h, m, s;
      if(sscanf(optarg, "%u:%u:%u", &h, &m, &s) == 3)
        m_incr = h*3600 + m*60 + s;
    }
    else
    {
      m_incr = atof(optarg);
    }
    if(m_loop)
      m_loop_from = 0; //m_incr;
  }
  break;
```
## Preparing for omxTV

At last, adjust the path of the modified OMXPlayer in the `omxTV.py` script, usually `pathofthedownloadedcode/omxplayer-dist/usr/bin/omxplayer`.

Install required Python packages with Python's package installer
```
$ pip install python-lirc pygame
```

Now run omxTV by typing
```
$ python omxTV.py
```
