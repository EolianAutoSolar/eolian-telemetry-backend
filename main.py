#!/usr/bin/env python

import time
import can
from can.message import Message

# TODO: implement this function
def parse_message(msg: can.Message):
    id = msg.arbitration_id
    data = msg.data
    parsed_message = {}
    if id == 0x001:
        parsed_message = {

        }
    elif id == 0xc3:
        parsed_message = {
            
        }
    return parsed_message

locked = False

class Database(can.Listener):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        f = open(file=self.file_name, mode='w')
        f.write("timestamp,msg_id,data\n")
        f.close()

    def on_message_received(self, msg: can.Message) -> None:
        global locked
        while locked:
            time.sleep(0.2)
        locked = True
        f = open(file=self.file_name, mode='a')
        f.write("{},{},{}\n".format(msg.timestamp, msg.arbitration_id, msg.data.hex()))
        f.close()
        locked = False
        
    
class Frontend(can.Listener):
    def on_message_received(self, msg: can.Message) -> None:
        print(msg)

def request_kelly(bus):
    commands = [0x1b, 0x1a, 0x33, 0x37, 0x42, 0x43, 0x44]
    for c in commands:
        bus.send_periodic(
            Message(
            arbitration_id=0xc8, data=[c], is_extended_id=False
            ), 1
        )
        bus.send_periodic(
            Message(
            arbitration_id=0x64, data=[c], is_extended_id=False
            ), 1
        )
    # TODO: add condition to stop

vcan0 = can.Bus(interface='socketcan', channel='vcan0', can_filters=[
    {"can_id": 0x064, "can_mask": 0xfff},
    {"can_id": 0x069, "can_mask": 0xfff}
])
vcan1 = can.Bus(interface='socketcan', channel='vcan1')

can.Notifier([vcan0], [Frontend(), Database('vcan0.csv')])
can.Notifier([vcan1], [Frontend(), Database('vcan1.csv')])

def main():
    request_kelly(vcan0)
    while True:
        pass

if __name__ == "__main__":
    main()