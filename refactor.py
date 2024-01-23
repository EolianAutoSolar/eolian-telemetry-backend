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
    def __init__(self, single_services, permanent_services) -> None:
        m = Manager()
        self.data = m.dict()
        self.single_services = single_services
        self.permanent_services = permanent_services
    
    def update(self, data):
        for name, value in data.items():
            self.data[name] = value
        for ps in self.permanent_services:
            Process(target=ps.update, args=(self.data, )).start()
        for ss in self.single_services:
            Process(target=ss.use_data, args=(self.data, )).start()
        

class PermanentService():
    def __init__(self) -> None:
        m = Manager()
        self.state = m.dict()
    
    def update(self, data):
        for name, value in data.items():
            self.state[name] = value
        print("updated data ", self.state)

    def main(self):
        while True:
            print("Service data {}".format(self.state))
            time.sleep(0.3)


class SingleService():
    def __init__(self) -> None:
        pass
    
    def use_data(self, data):
        print("Used data for single service ", data)


ss = SingleService()
ps = PermanentService()
dc = Data([ss], [ps])
r = Reader(dc)

for temp_ps in [ps]:
    Process(target=temp_ps.main).start()


r.read()


