
from network import LoRa
import socket
import struct
import machine
import pycom
import time
from pycoproc_1 import Pycoproc
import sys
from mqtt import MQTTClient
from network import WLAN
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,PRESSURE


ADAFRUIT_IO_USERNAME = "LION_224"
ADAFRUIT_IO_KEY = "aio_slYU78il4pEyaicrkRBtyPV1UW51"

FEED_ID = 'data_collections'

wlan = WLAN(mode=WLAN.STA)
wlan.connect("AndroidAP2ef5", auth=(WLAN.WPA2, "elaz224gaoual"), timeout=5000)

while not wlan.isconnected():
    machine.idle()
print("Connected to WiFi\n")
py = Pycoproc(Pycoproc.PYSENSE)
_LORA_PKG_FORMAT = "!BB%ds"
_LORA_PKG_ACK_FORMAT = "BBB"

DEVICE_ID = 0x01
pycom.heartbeat(False)

lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.EU868)
sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
sock.setblocking(False)

dht = SI7006A20(py)
lt = LTR329ALS01(py)

def connected(client):
    print('Connected to Adafruit IO! listening for {0} changes...'.format(FEED_ID))
    client.subscribe(FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    print('Subscribe to {0} with QoS {1}'.format(FEED_ID, granted_qos[0]))

def disconnected(client):
    print("Disconnected from Adafruit_IO")

    sys.exit(1)

def publish(client):
    data = get_data_from_sensors()
    print('Publishing {0} to {1} feed'.format(data, FEED_ID))
    client.publish(FEED_ID, data)

def message(client, fedd_id, payload):

    print("Feed {0} received new data: {1}".format(FEED_ID, payload))

def get_data_from_sensors()->str:
    """
    Collect the data from the sensors, especialy the temperature, humidity and light
    return a string containing these 3 infos.
    """
    temp = str(round(dht.temperature(), 2))
    humidity = str(round(dht.humidity(), 2))
    light = str(round(lt.lux(), 2))

    return "data :"+temp+" "+humidity+" "+light


def sending_data():
    """
    Send the data via LoRa
    """
    waiting_ack = True
    msg = get_data_from_sensors()
    pkg = struct.pack(_LORA_PKG_FORMAT%len(msg), DEVICE_ID, len(msg), msg)
    sock.send(pkg)
    recv_ack = sock.recv(256)
    if len(recv_ack) > 0:
        device_id, pkg_len, ack = struct.unpack(_LORA_PKG_FORMAT%recv_pkg_len, recv_pkg)
        if device_id == DEVICE_ID:
            if ack == 200:
                waiting_ack = False
                print("ACK")
            else:
                waiting_ack = False
                print("Message Failed")
    return waiting_ack

#client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client = MQTTClient("device_id", "io.adafruit.com",user=ADAFRUIT_IO_USERNAME, password=ADAFRUIT_IO_KEY, port=1883)
client.set_callback(subscribe)
data = get_data_from_sensors()
print('Publishing {0} to {1} feed'.format(data, FEED_ID))
client.publish(topic="LION_224/Feeds/data_collections", msg=data)

sending_data()
