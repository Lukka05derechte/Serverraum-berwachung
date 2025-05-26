#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "172.20.10.242"
PORT = 4223
UID = "Wcg"
UID2 = "R7M"
UID3 = "ML4"
UID4 = "22ND"
import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from tinkerforge.bricklet_nfc import BrickletNFC



if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    ptc = BrickletPTCV2(UID, ipcon) # Create device object
    ps = BrickletPiezoSpeakerV2(UID2, ipcon) # Create device object
    md = BrickletMotionDetectorV2(UID3, ipcon) # Create device object
    nfc = BrickletNFC(UID4, ipcon)
    ipcon.connect(HOST, PORT)
    # Don't use device before ipcon is connected

    # Setzte die Sensoren als Variable
    temperature = ptc.get_temperature()
    alarm = ps.set_alarm(700, 300, 10, 3, 7, 5000)
    led = md.set_indicator(255, 255, 255)
    
def cb_state_changed(state, idle):
    if state == BrickletNFC.STATE_REQUEST_TAG_ID_READY:
        tag_type, tag_id = nfc.get_tag_id()
        print(f"Tag erkannt. Typ: {tag_type}, ID: {tag_id.hex()}")
        
        # Optional: Daten lesen von z.B. Block 4 (bei MIFARE Classic 1K)
        try:
            result = nfc.mifare_classic_authenticate_block(tag_id, 4, BrickletNFC.KEY_A, [0xFF]*6)
            if result:
                data = nfc.mifare_classic_read_block(4)
                print("Block 4 Daten:", data)
            else:
                print("Authentifizierung fehlgeschlagen.")
        except Exception as e:
            print("Fehler beim Lesen:", e)

        # Wieder in Lese-Modus gehen
        nfc.request_tag_id()

    nfc.register_callback(nfc.CALLBACK_STATE_CHANGED, cb_state_changed)

    # In Reader-Modus wechseln
    nfc.set_mode(BrickletNFC.MODE_READER)
    time.sleep(0.5)

    # Nach Tag suchen
    print("Bitte NFC-Tag an das Bricklet halten...")
    nfc.request_tag_id()


    print("Beobachte Bewegung für 30 Sekunden...")
    start_time = time.time()
    detected = False

    while time.time() - start_time < 30:
        if md.get_motion_detected():
            print("Bewegung erkannt!")
            detected = True
            break  # Optional: abbrechen, sobald Bewegung erkannt wurde
        time.sleep(0.2)  # kleine Pause, damit die Schleife nicht zu schnell läuft
    if not detected:
        print("Keine Bewegung erkannt innerhalb von 30 Sekunden.")

    if detected:
        print("Bewegung Gespeichert")
        
        

    
    
    
    input("Press key to exit\n") # Use raw_input() in Python 2
    ipcon.disconnect()
