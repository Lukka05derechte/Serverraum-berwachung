#!/usr/bin/env python
# -*- coding: utf-8 -*-

import keyboard
import time
import threading

# ===== KONFIGURATION =====
HOST = "172.20.10.242"
PORT = 4223
UID = "Wcg"  # Deine PTC Bricklet UID
UID2 = "R7M"  # Deine Piezo Speaker UID

TEMPERATUR_GRENZE_C = 25.0  # Temperaturgrenze in °C

# ==========================

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2

def main():
    ipcon = IPConnection()
    ptc = BrickletPTCV2(UID, ipcon)
    ps = BrickletPiezoSpeakerV2(UID2, ipcon)

    ipcon.connect(HOST, PORT)

    alarm_aktiv = False
    stop_event = threading.Event()
    grenzwert = TEMPERATUR_GRENZE_C * 100  # Umrechnung in 1/100 °C für Bricklet

    # Event-Handler für Enter-Taste
    def on_enter(event):
        stop_event.set()

    keyboard.on_press_key("enter", on_enter)

    try:
        while not stop_event.is_set():
            temperature = ptc.get_temperature()
            temp_celsius = temperature / 100.0

            print(f"Temperatur: {temp_celsius:.2f} °C")

            if temperature > grenzwert and not alarm_aktiv:
                print(f"Temperatur über {TEMPERATUR_GRENZE_C}°C - Alarm AN")
                ps.set_alarm(800, 2000, 10, 1, 1, 10000)
                alarm_aktiv = True
            elif temperature <= grenzwert and alarm_aktiv:
                print(f"Temperatur unter {TEMPERATUR_GRENZE_C}°C - Alarm AUS")
                ps.set_alarm(0, 0, 0, 0, 0, 0)
                alarm_aktiv = False

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Mit Strg+C abgebrochen.")

    finally:
        ps.set_alarm(0, 0, 0, 0, 0, 0)  # Alarm sicher ausschalten
        ipcon.disconnect()
        keyboard.unhook_all()
        input("Taste drücken zum Beenden...")

if __name__ == "__main__":
    main()
