'''
The MIT License (MIT)

Copyright (c) 2021 Evan Weinberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

# Scroll down to line 86 if you want to skip the explanation of the rest of the code.

import board
import busio
import time
import math
import struct

# Pause for a second to let the RVR boot up.
time.sleep(1.0)

# Set up the serial port on the board
uart = busio.UART(board.TX, board.RX, baudrate=115200)

# This function takes in an angle, a pair of x and y coordinates, and a speed target to use for the RVR.
def drive_to_position_si(yaw_angle, x, y, speed):

  # This sets up the list of bytes needed for this command to be sent to the RVR through the serial port.
    SOP = 0x8d. #Always the start byte for a command to the RVR
    FLAGS = 0x06 #This tells the RVR to ignore the target and source ID, and that this command expects a response only if there are errors.
    TARGET_ID = 0x0e
    SOURCE_ID = 0x0b
    
  # The drive system ID is 0x16
    DEVICE_ID = 0x16
  # The drive_to_position_si command has ID of 38
    COMMAND_ID = 0x38
    
  # The sequence value is arbitrarily 1. We aren't using the sequence capability here.
    SEQ = 0x01
    
  # The final byte in the command is 0xD8
    EOP = 0xD8

  # The command expects four float values for yaw angle, x coordinate, y coordinate, and speed. This lets you use decimal values.
  # The lines below convert the float values to a set of four bytes representing each value.
    yaw_angle = bytearray(struct.pack('>f', yaw_angle))
    x = bytearray(struct.pack('>f', x))
    y = bytearray(struct.pack('>f', y))
    speed = bytearray(struct.pack('>f', speed))
  # The command has a flags byte that lets you set different attributes for how the robot moves between the positions. Check out page 12 of the SpheroRVRControlSystem manual for the details.
    flags = bytearray(struct.pack('B', 0))
    
  # Now we build the command packet byte by byte. First the first five bytes:
    output_packet = [SOP, FLAGS, DEVICE_ID,COMMAND_ID,SEQ]
    
  # Now the bytes for the flags
    output_packet.extend(yaw_angle)
    output_packet.extend(x)
    output_packet.extend(y)
    output_packet.extend(speed)
    output_packet.extend(flags)
  # And the checksum byte which does some math with the sum of the previous bytes in the command, and finally the end of packet byte.
    output_packet.extend([~((sum(output_packet) - SOP) % 256) & 0x00FF,EOP])

  # Now that the command is complete, return the command as an array of bytes.  
    return bytearray(output_packet)

# END OF DRIVE_TO_POSITION_SI

#***************************************************************#

# This code sets up the movement of the RVR to specific positions on the floor. You can change the SPEED, TILE_WIDTH, and coordinates lines to make this work for your own list of points.

# The SPEED variable is the speed in m/s that the RVR will move. This is more accurate for lower speeds, but 0.6 works pretty well.
SPEED = 0.6

# The tiles on my floor are 80 centimeters square. You can change this to match the size of the tiles on your floor.
TILE_WIDTH = 0.8

# This list contains the coordinates that my RVR travels on the floor in units of tiles. You can change this to match your own set of tile coordinates that you want the RVR to travel to.
# From testing, this works best if the distance traveled between points is at least 50 centimeters or so.
COORDINATES = [[0,0],[0,2],[-1,2],[-1,3],[2,3],[2,2],[0,1],[0,0],[0,0.1]]

# You can leave the code below as it is and it should work. I've added some comments to explain it as well.

# The for-loop below turns the tile coordinates into real world positions in meters.
positions = []
for pair in COORDINATES
    positions.append([0.0,pair[0]*TILE_WIDTH,pair[1]*TILE_WIDTH])

# This for-loop iterates over the pairs of points in the list
for i in range(len(positions)-1):
    current_position = positions[i]
    next_position = positions[i+1]
    dx = next_position[1] - current_position[1]
    dy = next_position[2] - current_position[2]
    
    # This calculates a heading for the movement about to occur.
    raw_angle = -180.0/3.1415926*math.atan2(dx,dy)
    
    # This line 
    command = drive_to_position_si(raw_angle,next_position[1],next_position[2],SPEED)
    uart.write(command)
    
    # This waits for the command to complete based on the distance to the next point, along with some helpful fudge factors.
    travel_time = math.sqrt(dx*dx + dy*dy)/SPEED*1.1 + 1.5
    
    #This print statement is for debugging purposes.
    print("Driving to {0},{1}, heading {2}, travel time {3}".format(next_position[1],next_position[2], raw_angle,travel_time))
    time.sleep(travel_time)
