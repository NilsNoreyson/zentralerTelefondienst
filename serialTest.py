__author__ = 'peterb'

import serial
import datetime
from pylab import *

def get_USBPort_name():
    name=None
    for i in range(200):
        try:
            ser=serial.Serial('/dev/ttyUSB%i'%i,115200,timeout=1)
            name=ser.name
            ser.close()
            break
        except:
            pass
    return name


def initSerialPort(name):
    ser=serial.Serial(name,115200,timeout=1)
    return ser


serialName=get_USBPort_name()
print(serialName)
if serialName:
    ser=initSerialPort(serialName)


dataPoints=[]

for i in range(20000):
    print(i)
    try:
        line=ser.readline()
        line=line.decode()
        line=line.strip()
    except:
        print('serial readError')
        line=""

    if line!="":
        print(line)
        dataPoints.append(int(line))
    else:
        print('no output')
ser.close()
fig,axe=subplots()
axe.plot(dataPoints)
fig.show()