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
             0: 'Another Self Portrait',
             145:'Extrawelt'

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


def getVol():

    stat=client.status()
    vol=int(stat['volume'])
    return vol


def play_by_number(number):
    if number in list(telefonBuch.keys()):
        playname=telefonBuch[number]
        print(playname)
        try:
            playByName(playname, playlists)
        except:
            print('Starting playlis failed')

    else:
        print('no entry')


serialName=get_USBPort_name()
if serialName:
    ser=initSerialPort(serialName)




reconnect()
connectTime=datetime.datetime.now()
playByName('anton',playlists)


actionTime=False
lastAction=datetime.datetime.now()
actionTimestamp=0


LOST_ACTION_TIME=10
vol=getVol()


last_number_time=datetime.datetime.now()
dail_timeout=3
number=0
newDail=False


for k in playlists:
    print(k['playlist'])

while True:
    if not(actionTime):
        vol=getVol()
    if (datetime.datetime.now()-lastAction).total_seconds()>LOST_ACTION_TIME:
        actionTime=False
    line=ser.readline()
    line=line.decode()
    line=line.strip()
    
    if line!="":
        print(line)
        if line.split('.')[0]=='rot':
            dir=line.split('.')[1]
            actionTime=True
            lastAction=datetime.datetime.now()

            if dir=="+":
                changeVol=+5
            elif dir=="-":
                changeVol=-5
            vol=vol+changeVol
            try:
                client.setvol(vol)
            except:
                print('setting volume failed')


        if line.split('.')[0]=='tel':
            new_number=line.split('.')[1]
            new_number=int(new_number)
            last_number_time=datetime.datetime.now()
            number=number*10+new_number
            print(number)
            newDail=True


    if newDail and ((datetime.datetime.now()-last_number_time).total_seconds()>dail_timeout):
        play_by_number(number)
        number=0
        newDail=False

    if (datetime.datetime.now()-connectTime).total_seconds()>99:
        try:
            print('reconnect')
            reconnect()
            client.clearerror()
        except:
            pass
        connectTime=datetime.datetime.now()
        

ser.close()

