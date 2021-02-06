
import board
import busio
import time


from sphero_rvr import *


rvr = RVRDrive()

rvr.drive_to_position_si(0.0,0.5,1.0,100)
