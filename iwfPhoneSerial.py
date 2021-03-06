__author__ = 'peterb'

import serial
import datetime
#form mopidy_websocket import *
from mopidy_websocket import *


add='ws://192.168.13.30'
port=80


telefonBuch={9:'Toystore',
             3:'anton'}

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

def reconnect(ws):
    try:
        ws.close()
    except:
        pass
    ws=init_mopidy_websocket()
    return ws
    



serialName=get_USBPort_name()
if serialName:
    ser=initSerialPort(serialName)

#ws=init_mopidy_websocket(add,port)
ws=init_mopidy_websocket()
#print(set_rel_volume(ws,-10))
listCommands(ws,filter=True,filterName="playback")
playlists=getPlaylists(ws)


connectTime=datetime.datetime.now()


for i in range(30):
    try:
        ws.recv()
    except:
        break



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
            try:
                if dir=="+":
                    changeVol=+15
                elif dir=="-":
                    changeVol=-15
                print(set_rel_volume(ws,changeVol))
            except:
                print('split error')
        if line.split('.')[0]=='tel':
            number=line.split('.')[1]
            number=int(number)
            if number in list(telefonBuch.keys()):
                playname=telefonBuch[number]
                print(playname)
                playPlaylistName(ws,playlists,playname)
            else:
                print('no entry')

    if (datetime.datetime.now()-connectTime).total_seconds()>300:
        print('reconnect')
        ws=reconnect(ws)
        connectTime=datetime.datetime.now()
        try:
            playlists=getPlaylists(ws)
        except:
            pass
        

ser.close()

