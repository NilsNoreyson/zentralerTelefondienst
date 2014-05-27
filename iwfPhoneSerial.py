__author__ = 'peterb'

import serial
import datetime
#form mopidy_websocket import *
from mopidy_websocket import *


mopidyAddress = 'ws://192.168.13.30'
mopidyPort = 80


Mopidy = MopidyPythonClient(mopidyAddress, mopidyPort)
Mopidy.update_playlist_dict(0)


telefonBuch={9: 'Toystore',
             3: 'anton',
             1: 'Stan',
             7: 'Kalkbrenner',
             2: 'Hit Box',
             4: 'The Katie Melua Collection',
             6: 'IRM',
             5: 'Anthems of All',
             8: 'Broken Bells',
             0: 'Another Self Portrait'

            }

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



connectTime=datetime.datetime.now()



while True:
    try:
        line=ser.readline()
        line=line.decode()
        line=line.strip()
    except:
        print('serial readError')
        line=""
    
    if line!="":
        print(line)
        if line.split('.')[0]=='rot':
            dir=line.split('.')[1]
            try:
                if dir=="+":
                    changeVol=+15
                elif dir=="-":
                    changeVol=-15
                print(Mopidy.set_rel_volume(changeVol))
            except:
                print('split error')
        if line.split('.')[0]=='tel':
            number=line.split('.')[1]
            number=int(number)
            if number in list(telefonBuch.keys()):
                playname=telefonBuch[number]
                print(playname)
                Mopidy.play_playlist_by_name(playname)
            else:
                print('no entry')

    if (datetime.datetime.now()-connectTime).total_seconds()>300:
        print('reconnect')
        Mopidy.reconnect()
        connectTime=datetime.datetime.now()
        try:
            Mopidy.update_playlist_dict()
        except:
            pass
        

ser.close()

