# MediaLooper

The script loops video **or** audio files that are present on a USB device. Audio files must be located in `/media/usb/audioloop` and
video files in `/media/usb/videoloop`. Videos are displayed using [OMXPlayer](https://www.raspberrypi.org/documentation/raspbian/applications/omxplayer.md) and should be encoded as MP4 with H264 codec.

If you are looking for a video looper only, use [Adafruit's Video Looper](https://learn.adafruit.com/raspberry-pi-video-looper/overview). It is the most performant video looper for Raspberry Pi and starts videos really fast after a video is finished.

