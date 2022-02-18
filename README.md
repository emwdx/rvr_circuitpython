# rvr_circuitpython
This is a collection of code that can be used to run the RVR using CircuitPython.

My notes learning to use the Sphero RVR API for the Drive to Position functionality are linked here: [Link](https://drive.google.com/file/d/1oYMbidrGnvpz_ruhsh2HalU-BsVFMmpa/view?usp=sharing)

## Pin connection definition Microcontroller - RVR

We use the following standard pins to communicate with the Sphero RVR with a HCSR04 Ultrasonic Sensor attached to the front:

|                    | blackpill | rp2040 | lilygo ESP32-S2 | Metro M4 express | Metro M0 express**
|--------------------|:---------:|:------:|:---------------:|:----------------:|:----------------:|
| UART TX            |     A2    |   GP4  |       IO1       |        D1        |        D2        |
| UART RX            |     A3    |   GP5  |       IO2       |        D0        |        D3        |
| Ultrasonic trigger |     B1    |  GP10  |       IO5       |        D11       |        D11       |
| Ultrasonic echo    |     B0    |  GP11  |       IO4       |        D10       |        D10       |

**Note: The Metro M0 express does not have enough memory to run both the sphero_rvr library and the imported adafruit_hcsr04 library

## sphero_rvr.py library ##
The annotated library has the API that I've given my students to use during class. Not everything is there at this point - a work in progress.

The .mpy file is the compiled version of the library for [Circuitpython 7.1.1](https://circuitpython.org). 

## Big thanks! ##
* [@kreier](https://github.com/kreier/) for doing testing with serial communication with RVRs and ultrasonic sensors for several boards
* [@rmerriam](https://github.com/rmerriam) for his original CPP code and documentation of the RVR API 
  * [Sphero RVR Wiki reference](https://bitbucket.org/rmerriam/rvr-cpp/wiki/browse/)
  * [Github repository for C++ API] (https://github.com/rmerriam/rvr-cpp-v2)[https://github.com/rmerriam/rvr-cpp-v2]
  
