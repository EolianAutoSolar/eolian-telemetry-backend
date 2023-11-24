#!/usr/bin/env python
# std modules
import threading

# third party module
import can

# local modules
from front import FrontEnd, Frontend, frontData 
from database import Database
from kelly import request_kelly

# envs
PRE_SIMU = 1
SIMU = 2
EOLIAN = 3

# init can networks
vcankellys = can.Bus(interface='socketcan', channel='can0', can_filters=[
    {"can_id": 0x069, "can_mask": 0xfff}, # response kelly1
    {"can_id": 0x0cd, "can_mask": 0xfff}, # response kelly2
])

# can_id=0b000 00000000:can_mask=0b111 00000000
# can_id=0b001 00000000:can_mask=0b111 00000000

# 


# configs
ENV = PRE_SIMU

# init
# can network
can0 = can.Bus(interface='socketcan', channel='can0') if ENV == PRE_SIMU \
    else can.Bus(interface='socketcan', channel='can0')
can1 = can.Bus(interface='socketcan', channel='can1') if ENV == PRE_SIMU \
    else can.Bus(interface='socketcan', channel='can1')
    # falta agregar los baudrates para ENV != PRE_SIMU

# frontend
frontEnd = FrontEnd()
# init end

# CanNotifiers
can.Notifier([can0], [Frontend(frontEnd), Database('vcan0.csv')])
can.Notifier([can1], [Frontend(frontEnd), Database('vcan1.csv')])

# def request_kelly_daemon():
#     while True:
#         request_kelly(vcankellys)


if __name__ == "__main__":
    # Threading the request_kelly function
    print("starting")
    # t1 = threading.Thread(target=request_kelly_daemon)
    # t1.start()

    # save messages

    # process messages

    # running the frontend given messages
    frontEnd.run()
