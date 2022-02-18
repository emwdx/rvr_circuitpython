# rvr_circuitpython
This is my collection of code that I've used to run the RVR using CircuitPython.

My notes learning to use the Sphero RVR API for the Drive to Position functionality are linked here: [Link](https://drive.google.com/file/d/1oYMbidrGnvpz_ruhsh2HalU-BsVFMmpa/view?usp=sharing)

## Pin connection definition Microcontroller - RVR

We use the following standard pins to communicate with the Sphero RVR:

|                    | blackpill | rp2040 | lilygo ESP32-S2 | Metro M4 express |
|--------------------|:---------:|:------:|:---------------:|:----------------:|
| UART TX            |     A2    |   GP4  |       IO1       |        D1        |
| UART RX            |     A3    |   GP5  |       IO2       |        D0        |
| Ultrasonic trigger |     B1    |  GP10  |       IO5       |        D11       |
| Ultrasonic echo    |     B0    |  GP11  |       IO4       |        D10       |

## sphero_rvr library ##
The annotated library has the API that I've given my students to use during class. Not everything is there at this point - a work in progress.

## Big thanks! ##
* @kreier for doing testing with serial communication with RVRs and ultrasonic sensors for several boards
* @rmerriam for his original CPP code and documentation of the RVR API 
  **https://github.com/rmerriam/rvr-cpp-v2
  **https://bitbucket.org/rmerriam/rvr-cpp/wiki/browse/
