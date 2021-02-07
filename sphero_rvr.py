import board
import busio
import time
import struct

uart = busio.UART(board.D2, board.D3, baudrate=115200)

class RawMotorModes:
    OFF = 0
    FORWARD = 1
    BACKWARD = 2

class RVRDrive:

    def __init__(self,uart = uart):
        self._uart = uart


    def drive(self,speed, heading):

        flags = 0x00

        if speed < 0:
            speed *= -1
            heading += 180
            heading %= 360
            flags = 0x01

        drive_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x07, 0x00,
            speed, heading >> 8, heading & 0xFF, flags
        ]

        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self.uart.write(bytearray(drive_data))

        return

    @staticmethod
    def stop(heading):
        RVRDrive.drive(0, heading)

        return


    def set_raw_motors(self,left_mode, left_speed, right_mode, right_speed):
        if left_mode < 0 or left_mode > 2:
            left_mode = 0

        if right_mode < 0 or right_mode > 2:
            right_mode = 0

        raw_motor_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x01, 0x00,
            left_mode, left_speed, right_mode, right_speed
        ]

        raw_motor_data.extend([~((sum(raw_motor_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self.uart.write(bytearray(raw_motor_data))

        return

    def float_to_hex(self,f):
        #return hex(struct.unpack('<I', struct.pack('<f', f))[0])
        result = bytearray(struct.pack('f', f))

        return result

    def drive_to_position_si(self, heading,x, y, speed):
        raw_motor_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x38, 0x00,0x00]

        bytesHeading = self.float_to_hex(heading)
        bytesX = self.float_to_hex(x)
        bytesY = self.float_to_hex(y)
        bytesSpeed = self.float_to_hex(speed)
        header = bytearray(raw_motor_data)
        header.extend(bytesHeading)
        header.extend(bytesX)
        header.extend(bytesY)
        header.extend(bytesSpeed)

        flags = bytearray(0x00)
        header.extend(flags)
        ending = bytearray([~((sum(header) - 0x8D) % 256) & 0x00FF, 0xD8])
        header.extend(ending)
        #raw_motor_data.extend([~((sum(raw_motor_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        #print(header)
        self._uart.write(header)
        response = bytearray(10)
        self._uart.readinto(response)
        print(response)

    def setMotors(self,left,right):
        # First set the direction of each motor based on its value
        rightMode = RawMotorModes.FORWARD if (right >= 0) else RawMotorModes.BACKWARD
        leftMode = RawMotorModes.FORWARD if (left >= 0) else RawMotorModes.BACKWARD

        # Second make sure motor powers are within bounds
        if(left > 255):
            left = 255
        if(left < -255):
            left = -255
        if(right > 255):
            right = 255
        if(right < -255):
            right = -255

        # Third adjust the speed value to always be positive
        if(left < 0):
            left = -left
        if(right < 0):
            right = - right

        # Call raw motor function
        self.set_raw_motors(leftMode,left,rightMode,right)

    @staticmethod
    def reset_yaw():
        drive_data = [0x8D, 0x3E, 0x12, 0x01, 0x16, 0x06, 0x00]

        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self.uart.write(bytearray(drive_data))

        return
