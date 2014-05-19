__author__ = 'peterb'

import serial
#form mopidy_websocket import *
from mopidy_websocket import *


add='ws://192.168.13.30'
port=80



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
if serialName:
    ser=initSerialPort(serialName)

#ws=init_mopidy_websocket(add,port)
ws=init_mopidy_websocket()
#print(set_rel_volume(ws,-10))
print(getVolume(ws))
print(set_rel_volume(ws,-10))


while True:
    try:
        line=ser.readline()
    except:
        print('serial readError')
        line=""
    line=str(line,encoding='utf-8')
    line=line.strip()
    if line!="":
        print(line)
        if line.split('.')[0]=='rot':
            dir=line.split('.')[1]
            if ws.connected:
                pass
            else:
                try:
                    ws.close()
                except:
                    pass
                ws=init_mopidy_websocket()


            try:
                if dir=="+":
                    changeVol=+15
                elif dir=="-":
                    changeVol=-15
                print(set_rel_volume(ws,changeVol))
            except:
                print('split error')

ser.close()

