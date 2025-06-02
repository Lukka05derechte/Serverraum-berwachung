#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "172.20.10.242"
PORT = 4223
UID = "Wcg"
UID2 = "R7M"
UID3 = "ML4"
UID4 = "22ND"
UID5 = "R7M"  
UID6 = "Tre"  
UID7 = "ViW"

import time
import threading
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from tinkerforge.bricklet_nfc import BrickletNFC
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2
from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2 
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2


#__Tag to string_#
def tag_id_to_string(tag_id):
    return ' '.join(f'{b:02X}' for b in tag_id)


#__Ipconnection zu Bricklets__#
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    ptc = BrickletPTCV2(UID, ipcon)
    md = BrickletMotionDetectorV2(UID3, ipcon) # Create device object
    nfc = BrickletNFC(UID4, ipcon)
    ps = BrickletPiezoSpeakerV2(UID5, ipcon)
    sd = BrickletSegmentDisplay4x7V2(UID6, ipcon) # Create device object
    h = BrickletHumidityV2(UID7, ipcon)
    ipcon.connect(HOST, PORT)


#__Vordefenierte Varis__#    
TEMPERATUR_GRENZE_C = 30
temperature1 = ptc.get_temperature()

grenzwert = TEMPERATUR_GRENZE_C * 100  # Umrechnung in 1/100 °C für Bricklet



#__Programmstart aka Programm ans sich__#
def movedetect():
        alarm_aktiv = False
        sd.set_brightness(7) 
        print("Beobachte Bewegung für 60 Sekunden...")
        start_time = time.time()
        detected = False

        while time.time() - start_time < 60:
            if md.get_motion_detected():
                detected = True
                break  # Bewegung erkannt, Schleife abbrechen
            time.sleep(0.2)  # kleine Pause für CPU-Entlastung

        if detected:
            print("Bewegung erkannt")

            nfc.set_mode(BrickletNFC.MODE_READER)
            time.sleep(0.5)
            nfc.reader_request_tag_id()

            time.sleep(1)  

            try:
                nfc.set_mode(BrickletNFC.MODE_READER)
                time.sleep(0.5)
                nfc.reader_request_tag_id()
                time.sleep(1)

                tag_type, tag_id = nfc.reader_get_tag_id()
                #print(tag_id)
            except:
                print("Kein Tag erkannt.")
            else:
                if tag_id == (4, 59, 86, 66, 185, 17, 145):#weiß G5
                    print("Tag erkannt! UID:", tag_id_to_string(tag_id))
                    print(f"🌡️ Temperatur: {temperature1 / 100} °C")
                    humidity = h.get_humidity()
                    print("Humidity: " + str(humidity/100.0) + " %RH")
                    while time.time() - start_time < 60:
                        temperature = ptc.get_temperature()
                        temp_celsius = temperature / 100.0

                        #print(f"Temperatur: {temp_celsius:.2f} °C")

                        array = [int(d) for d in f"{temp_celsius:.2f}" if d.isdigit()]
                        sd.set_numeric_value(array)

                        if temperature > grenzwert and not alarm_aktiv:
                            print(f"Temperatur über {TEMPERATUR_GRENZE_C}°C - Alarm AN")
                            ps.set_alarm(800, 2000, 10, 1, 1, 10000)
                            alarm_aktiv = True
                        elif temperature <= grenzwert and alarm_aktiv:
                            print(f"Temperatur unter {TEMPERATUR_GRENZE_C}°C - Alarm AUS")
                            ps.set_alarm(0, 0, 0, 0, 0, 0)
                            alarm_aktiv = False

                        time.sleep(0.5)
                else:
                    print("falsches Tag")


#__Input zum Start__#
if input("Programm Starten? J/N") == "J":
    movedetect()
else:
    print("Programm wurde nicht gestartet")
