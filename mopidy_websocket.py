__author__ = 'peterb'

import websocket
import json


def init_mopidy_websocket(add='ws://192.168.13.30',port=80,path="/mopidy/ws/",timeout=1):
    ws=websocket.create_connection('%s:%i%s'%(add,port,path),timeout=timeout)
    return ws


def listCommands(ws):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}')
    res=ws.recv()
    res=json.loads(res)
    print(res)
    for k in res['result']:
        #print(k,res['result'][k])
        if 'volume' in k or True:
            print(k)
            print(res['result'][k])
            print()

def getVolume(ws):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_volume"}')
    res=ws.recv()
    res=json.loads(res)
    vol=res['result']
    return vol

def setVolume(ws,vol):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.set_volume","params": [%s]}'%(vol))
    res=ws.recv()
    return res

def set_rel_volume(ws,rel_vol):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.set_rel_volume","params": [%s]}'%(rel_vol))
    res=ws.recv()
    return res

def playPiano(ws):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.set_rel_volume","params": [%s]}'%(rel_vol))
    res=ws.recv()
    return res





if __name__=='__main__':
    ws=init_mopidy_websocket()
    #ws=init_mopidy_websocket(add='ws://127.0.0.1',port=6680)
    set_rel_volume(ws,-10)
    print(getVolume(ws))
    listCommands(ws)
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.library.browse", "params":["local:"]}')
    res=ws.recv()
    print(res)
    ws.send('{"jsonrpc": "2.0", "id": 17, "method": "core.playback.get_current_track", "params":[]}')
    res=ws.recv()
    #res=json.loads(res)


    print(res)
    ws.close()

