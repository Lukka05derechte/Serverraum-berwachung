import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_nfc import BrickletNFC



HOST = "172.20.10.242"
PORT = 4223
UID4 = "22ND"

#ipcon = IPConnection() # Create IP connection
#nfc = BrickletNFC(UID4, ipcon)
#ipcon.connect(HOST, PORT)




def tag_id_to_string(tag_id):
    return ' '.join(f'{b:02X}' for b in tag_id)
ipcon = IPConnection()
nfc = BrickletNFC(UID4, ipcon)
ipcon.connect(HOST, PORT)

class nfcV2():
    def nfc_reading():


        nfc.set_mode(BrickletNFC.MODE_READER)
        time.sleep(0.5)
        nfc.reader_request_tag_id()

        time.sleep(1)  # kurze Pause für Tag-Erkennung

        try:
            tag_type, tag_id = nfc.reader_get_tag_id()
            print("Tag erkannt! UID:", tag_id_to_string(tag_id))
        except Exception:
            print("Kein Tag erkannt.")

        ipcon.disconnect()