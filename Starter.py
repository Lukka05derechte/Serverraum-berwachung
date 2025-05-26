#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "172.20.10.242"
PORT = 4223
UID = "Wcg"
UID2 = "R7M"
UID3 = "ML4"
UID4 = "22ND"

import Bewegung as bew
import heatsens as hs
import nfc as mako
from tinkerforge.ip_connection import IPConnection

Bewegungsmelder = bew.bw.movedetect()
Wearmesensor = hs.ptcsensor.get_temp()
#Get_NFC_Tag = mako.nfcV2.nfc_reading()

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    #ptc = BrickletPTCV2(UID, ipcon) # Create device object
    #ps = BrickletPiezoSpeakerV2(UID2, ipcon) # Create device object
    #nfc = BrickletNFC(UID4, ipcon)
    #ipcon.connect(HOST, PORT)
    # Don't use device before ipcon is connected

    # Setzte die Sensoren als Variable
    #temperature = ptc.get_temperature()
    #alarm = ps.set_alarm(700, 300, 10, 3, 7, 5000)


print(Bewegungsmelder)
#or i in range (1,30,1):
   #print(Bewegungsmelder)
   #print(Wearmesensor)