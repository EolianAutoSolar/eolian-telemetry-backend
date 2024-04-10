from telemetry_core import Process
from digi.xbee.devices import XBeeDevice

BAUD_RATE = 230400
# TODO: Check where we could call the xbee.close() method
#       if .open() takes little time one could open, send and then close
#       the device. Otherwise we need a place to call the .close() method
# TODO: XBee error handling
class RemoteSender(Process):

    def __init__(self, port):
        # TODO: Save xbee
        self.xbee = XBeeDevice(port, BAUD_RATE)
        self.xbee.open()
        self.counter = 0
        self.val = 0
        self.data_buffer = ''

    def use_data(self, data):
        self.data_buffer += '|' + data['raw_message']
        self.counter += 1
        self.val +=1
        # TODO: This value is important, it should not be set as a magic number
        if self.counter == 6:            
            # print("Sent message {}".format(self.data_buffer))
            xbee_network = self.xbee.get_network()
            remote_device = xbee_network.discover_device("XBEE_B")
            self.xbee.send_data_async(remote_device, self.data_buffer)
            # self.xbee.close()
            self.counter = 0
            self.data_buffer = ''
    
class RemoteReceiver(Process):

    def __init__(self, port):
        self.xbee = XBeeDevice(port, BAUD_RATE)

    def read_data(self) -> dict:
        self.xbee.open()
        read_data = self.xbee.read_data()
        self.xbee.close()
        if read_data is not None:
            print("Read data {}".format(read_data.data.decode()))
        # pasar data a dict
        return { "message": read_data }