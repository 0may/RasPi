# BrainSpeakers

The code here controls the interactive installation *BRAINS* of Anna Poetter. See http://wim.adbk-nuernberg.de/pages/brains/ for more information.

The brainspeakers_app.py script reads distance measurement from a Time-of-Flight sensor and adjusts the volume of a looping audio file depending on the distance of a spectator.

Requires [Pololu's VL53L1X Time-of-Flight distance sensor](https://www.pololu.com/product/3415) and the [VL53L1X](https://github.com/pimoroni/vl53l1x-python) Python package. Also requires the *pygame* Python package for audio playing and the *yaml* Python package to read the settings file.


