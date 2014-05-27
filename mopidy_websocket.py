__author__ = 'peterb'

import websocket
import json
import time



class MopidyPythonClient:

    def __init__(self,add='ws://192.168.13.30',port=80,path="/mopidy/ws/",timeout=1):
        self.address = add
        self.port = port
        self.path = path
        self.timeout = timeout
        self.ws =self.init_mopidy_websocket()

    def init_mopidy_websocket(self):
        ws=websocket.create_connection('%s:%i%s'%(self.address,self.port,self.path),timeout=self.timeout)
        return ws

    def list_commands(self,filter=False,filterName=""):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}')
        res = self.ws.recv()
        res = json.loads(res)
        #print(res.encode('utf-8',ignore=True))
        for k in res['result']:
            #print(k,res['result'][k])
            if filterName in k or not(filter):
                print(k)
                print(res['result'][k])
                print()
        return res



    def getVolume(self):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_volume"}')
        res=self.ws.recv()
        res=json.loads(res)
        vol=res['result']
        return vol

    def setVolume(self,vol):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.set_volume","params": [%s]}'%(vol))
        res=self.ws.recv()
        return res

    def set_rel_volume(self,rel_vol):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.set_rel_volume","params": [%s]}'%(rel_vol))
        res=self.ws.recv()
        return res

    def getPlaylists(self):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playlists.get_playlists","params": ["True"]}')
        playlistDict={}
        time.sleep(8)
        res=self.ws.recv()
        res=json.loads(res)
    #    print(res.encode('utf-8',ignore=True))
        playlists=res['result']
        for i,playlist in enumerate(playlists):
            name=playlist['name']
            playlistDict[name]=playlist
            #print(i,name.encode('ascii','ignore'))
        return playlistDict

    def update_playlistdict(self):
        self.playlist_dict=getPlaylists(self)
        return None

    def add_playlist_to_tracklist(self,playlist_object):
        tracks=playlist_object['tracks']
        tracks=json.dumps(tracks)
        ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add","params": [%s]}'%tracks)
        res=self.ws.recv()
        #print(res)

    def clear_tracklist(self):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear","params": []}')
        res=self.ws.recv()


    def play_tracklist(self):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.play","params": []}')
        res=self.ws.recv()
        #print(res)

    def get_filtered_playlists_names(self,name):
        filteredPlaylistNames=[p for p in list(self.playlist_dict.keys()) if (name in p)]
        return filteredPlaylistNames

    def play_playlist_by_name(self,name):
        self.clear_tracklist()
        playlist_namelist=self.get_filtered_playlists_names(name)
        for playlist_name in playlist_namelist:
            print(playlistName)
            playlist_object=self.playlist_dict[playlist_name]
            self.add_playlist_to_tracklist(playlist_object)
        self.play_tracklist(ws)


if __name__=='__main__':
    #add='ws://192.168.13.30'
    add='ws://127.0.0.1'
    port=6680
    Mopidy=MopidyPythonClient(add,port)
    Mopidy.list_commands()
    #ws=init_mopidy_websocket(add='ws://127.0.0.1',port=6680)
    #set_rel_volume(ws,-10)
    #print(getVolume(ws))
    # listCommands(ws,filter=True,filterName="playlist")
    # listCommands(ws,filter=True,filterName="track")
    # listCommands(ws,filter=True,filterName="playback")
    #
    # #ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_current_track", "params":[]}')
    # #res=ws.recv()
    # #print(res)
    #
    # name='anton'
    # playlists=getPlaylists(ws)
    # #print(list(playlists.keys()))
    # playPlaylistName(ws,playlists,name)
    #
    # ws.close()
    #
