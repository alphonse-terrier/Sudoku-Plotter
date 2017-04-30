#!/sr/bin/env python

import bluetooth
import time
import sys

bd_addr = "85:55:06:21:31:EE"
port = 1

print("connexion...")
try:
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
except:
    print("Erreur lors de la connexion !")

time.sleep(5)
try:
    sock.close()
except:
    passs

