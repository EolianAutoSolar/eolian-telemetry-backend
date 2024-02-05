from telemetry_core import Data
from multiprocessing import Process

# Working implementation of a whole program execution using telemetry_core architechture
class Telemetry():

    def __init__(self, services : ['Service'], readers : ['Reader']) -> None:
        self.data_store = Data()
        for s in services:
            self.data_store.subscribe_service(s)
        self.readers = readers
        for r in self.readers:
            self.data_store.subscribe_to_reader(r)
    
    def run(self):
        for i in range(len(self.readers) - 1):
            Process(target=self.readers[i].read).start()
        self.readers[len(self.readers) - 1].read()