from refactor import Reader
import can

class CanReader(Reader):

    # If using a virtual interface bitrate is None, if using a real interface specify the bitrate
    def __init__(self, data_store, channel, bitrate=None) -> None:
        super().__init__(data_store)
        self.bus = can.Bus(interface='socketcan', channel=channel, bitrate=bitrate)

    def read_data(self) -> dict:
        message = self.bus.recv()
        return self.parse_can_message(message)
    
    # receives and process a can message and returns it as data dict {name: value}
    def parse_can_message(self, message) -> dict:
        return { "PLACEHOLDER": 100 }