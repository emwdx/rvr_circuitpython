import board
import busio
import time
from struct import *

spi = busio.SPI(board.SCK, MOSI = board.MOSI,MISO=board.MISO)


from adafruit_bus_device.spi_device import SPIDevice
device = SPIDevice(spi, baudrate=2000000, polarity=0, phase=0)

while not spi.try_lock():
    pass

class Pixy:
    def __init__(self):
        self.link = device
        self.blocks = []
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.blockFound = False

    def set_lamp(self,on):
        self.link.spi.write(bytes([174, 193, 22, 2, 1 if on else 0, 0]))

    def set_led(self,red,green,blue):
        self.link.spi.write(bytes([174, 193, 20, 3,red, green, blue]))



    def set_servo(self,s1,s2):
        servo1 = pack('<H',s1)
        servo2 = pack('<H',s2)

        self.link.spi.write(bytes([174, 193, 18,4]))
        self.link.spi.write(servo1)
        self.link.spi.write(servo2)


    def get_blocks(self,sigmap,maxblocks):
        self.link.spi.write(bytes([174, 193, 32, 2,sigmap,maxblocks]))
        result = bytearray(25)
        self.link.spi.readinto(result)

        dataB = unpack('BBBBBBB',result[4:11])
        dataL = unpack('<HHHHHH',result[11:23])

        if(dataB[6] == 14):
            self.x = dataL[2]
            self.y = dataL[3]
            self.width = dataL[4]
            self.height = dataL[5]
            self.blockFound = True

        else:
            self.x = None
            self.y = None
            self.width = None
            self.height = None
            self.blockFound = False

    def getVersion(self):
        self.link.spi.write(bytes([174, 193, 14,0]))
        result = bytearray(13)
        self.link.spi.readinto(result)
        data = unpack('bbb',result[4:7])
        return data