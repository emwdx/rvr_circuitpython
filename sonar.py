# sonar example 2022-02-17
import board
import busio
import time
import math
import digitalio

import adafruit_hcsr04
from sphero_rvr import RVRDrive

#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.IO5, echo_pin=board.IO4)   # lilygo ESP32-S2
#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.B1, echo_pin=board.B0)     # blackpill
#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP10, echo_pin=board.GP11) # RP Pico
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D11, echo_pin=board.D10)    # M4 Metro express

#rvr = RVRDrive(uart = busio.UART(board.IO1, board.IO2, baudrate=115200))    # lilygo ESP32-S2
#rvr = RVRDrive(uart = busio.UART(board.A2, board.A3, baudrate=115200))      # blackpill
#rvr = RVRDrive(uart = busio.UART(board.GP4, board.GP5, baudrate=115200))    # RP Pico
rvr = RVRDrive(uart = busio.UART(board.D1, board.D0, baudrate=115200))       # M4 Metro express

led = digitalio.DigitalInOut(board.LED) # board.LED
led.direction = digitalio.Direction.OUTPUT
while True:
    try:
        sensor_distance = sonar.distance
        print(sensor_distance)
        led.value = False
        if sensor_distance < 10 :
            rvr.set_all_leds(255,0,0)
        else:
            rvr.set_all_leds(0,255,0)
        time.sleep(0.1)
        led.value = True
        rvr.set_all_leds(0,0,0)
        time.sleep(sensor_distance / 200)

    except RuntimeError:
        print("Retrying!")
        rvr.set_all_leds(0,0,255) #set leds to blue
        pass
    time.sleep(0.2)
