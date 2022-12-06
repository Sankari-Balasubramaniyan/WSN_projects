import time
import pycom
import machine
from network import WLAN
from mqtt import MQTTClient

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from pycoproc_1 import Pycoproc

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

def sub_cb(topic, msg):
    #print("Received" + str(msg))
    #alt = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    #press = MPL3115A2(py,mode=PRESSURE)
    #li = LTR329ALS01(py)
    #msg1 = int(alt.temperature())
    #msg2 = press.pressure()
        # msg3 = int(li.light())
    #if(topic == "Angelaaa/feeds/temperature"):
    print("pressure" + str(msg))
    # print("Altitude: " + str(alt.altitude()))
    # client.publish(topic="Angelaaa/feeds/temperature", msg=str(msg1))
    # time.sleep(1)
    # client.publish(topic="Angelaaa/feeds/pressure", msg=str(msg2))
    # time.sleep(1)

def settimeout(duration):
    pass

wlan = WLAN(mode=WLAN.STA)
wlan.connect("Angela", auth=(WLAN.WPA2, "k25ag2pn"), timeout=50000)

while not wlan.isconnected():
    machine.idle()
print("Connected to WiFi\n")

py = Pycoproc(Pycoproc.PYSENSE)
# if 'pybytes' in globals():
#     if(pybytes.isconnected()):
#         print('Pybytes is connected, sending signals to Pybytes')
#         pybytes_enabled = True

client = MQTTClient("temp", "io.adafruit.com",user="Angelaaa", password="aio_HQNl44AJsQZhX6KZD5lvmjQ83EAw", port=1883)
client.settimeout = settimeout
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic="Angelaaa/feeds/pressure")

while True :
    alt = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    press = MPL3115A2(py,mode=PRESSURE)
    li = LTR329ALS01(py)
    msg1 = int(alt.temperature())
    msg2 = press.pressure()
    # msg3 = int(li.light())
    #print("MPL3115A2 temperature: " + str(alt.temperature()))
    #print("Altitude: " + str(alt.altitude()))
    client.publish(topic="Angelaaa/feeds/pressure", msg=str(msg2))
    time.sleep(1)
    # press = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
    # print("Pressure: " + str(press.pressure()))
    #
    # dht = SI7006A20(py)
    # print("Temperature: " + str(dht.temperature())+ " deg C and Relative Humidity: " + str(dht.humidity()) + " %RH")
    # print("Dew point: "+ str(dht.dew_point()) + " deg C")
    # #change to your ambient temperature
    # t_ambient = 24.4
    # print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(dht.humid_ambient(t_ambient)) + "%RH")
    #
    # li = LTR329ALS01(py)
    # print("Light (channel Blue lux, channel Red lux): " + str(li.light()))
    #
    # acc = LIS2HH12(py)
    # print("Acceleration: " + str(acc.acceleration()))
    # print("Roll: " + str(acc.roll()))
    # print("Pitch: " + str(acc.pitch()))
    # print("Battery voltage: " + str(py.read_battery_voltage()))
    # if(pybytes_enabled = True):
    #     pybytes.send_signal(1, alt.temperature())
    #     print("Send data to pybytes")
