from refactor import Service, Reader, Data
from multiprocessing import Process

class Telemetry():

    def __init__(self, services : ['Service'], readers : ['Reader']) -> None:
        self.data_store = Data()
        for s in services:
            self.data_store.subscribe_service(s)
        self.readers = readers
        for r in self.readers:
            r.subscribe_data_store(self.data_store)
    
    def run(self):
        for i in range(len(self.readers) - 1):
            Process(target=self.readers[i].read).start()
        self.readers[len(self.readers) - 1].read()