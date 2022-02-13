import board
import busio
import struct
import time

class RawMotorModes:
    OFF = 0
    FORWARD = 1
    BACKWARD = 2

uart = busio.UART(board.D2, board.D3, baudrate=115200)

class RVRDrive:
    def __init__(self):
        self._uart = uart
        self._location = [0.0,0.0,0.0]
        
    
    def drive(self,speed,heading):

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

        self._uart.write(bytearray(drive_data))

        return

    
    def stop(self):
        self.set_raw_motors(self,0,0,0,0)

        return

    @staticmethod
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
        self.set_raw_motors(self,leftMode,left,rightMode,right)

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
        uart.write(bytearray(output_packet))
        return bytearray(output_packet)


    def reset_yaw(self):
        drive_data = [0x8D, 0x3E, 0x12, 0x01, 0x16, 0x06, 0x00]

        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(drive_data))

        return

    def sensor_start(self):
        self.conf_streaming()
        time.sleep(0.2) 
        self.start_streaming()
        time.sleep(0.2) 
        
    def conf_streaming(self):

        SOP = 0x8d
        FLAGS = 0x02
        TARGET_ID = 0x02
        SOURCE_ID = 0x00
        DEVICE_ID = 0x18
        COMMAND_ID = 0x39
        SEQ = 0x01
        EOP = 0xD8

        output_packet = [SOP, FLAGS, DEVICE_ID,COMMAND_ID,SEQ]
        #output_packet = [0x8d, 0x02, 0x18,0x39,0x01]
        output_packet.extend([0x02,0x00, 0x06, 0x02,0x00,0x01,0x01])

        output_packet.extend([~((sum(output_packet) - SOP) % 256) & 0x00FF,0xD8])
        self._uart.write(bytearray(output_packet))
        #return bytearray(output_packet)

    def start_streaming(self):

        SOP = 0x8d
        FLAGS = 0x02
        TARGET_ID = 0x01
        SOURCE_ID = 0x00
        DEVICE_ID = 0x18
        COMMAND_ID = 0x3A
        SEQ = 0x02
        EOP = 0xD8

        output_packet = [SOP, FLAGS, DEVICE_ID,COMMAND_ID,SEQ]
        #output_packet = [0x8d,0x02,0x18,0x3A,0x02]
        output_packet.extend([0x00,0x0F])

        output_packet.extend([~((sum(output_packet) - SOP) % 256) & 0x00FF,0xD8])
        self._uart.write(bytearray(output_packet))
        #return bytearray(output_packet)

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


    def update_sensors(self):
        last_packet = bytearray([0,0,0,0,0])
        if uart.in_waiting != 0:
            data_read = self._uart.read(uart.in_waiting)
            index_2 = -1
            index = 0
            for index in range(len(data_read)):
                index_1 = data_read.find(b'\x8d',index)
                if index_1 != -1:
                    index_2 = data_read.find(b'\xd8',index_1)
                    if(index_2 != -1):

                        last_packet = data_read[index_1:index_2+1]
                        data_read = data_read[index_2:]
                        index = index_2
                else:
                    index += 1

            if(last_packet[4]==0x3d):
                xScaled = self._scale_uint32_sensor(struct.unpack('>I', last_packet[7:11])[0])
                yScaled = self._scale_uint32_sensor(struct.unpack('>I', last_packet[11:15])[0])
                angle = int(self._scale_angle_value(struct.unpack('>H',last_packet[19:21])[0]))
                #return (self._scale_uint16_sensor(struct.unpack('>H', last_packet[7:9])[0]),self._scale_uint16_sensor(struct.unpack('>H', last_packet[9:11])[0]),self._scale_angle_value(struct.unpack('b',last_packet[15:16])[0]))
                self._location = [xScaled,yScaled,angle]
    def _scale_uint32_sensor(self,value):
        return (value - 2147483647)/(2147483647)*16000


    def _scale_uint16_sensor(self,value):
        return (value - 65536)/(65536)*16000

    def _scale_angle_value(self,value):
        return -(-180 - 180)*(value - 32768)/(0 - 65536) 
        
    def get_x(self):
        return self._location[0]

    def get_y(self):
        return self._location[1]

    def get_heading(self):
        return self._location[2]

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

