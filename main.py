
import board
import busio
import time


from sphero_rvr import *


rvr = RVRDrive()
time.sleep(2.0)
rvr.drive_to_position_si(0.0,0.05,0.0,0.0)
time.sleep(2.0)
rvr.drive_to_position_si(90.0,0.0,0.0,0.0)
