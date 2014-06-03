__author__ = 'peterb'

import serial
import datetime
from mpd import MPDClient

mopidyAddress = '192.168.13.13'
mopidyPort = 6600

client=MPDClient()
playlists={}

def reconnect():
    global client
    global playlists
    try:
        client.disconnect()
    except:
        pass
    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    client.password('IlPits2013')
    playlists=client.listplaylists()

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
def getFilteredPlaylists(playlists,filterName):
    fPlaylists=[]
    for p in playlists:
        if filterName in p['playlist']:
            fPlaylists.append(p)
            print(p['playlist'])
    return fPlaylists

def playByName(name, playlists):
    client.clear()
    fPlaylists=getFilteredPlaylists(playlists,name)
    for p in fPlaylists:
        client.load(p['playlist'])
    client.play()


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




reconnect()
connectTime=datetime.datetime.now()
playByName('anton',playlists)


while True:
    line=ser.readline()
    line=line.decode()
    line=line.strip()
    
    if line!="":
        print(line)
        if line.split('.')[0]=='rot':
            dir=line.split('.')[1]
            try:
                if dir=="+":
                    changeVol=+5
                elif dir=="-":
                    changeVol=-5

                stat=client.status()
                vol=int(stat['volume'])

                try:
                    client.setvol(vol+changeVol)
                except:
                    print('setting volume failed')
            except:
                print('split error')
        if line.split('.')[0]=='tel':
            number=line.split('.')[1]
            number=int(number)
            if number in list(telefonBuch.keys()):
                playname=telefonBuch[number]
                print(playname)
                try:
                    playByName(playname, playlists)
                except:
                    print('Starting playlis failed')

            else:
                print('no entry')

    if (datetime.datetime.now()-connectTime).total_seconds()>30:
        try:
            print('reconnect')
            reconnect()
            client.clearerror()
        except:
            pass
        connectTime=datetime.datetime.now()
        

ser.close()

