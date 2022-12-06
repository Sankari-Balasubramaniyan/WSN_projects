
import time
import pycom
from pycoproc_1 import Pycoproc
import machine
import math
from LIS2HH12 import LIS2HH12 #Accelerometer sensor
from network import Bluetooth
from machine import Timer

pycom.heartbeat(False)
pycom.rgbled(0xFF000)

py = Pycoproc(Pycoproc.PYSENSE)
pybytes_enabled = False
update = False

def conn_cb(chr):
    events = chr.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print('client connected')
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print('client disconnected')
        update = False

#Adding accelerometer data
li = LIS2HH12(py)
#Starting points as reference points
i_x, i_y, i_z = li.acceleration()
current_direc = "Nothing"

while(True):
    #Current values
    x = 0
    x,y,z = li.acceleration()
    x = round(x,2)
    print("Change in orientation : ", x)

    #Code based on ludo logic
    if(x > 0.9):
        print("Right",x)
        pycom.rgbled(0x7f7f00) # yellow
        x,y,z = li.acceleration()
        x = round(x,2)
        time.sleep(0.5)
    elif(x < -0.9):
        print("Left",x)
        pycom.rgbled(0x7f0000) # red
        x,y,z = li.acceleration()
        x = round(x,2)
        time.sleep(0.5)
    else:
        print("Nothing")
        # pycom.rgbled(0xff00) #Green
        x,y,z = li.acceleration()
        x = round(x,2)
        time.sleep(0.5)

if(pybytes_enabled):
    pybytes.send_signal(1, li.acceleration())
    print("Send data to pybytes")

time.sleep(5)
bluetooth = Bluetooth()
bluetooth.set_advertisement(name="FiPy", manufacturer_data="Pycom")
bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)
