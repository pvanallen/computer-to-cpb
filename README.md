## Communicate over Bluetooth with Circuit Playground Bluefruit, get light level
This is an example set of code that runs on a computer (tested on Mac, might work on RPI) and the CPB [Circuit Playground Bluefruit](https://www.adafruit.com/product/4333), allowing them to communicate by Bluetooth.

It will display RED on the NEOPIXELs if there is bright light, and random colors otherwise.

### Dependencies
* [cpb_receive.py](https://github.com/pvanallen/computer-to-cpb/blob/master/cpb_receive.py) tested on the CPB with
  * [Circuit Python libraries v5](https://circuitpython.org/libraries)
  * [Circuit Python v5.0.0 Beta 1](https://circuitpython.org/board/circuitplayground_bluefruit/)
* [computer_send.py](https://github.com/pvanallen/computer-to-cpb/blob/master/computer_send.py) is tested on MacOS 10.15.2 after installing
  * [Adafruit_Python_BluefruitLE](https://github.com/adafruit/Adafruit_Python_BluefruitLE)
  * Also, place the adafruit_bluefruit_connect directory from [Adafruit_CircuitPython_BluefruitConnect](https://github.com/adafruit/Adafruit_CircuitPython_BluefruitConnect), in the same directory as the .py file (also included in this repo).
