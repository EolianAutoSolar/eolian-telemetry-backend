from telemetry_core import Service, Reader
from digi.xbee.devices import XBeeDevice

BAUD_RATE = 9600

# TODO: Check where we could call the xbee.close() method
#       if .open() takes little time one could open, send and then close
#       the device. Otherwise we need a place to call the .close() method
# TODO: XBee error handling
class RemoteSender(Service):

    def __init__(self, port):
        # TODO: Save xbee
        self.xbee = XBeeDevice(port, BAUD_RATE)

    def use_data(self, data):
        self.xbee.open()
        print("Sent message {}".format(data))
        self.xbee.send_data_broadcast(data["raw_message"])
        self.xbee.close()
    
class RemoteReceiver(Reader):

    def __init__(self, port):
        self.xbee = XBeeDevice(port, BAUD_RATE)

    def read_data(self) -> dict:
        self.xbee.open()
        read_data = self.xbee.read_data()
        self.xbee.close()
        print("Read data {}".read_data)
        # pasar data a dict
        return { "message": read_data }