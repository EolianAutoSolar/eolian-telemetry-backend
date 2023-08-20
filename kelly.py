from typing import Any
from can import Bus, Listener, Notifier
from can.message import Message
import random

class Kelly(Listener):
    def __init__(self, bus: Bus):
        self.bus = bus

    def on_message_received(self, msg: Message) -> None:
        if msg.arbitration_id == 0x0c8 or msg.arbitration_id == 0x064:
            req_id = msg.data[0]
            ans = Message(arbitration_id=(0x0cd if msg.arbitration_id == 0x0c8 else 0x069), data=[0xee, 0,0,0,0,0,0,0], is_extended_id=False)
            if req_id == 0x1b:
                ans.data = [0x23, 0x01, 0x02, 0x03, 0x04]
                ans.dlc = 5
            elif req_id == 0x1a:
                ans.data = [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255)]
                ans.dlc = 6
            elif req_id == 0x33:
                ans.data = [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255)]
                ans.dlc = 6
            elif req_id == 0x37:
                ans.data = [0x00, 0x01, 0x02, 0x03, 0x04]
                ans.dlc = 5
            elif req_id == 0x42:
                ans.data = [0x00]
                ans.dlc = 1
            elif req_id == 0x43:
                ans.data = [0x00]
                ans.dlc = 1
            elif req_id == 0x44:
                ans.data = [0x00]
                ans.dlc = 1
            self.bus.send(ans)


vcan0 = Bus(interface='socketcan', channel='vcan0')
notify = Notifier(vcan0, [Kelly(vcan0)])

while True:
    pass
