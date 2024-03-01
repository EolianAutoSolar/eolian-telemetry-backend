from telemetry_core import Service, Reader
# TODO: pip install digi-xbee

class RemoteSender(Service):

    def __init__(self):
        # TODO: Save xbee
        self.xbee = 0

    def use_data(self, data):
        self.send(data)
    
    def send(self, data):
        print("Sent message {}".format(data))
        self.xbee.send(data)

class RemoteReceiver(Reader):

    def __init__(self):
        # TODO: Save xbee
        self.xbee = 0

    def read_data(self) -> dict:
        read_data = self.xbee.recv()
        # pasar data a dict
        return read_data