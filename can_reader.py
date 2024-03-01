from telemetry_core import Reader
import can
import random

class CanReader(Reader):

    # If using a virtual interface bitrate is None, if using a real interface specify the bitrate
    def __init__(self, channel, bitrate=None) -> None:
        super().__init__()
        self.bus = can.Bus(interface='socketcan', channel=channel, bitrate=bitrate)

    def read_data(self) -> dict:
        message = self.bus.recv()
        return self.parse_can_message(message)
    
    # TODO: Add orion and kelly process formulas
    # receives and process a can message and returns it as data dict {name: value}
    def parse_can_message(self, message) -> dict:
        # parse message
        return { "kelly_izq_rpm": random.randint(5, 10),
                 "kelly_izq_temp": random.randint(0, 20), 
                 "kelly_izq_vel": random.randint(0, 20), 
                 "kelly_der_rpm": random.randint(0, 20), 
                 "kelly_der_temp": random.randint(0, 20), 
                 "kelly_der_vel": random.randint(0, 20), 
                 "bms_soc": random.randint(0, 20), 
                 "bms_volt": random.randint(0, 20), 
                 "bms_curr": random.randint(0, 20), 
                 "bms_temp": random.randint(0, 20),
                 "raw_message": "TIMESTAMP#ID#DATA" 
                 }