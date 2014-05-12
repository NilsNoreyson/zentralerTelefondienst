# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/peterb/.spyder2/.temp.py
"""
import numpy as np
import serial
import alsaaudio
import websocket
import json

volFactor=0.1

m=alsaaudio.Mixer()

ws=websocket.create_connection('ws://192.168.13.30:80/mopidy/ws/',timeout=1)

#ser=serial.Serial('/dev/ttyUSB0',115200,timeout=1)
ser=serial.Serial('/dev/ttyUSB1',115200,timeout=1)
volArray=[]
volume=1
volV=0


#ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}')

class Mopidy():
    def __init__(self,ws):
        self.ws=ws
        self.vol=0
    def listFunction(self):
        ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}')
        res=ws.recv()
        res=json.loads(res)
        print(res.keys())
        print(res['result'])
        for k in res['result'].keys():
            print(k,res['result'][k])
    def setVolume(self,vol):
        ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.set_volume","params": [%s]}'%vol)
        #core.playback.set_volume {'params': [{'name': 'volume'}], 'description': None}
        res=ws.recv()
        res=json.loads(res)
        print(res)
    def getVolume(self):
        ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_volume"}')
        res=ws.recv()
        res=json.loads(res)
        try:
            print(int(res['result']))
        except:
            print(res)


#m=Mopidy(ws)
#m.listFunction()
#m.getVolume()


while True:
    line=ser.readline()
    line=str(line,'utf-8')
    #print(str(vol.strip()))
    string=str(line.strip())
    string=string.strip("'")
    string=string.split('.')
    print(string)
    #m.setVolume(int(np.round(volume)))
    #m.getVolume()



