
import board
import busio
import time


from sphero_rvr import *


rvr = RVRDrive()
time.sleep(2.0)
rvr.drive_to_position_si(0.0,0,0.8,0.5)
time.sleep(2.0)
rvr.drive_to_position_si(90.0,1.6,0.8,0.5)
