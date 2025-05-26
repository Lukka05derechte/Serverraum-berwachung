import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2

HOST = "172.20.10.242"
PORT = 4223
UID3 = "ML4"

ipcon = IPConnection() # Create IP connection
md = BrickletMotionDetectorV2(UID3, ipcon) # Create device object
ipcon.connect(HOST, PORT)

class bw():
    def movedetect():
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
        else:
            print("Keine Bewegung erkannt innerhalb von 60 Sekunden.")