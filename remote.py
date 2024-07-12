from telemetry_core import Process, Producer
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress

BAUD_RATE = 230400
# TODO: Check where we could call the xbee.close() method
#       if .open() takes little time one could open, send and then close
#       the device. Otherwise we need a place to call the .close() method
# TODO: XBee error handling
class RemoteSender(Process):

    def __init__(self, port):
        # TODO: Save xbee
        self.xbee = XBeeDevice(port, BAUD_RATE)
        # self.xbee.open(force_settings=True)
        self.xbee.open()

        self.remote = RemoteXBeeDevice(self.xbee, 
                    x64bit_addr=XBee64BitAddress(bytearray.fromhex('0013A20041AE8955')),
                    node_id='XBEE_B')
        self.counter = 0
        self.val = 0
        self.data_buffer = ''

    def use_data(self, data):
        self.data_buffer += '|' + data['raw_message']
        self.counter += 1
        self.val +=1
        self.xbee.send_data_async(self.remote, data['raw_message'])
        # # TODO: This value is important, it should not be set as a magic number
        # if self.counter == 6:
        #     try:
        #         self.xbee.send_data_async(self.remote, self.data_buffer)

        #         print("Success")

        #     except Exception as e:
        #         print("Exception: %s" % e)

        #     finally:
        #         self.counter = 0
        #         self.data_buffer = ''
    
class RemoteReceiver(Producer):

    def __init__(self, port):
        self.xbee = XBeeDevice(port, BAUD_RATE)
        if self.xbee.is_open():
            self.xbee.close()
        self.xbee.open()
        self.xbee.flush_queues()

    def read_data(self) -> dict:
        read_data = self.xbee.read_data()
        # print(read_data)
        # TODO: it will probably be a bottleneck
        while read_data is None:
            read_data = self.xbee.read_data()
        print(read_data.data.decode())
        return { "raw_message": read_data.data.decode() }
        # print("Read data {}".format(read_data))
        # # pasar data a dict
        # if read_data is None:
        #     return { "message": read_data, "raw_message": "#Null" }
        # else:
        #     return { "message": read_data, "raw_message": read_data.data.decode() }
                