
import board
import busio
import time


from sphero_rvr import *


rvr = RVRDrive()
rvr.wake()
rvr.reset_yaw()
rvr.set_all_leds(255,0,0)
time.sleep(5.0)
rvr.drive_to_position_si(0.0,0.0,0.8,0.5)
rvr.set_all_leds(0,255,0)
time.sleep(5.0)
rvr.drive_to_position_si(90.0,1.6,0.8,0.5)
rvr.set_all_leds(0,0,255)
time.sleep(5.0)
rvr.set_all_leds(255,0,255)
