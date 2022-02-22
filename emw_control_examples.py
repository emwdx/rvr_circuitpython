# RVR drive example 2022-02-17

import board
import busio
import time
import math

import adafruit_hcsr04
from sphero_rvr import RVRDrive

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D11, echo_pin=board.D10)    # M4 Metro express

rvr = RVRDrive(uart = busio.UART(board.D1, board.D0, baudrate=115200))       # M4 Metro express

time.sleep(0.5)

rvr.set_all_leds(255,0,0) #set leds to red
time.sleep(0.1)
rvr.set_all_leds(0,255,0) #set leds to green
time.sleep(0.1)
rvr.set_all_leds(0,0,255) #set leds to blue
time.sleep(0.1) #turn off
rvr.set_all_leds(255,255,255) #turn off leds or make them all black



print("starting up")

rvr.sensor_start()

print("sensor_start")

MAX_SPEED = 100
rvr.sensor_start()

start_time = time.monotonic()
elapsed_time = time.monotonic() - start_time

# drive to coordinates (0,1.8)
# elapsed time: 6.0 seconds

rvr.drive_to_position_si(0, 0, 1.8, 0.4)

while(elapsed_time < 6.0):
    elapsed_time = time.monotonic() - start_time
    
    time.sleep(0.1)


# drive at heading of 90 until x coordinate is 1.8
# elapsed time: 3.0 seconds
start_time = time.monotonic()
elapsed_time = time.monotonic() - start_time
rvr.update_sensors()

setpoint = 1.8
k = 150
while(elapsed_time < 8.0):
    elapsed_time = time.monotonic() - start_time
    rvr.update_sensors()
    
    current_x_coordinate = rvr.get_x()
    
    error = setpoint - current_x_coordinate
    
    output = k*error

    if(output > 100):
        output = 100
    if(output < -100):
        output = -100
    
    print(current_x_coordinate)
    rvr.drive(output,90)
    
    time.sleep(0.2)

# drive with on/off until y-coordinate is 0
# elapsed time: 3.0 seconds

setpoint = 0
rvr.drive(10,180)
time.sleep(1.0)
rvr.stop()


start_time = time.monotonic()
elapsed_time = time.monotonic() - start_time

while(elapsed_time < 4.0):
    elapsed_time = time.monotonic() - start_time
    rvr.update_sensors()
    
    current_y_coordinate = rvr.get_y()
    print(current_y_coordinate)
    if(current_y_coordinate > setpoint):
        rvr.setMotors(80,80)
    if(current_y_coordinate <= setpoint):
        rvr.setMotors(-80,-80)
    time.sleep(0.2)


rvr.stop()

