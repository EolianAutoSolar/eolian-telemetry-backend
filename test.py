from multiprocessing import Process, Manager
import time
import random

class Reader():
    def __init__(self, data_store) -> None:
        self.data_store = data_store

    def read(self):
        while True:
            data = self.read_data()
            print("generated data ", data)
            Process(target=self.data_store.update, args=(data, )).start()
            time.sleep(1)
    
    def read_data(self):
        return {"read data": random.randint(0, 10)}

class Data():
    def __init__(self, services) -> None:
        m = Manager()
        self.d = m.dict()
        self.services = services
    
    def update(self, data):
        for name, value in data.items():
            self.d[name] = value
        for s in self.services:
            Process(target=s.update, args=(self.d, )).start()
        

class Service():
    def __init__(self) -> None:
        m = Manager()
        self.d = m.dict()
    
    def update(self, data):
        for name, value in data.items():
            self.d[name] = value
        print("updated data ", self.d)

s = Service()
dc = Data([s])
r = Reader(dc)
Process(target=r.read).start()

while True:
    print("Service data {}".format(s.d))
    time.sleep(0.3)

