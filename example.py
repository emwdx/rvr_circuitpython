# RVR drive example 2022-02-17

import board
import busio
import time
import math

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

time.sleep(0.5)

rvr.set_all_leds(255,0,0) #set leds to red
time.sleep(0.1)
rvr.set_all_leds(0,255,0) #set leds to green
time.sleep(0.1)
rvr.set_all_leds(0,0,255) #set leds to blue
time.sleep(0.1) #turn off
rvr.set_all_leds(255,255,255) #turn off leds or make them all black

rvr.sensor_start()

print("starting up")
setpoint = 100.0
k = 5
MAX_SPEED = 100

rvr.update_sensors()

error = 100
start_time = time.monotonic()
elapsed_time = time.monotonic() - start_time

#on off control
while(elapsed_time < 3.0):
    elapsed_time = time.monotonic() - start_time
    try:
        sensor_distance = sonar.distance

        # Add your proportional control code here.
        error = sensor_distance - setpoint

        if(error > 0):
            output = 80
            rvr.set_all_leds(0,255,0) #set leds to green
        elif(error < 0):
            output = -80
            rvr.set_all_leds(255,0,0) #set leds to red

        rvr.setMotors(output, output) #set the power of the motors for both the left and right track
            # Read the Sphero RVR library file to find the rvr.setMotors(left,right) command.
            # Use this command in the next line to send the output of your proportional
            # control to both the left and right motors.

    except RuntimeError:
        print("Retrying!")
        pass
    time.sleep(0.2)


# Drive for two seconds at a heading of 90 degrees
rvr.drive(30,90)
rvr.set_all_leds(0,0,255) #set leds to blue
time.sleep(2.0)
rvr.stop()

# Drive back to the starting point
rvr.drive_to_position_si(0,0,0,0.4)
rvr.set_all_leds(0,255,0)
time.sleep(3.0)
rvr.set_all_leds(255,255,255)
