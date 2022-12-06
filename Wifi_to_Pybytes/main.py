import time
import pycom
import machine
from network import WLAN
from mqttclient import MQTTClient
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from pycoproc_1 import Pycoproc
from _pybytes import Pybytes
from _pybytes_config import PybytesConfig
from pycoproc_1 import Pycoproc

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

py = Pycoproc(Pycoproc.PYSENSE)

conf = PybytesConfig().read_config()
#Give your wifi and pass
conf['wifi']['ssid'] = 'Angela'
conf['wifi']['password'] = 'k25ag2pn'
print(conf['wifi'])
pybytes = Pybytes(conf)
print(pybytes.connect_wifi())

while True :
    alt = MPL3115A2(py,mode=ALTITUDE)
    msg = int(alt.temperature())
    dht = SI7006A20(py)
    t_ambient = 24.4
    li = LTR329ALS01(py)
    pybytes.send_signal(2,str(msg))
    print("MPL3115A2 temperature: " + str(alt.temperature()))
    time.sleep(1)
    pybytes.send_signal(3,str(li.light()))
    print("Light (channel Blue lux, channel Red lux): " + str(li.light()))
    time.sleep(1)
    pybytes.send_signal(1,dht.humid_ambient(t_ambient))
    print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(dht.humid_ambient(t_ambient)) + "%RH")
