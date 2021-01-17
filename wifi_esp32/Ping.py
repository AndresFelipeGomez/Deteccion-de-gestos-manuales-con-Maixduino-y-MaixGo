import network
import utime
from Maix import GPIO
from fpioa_manager import *

#iomap at MaixDuino
fm.register(25,fm.fpioa.GPIOHS10)#cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#mosi
fm.register(26,fm.fpioa.GPIOHS14)#miso
fm.register(27,fm.fpioa.GPIOHS15)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12,
mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)
SSID = "GOMEZ"
PASW = "1102381153"
nic.connect("GOMEZ", "1102381153")

if nic.isconnected() == False:
    for i in range(5):
        try:
            nic.reset()
            print('try AT connect wifi...')
            nic.connect(SSID, PASW)
            if nic.isconnected():
                break
        except Exception as e:
            print(e)
print('network state:', nic.isconnected(), nic.ifconfig())

print("ping uis.edu.co:", nic.ping("uis.edu.co"), "ms")
nic.disconnect()
