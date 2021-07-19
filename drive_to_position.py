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

import board
import busio
import time
import math
import struct


time.sleep(1.0)

uart = busio.UART(board.TX, board.RX, baudrate=115200)
def drive_to_position_si(yaw_angle, x, y, speed):
    SOP = 0x8d
    FLAGS = 0x06
    TARGET_ID = 0x0e
    SOURCE_ID = 0x0b
    DEVICE_ID = 0x16
    COMMAND_ID = 0x38
    SEQ = 0x01
    EOP = 0xD8

    yaw_angle = bytearray(struct.pack('>f', yaw_angle))
    x = bytearray(struct.pack('>f', x))
    y = bytearray(struct.pack('>f', y))
    speed = bytearray(struct.pack('>f', speed))
    flags = bytearray(struct.pack('B', 0))

    output_packet = [SOP, FLAGS, DEVICE_ID,COMMAND_ID,SEQ]
    output_packet.extend(yaw_angle)
    output_packet.extend(x)
    output_packet.extend(y)
    output_packet.extend(speed)
    output_packet.extend(flags)
    output_packet.extend([~((sum(output_packet) - SOP) % 256) & 0x00FF,EOP])

    print(bytearray(output_packet))
    return bytearray(output_packet)

SPEED = 0.6
TILE_WIDTH = 0.8
coordinates = [[0,0],[0,2],[-1,2],[-1,3],[2,3],[2,2],[0,1],[0,0],[0,0.1]]
positions = []
for pair in coordinates:
    positions.append([0.0,pair[0]*TILE_WIDTH,pair[1]*TILE_WIDTH])

for i in range(len(positions)-1):
    current_position = positions[i]
    next_position = positions[i+1]
    dx = next_position[1] - current_position[1]
    dy = next_position[2] - current_position[2]
    raw_angle = -180.0/3.1415926*math.atan2(dx,dy)

    command = drive_to_position_si(raw_angle,next_position[1],next_position[2],SPEED)
    uart.write(command)

    travel_time = math.sqrt(dx*dx + dy*dy)/SPEED*1.1 + 1.5
    print("Driving to {0},{1}, heading {2}, travel time {3}".format(next_position[1],next_position[2], raw_angle,travel_time))
    time.sleep(travel_time)
