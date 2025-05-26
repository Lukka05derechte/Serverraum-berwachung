import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2

HOST = "172.20.10.242"
PORT = 4223
UID = "Wcg"

ipcon = IPConnection() # Create IP connection
ptc = BrickletPTCV2(UID, ipcon) # Create device object
ipcon.connect(HOST, PORT)


class ptcsensor():

    def get_temp():
        temperature = ptc.get_temperature()
        print(temperature)

