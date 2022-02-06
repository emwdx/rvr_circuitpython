# Write your code here :-)

import board
import busio
import time
import struct

class LEDs:
    RIGHT_HEADLIGHT = [0x00, 0x00, 0x00, 0x07]
    LEFT_HEADLIGHT = [0x00, 0x00, 0x00, 0x38]
    LEFT_STATUS = [0x00, 0x00, 0x01, 0xC0]
    RIGHT_STATUS = [0x00, 0x00, 0x0E, 0x00]
    BATTERY_DOOR_FRONT = [0x00, 0x03, 0x80, 0x00]
    BATTERY_DOOR_REAR = [0x00, 0x00, 0x70, 0x00]
    POWER_BUTTON_FRONT = [0x00, 0x1C, 0x00, 0x00]
    POWER_BUTTON_REAR = [0x00, 0xE0, 0x00, 0x00]
    LEFT_BRAKELIGHT = [0x07, 0x00, 0x00, 0x00]
    RIGHT_BRAKELIGHT = [0x38, 0x00, 0x00, 0x00]

class RawMotorModes:
    OFF = 0
    FORWARD = 1
    BACKWARD = 2

uart = busio.UART(board.D2, board.D3, baudrate=115200)
class RVRDrive:

    def __init__(self,uart = uart):
        self._uart = uart


    def drive(self,speed, heading):

        flags = 0x00
        speed = int(speed)
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

        self._uart.write(bytearray(raw_motor_data))

        return

    def setMotors(self,left,right):
        # First set the direction of each motor based on its value
        rightMode = RawMotorModes.FORWARD if (right >= 0) else RawMotorModes.BACKWARD
        leftMode = RawMotorModes.FORWARD if (left >= 0) else RawMotorModes.BACKWARD
        
        # Second convert to integers if not already
        right = int(right)
        left = int(left)
        # Third make sure motor powers are within bounds
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

    def float_to_hex(self,f):
        #return hex(struct.unpack('<I', struct.pack('<f', f))[0])
        result = bytearray(struct.pack('>f', f))

        return result

    def drive_to_position_si(self,yaw_angle, x, y, speed):
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

        #print(bytearray(output_packet))
        uart.write(bytearray(output_packet))
        return bytearray(output_packet)


    def reset_yaw(self):
        drive_data = [0x8D, 0x3E, 0x12, 0x01, 0x16, 0x06, 0x00]

        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(drive_data))

        return

    def set_streaming(self):
        
        SOP = 0x8d
        FLAGS = 0x06
        TARGET_ID = 0x02
        SOURCE_ID = 0x0b
        DEVICE_ID = 0x18
        COMMAND_ID = 0x39
        SEQ = 0x01
        EOP = 0xD8
        
        output_packet = [SOP, FLAGS, DEVICE_ID,COMMAND_ID,SEQ]
        output_packet.extend([0x03, 0x00, 0x0A, 0x02, 0x00, 0x03, 0x01])
    
        output_packet.extend([~((sum(output_packet) - SOP) % 256) & 0x00FF,EOP])

    def start_streaming(self):
    
        SOP = 0x8d
        FLAGS = 0x06
        TARGET_ID = 0x02
        SOURCE_ID = 0x0b
        DEVICE_ID = 0x18
        COMMAND_ID = 0x3A
        SEQ = 0x01
        EOP = 0xD8
        
        output_packet = [SOP, FLAGS, DEVICE_ID,COMMAND_ID,SEQ]
        output_packet.extend([0x03, 0x00, 0x0A, 0x02, 0x00, 0x03, 0x01])
    
        output_packet.extend([~((sum(output_packet) - SOP) % 256) & 0x00FF,EOP])

    def set_all_leds(self, red, green, blue):
        led_data = [
            0x8D, 0x3E, 0x11, 0x01, 0x1A, 0x1A, 0x00,
            0x3F, 0xFF, 0xFF, 0xFF
        ]
        for _ in range (10):
            led_data.extend([red, green, blue])
        led_data.extend([~((sum(led_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        self._uart.write(bytearray(led_data))
        return

    def wake(self):
        power_data = [0x8D, 0x3E, 0x11, 0x01, 0x13, 0x0D, 0x00]
        power_data.extend([~((sum(power_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        self._uart.write(bytearray(power_data))
        return

    def sleep(self):
        power_data = [0x8D, 0x3E, 0x11, 0x01, 0x13, 0x01, 0x00]
        power_data.extend([~((sum(power_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        self._uart.write(bytearray(power_data))
        return
