__author__ = 'peterb'

import websocket
import json
import time
import datetime

class MopidyPythonClient:


    def __init__(self, add='ws://192.168.13.30', port=80, path="/mopidy/ws/", timeout=10):
        """

        :param add: Address of the mopidy server
        :param port:
        :param path: Path to the ws
        :param timeout:
        """
        self.address = add
        self.port = port
        self.path = path
        self.timeout = timeout
        self.ws = self.init_mopidy_websocket()
        self.playlist_dict = {}

    def init_mopidy_websocket(self):
        ws = websocket.create_connection('%s:%i%s' % (self.address, self.port, self.path), timeout=self.timeout)
        return ws

    def reconnect(self):
        self.ws.close()
        self.ws = self.init_mopidy_websocket()

    def send_method(self, method, params=None):

        json_rpc={}

        json_rpc["jsonrpc"] = "2.0"
        json_rpc["id"] = method
        json_rpc["method"]=method
        if params:
            json_rpc["params"]=params
        send_str = json.dumps(json_rpc)
        print(send_str)
        self.ws.send(send_str)

    def read_response(self,id=None):
        start_time = time.time()
        while (time.time()-start_time)<10:
            res = self.ws.recv()
            res = json.loads(res)
            if ('id' in res) and id:
                if res['id'] == id:
                    return res
                else:
                    pass
            elif 'id' in res:
                return res

            else:
                pass

        raise("No response from mopidy")

    def write_read_json_rpc(self,method, params=None):
        self.send_method(method, params)
        return self.read_response(id=method)


    def list_commands(self, use_filter=False, filter_name=""):
        """


        :rtype : object
        :param use_filter: Filter the commands by the argument
        :param filter_name: The name to look for
        :return: return the mopidy websocket response
        """
        method="core.describe"

        res=self.write_read_json_rpc(method, params=None)


        for k in res['result']:
            #print(k,res['result'][k])
            if filter_name in k or not use_filter:
                print(k)
                print(res['result'][k])
                print()
        return res


    def get_volume(self):
        method="core.playback.get_volume"
        params=None
        res=self.write_read_json_rpc(method, params)
        vol = res['result']
        return vol

    def set_volume(self, vol):

        method="core.playback.set_volume"
        params=[vol]
        res=self.write_read_json_rpc(method, params)
        return res

    def set_rel_volume(self, rel_vol):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.set_rel_volume","params": [%s]}' % rel_vol)
        res = self.ws.recv()
        return res

    def get_playlists_from_mopidy(self, wait_for_response=8):
        """
        The function reads the available playlists at the conneczted mopidy server and packs them by name in a dict

        :return: A dictionary with the names as keys and the mopidy playlist object as value
        """

        playlists_dict = {}

        method="core.playlists.get_playlists"
        params=["True"]
        res=self.write_read_json_rpc(method, params)

        playlists = res['result']
        for i, playlist in enumerate(playlists):
            name = playlist['name']
            playlists_dict[name] = playlist
            #print(i,name)
            #print(i,name.encode('utf-8','ignore'))
        return playlists_dict

    def update_playlist_dict(self,wait_for_seconds=8):
        self.playlist_dict = self.get_playlists_from_mopidy(wait_for_response=wait_for_seconds)
        return None

    def add_playlist_to_tracklist(self, playlist_object):
        tracks = playlist_object['tracks']
        tracks = json.dumps(tracks)
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add","params": [%s]}' % tracks)
        res = self.ws.recv()
        #print(res)

    def clear_tracklist(self):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear","params": []}')
        res = self.ws.recv()
        print(res)

    def play_tracklist(self):
        self.ws.send('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.play","params": []}')
        res = self.ws.recv()
        #print(res)

    def get_filtered_playlists_names(self, name):
        filtered_playlist_names = [p for p in list(self.playlist_dict.keys()) if (name in p)]
        return filtered_playlist_names

    def play_playlist_by_name(self, name):
        self.clear_tracklist()
        playlist_namelist = self.get_filtered_playlists_names(name)
        for playlist_name in playlist_namelist:
            #print(playlist_name)
            playlist_object = self.playlist_dict[playlist_name]
            self.add_playlist_to_tracklist(playlist_object)
        self.play_tracklist()


if __name__ == '__main__':
    mopidyAddress = 'ws://192.168.13.30'
    mopidyPort = 80
    #add='ws://127.0.0.1'
    #port=6680

    Mopidy = MopidyPythonClient(mopidyAddress, mopidyPort)
    # Mopidy.list_commands()
    Mopidy.update_playlist_dict(0)
    Mopidy.play_playlist_by_name("Stan")
    Mopidy.reconnect()
    time.sleep(3)
    Mopidy.play_playlist_by_name("Stan")
    # ws.close()
    #

