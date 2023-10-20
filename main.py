#!/usr/bin/env python
# std modules
import threading

# third party module
import can

# local modules
from front import FrontEnd, Frontend, frontData 
from database import Database
from kelly import request_kelly

vcankellys = can.Bus(interface='socketcan', channel='can0', can_filters=[
    {"can_id": 0x069, "can_mask": 0xfff}, # response kelly1
    {"can_id": 0x0cd, "can_mask": 0xfff}, # response kelly2
])

vcan0 = can.Bus(interface='socketcan', channel='can0')
vcan1 = can.Bus(interface='socketcan', channel='can1')

# Front Object
frontEnd = FrontEnd()

# CanNotifiers
can.Notifier([vcan0], [Frontend(frontEnd), Database('vcan0.csv')])
can.Notifier([vcan1], [Frontend(frontEnd), Database('vcan1.csv')])

def request_kelly_daemon():
    while True:
        request_kelly(vcankellys)

if __name__ == "__main__":
    # Threading the request_kelly function
    print("starting")
    t1 = threading.Thread(target=request_kelly_daemon)
    t1.start()

    # Running the FrontEnd
    frontEnd.run()
