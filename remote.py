from telemetry_core import Process, Producer
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress

BAUD_RATE = 230400
# TODO: Check where we could call the xbee.close() method
#       if .open() takes little time one could open, send and then close
#       the device. Otherwise we need a place to call the .close() method
# TODO: XBee error handling
class RemoteSender():

    def __init__(self, port):
        # TODO: Save xbee
        xbee = XBeeDevice(port, BAUD_RATE)
        if xbee.is_open():
            xbee.close()
        # self.xbee.open(force_settings=True)
        xbee.open()

        remote = RemoteXBeeDevice(xbee, 
                    x64bit_addr=XBee64BitAddress(bytearray.fromhex('0013A20041AE8955')),
                    node_id='XBEE_B')
        
        self.xbee = xbee
        self.remote = remote

    def use_data(self, data):
        self.xbee.send_data_async(self.remote, data['raw_message'])
    
class RemoteReceiver():

    def __init__(self, port):
        xbee = XBeeDevice(port, BAUD_RATE)
        if xbee.is_open():
            xbee.close()
        xbee.open()
        xbee.flush_queues()

        remote = RemoteXBeeDevice(xbee, 
                x64bit_addr=XBee64BitAddress(bytearray.fromhex('13A20041AE890D')))

        self.xbee = xbee
        self.remote = remote



    def read_data(self) -> dict:
        self.remote.set_sync_ops_timeout(0)
        xbee_message = self.xbee.read_data_from(self.remote, 10)
        # print(read_data)
        # TODO: it will probably be a bottleneck
        if xbee_message is not None:
            return { "raw_message": xbee_message.data.decode() }
        else:
            return { "raw_message": "Not found data"}
