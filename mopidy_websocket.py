__author__ = 'peterb'

import websocket
import json
import time

def init_mopidy_websocket(add='ws://192.168.13.30',port=80,path="/mopidy/ws/",timeout=1):
    ws=websocket.create_connection('%s:%i%s'%(add,port,path),timeout=timeout)
    return ws

def listCommands(ws,filter=False,filterName=""):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}')
    res=ws.recv()
    res=json.loads(res)
    #print(res.encode('utf-8',ignore=True))
    for k in res['result']:
        #print(k,res['result'][k])
        if filterName in k or not(filter):
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

def getPlaylists(ws):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playlists.get_playlists","params": ["True"]}')
    playlistDict={}
    time.sleep(8)
    res=ws.recv()
    res=json.loads(res)
#    print(res.encode('utf-8',ignore=True))
    playlists=res['result']
    for i,playlist in enumerate(playlists):
        name=playlist['name']
        playlistDict[name]=playlist
        #print(i,name.encode('ascii','ignore'))
    return playlistDict



def addPlaylist(ws,playlist):
    tracks=playlist['tracks']
    tracks=json.dumps(tracks)
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add","params": [%s]}'%tracks)
    res=ws.recv()
    #print(res)

def clearTracklist(ws):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear","params": []}')
    res=ws.recv()
    #print(res)

def clearTracklist(ws):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear","params": []}')
    res=ws.recv()
    #print(res)

def playTracklist(ws):
    ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.play","params": []}')
    res=ws.recv()
    #print(res)

def filterPlaylists(playlists,name):
    filteredPlaylistNames=[p for p in list(playlists.keys()) if (name in p)]
    return filteredPlaylistNames

def playPlaylistName(ws,playlists,name):
    clearTracklist(ws)
    nameLists=filterPlaylists(playlists,name)
    for playlistName in nameLists:
        #print(playlistName)
        playlist=playlists[playlistName]
        addPlaylist(ws,playlist)
    playTracklist(ws)


if __name__=='__main__':
    ws=init_mopidy_websocket()
    #ws=init_mopidy_websocket(add='ws://127.0.0.1',port=6680)
    #set_rel_volume(ws,-10)
    #print(getVolume(ws))
    listCommands(ws,filter=True,filterName="playlist")
    listCommands(ws,filter=True,filterName="track")
    listCommands(ws,filter=True,filterName="playback")

    #ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_current_track", "params":[]}')
    #res=ws.recv()
    #print(res)

    name='anton'
    playlists=getPlaylists(ws)
    #print(list(playlists.keys()))
    playPlaylistName(ws,playlists,name)

    ws.close()

