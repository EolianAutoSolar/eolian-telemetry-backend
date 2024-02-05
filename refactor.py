from multiprocessing import Process, Manager
from abc import ABC, abstractmethod

# TODO: make everything private

class Reader(ABC):

    # Data Store is the container of the read data
    def __init__(self) -> None:
        self.data_store = None

    # subscribe a data store to the reader
    def subscribe_data_store(self, ds : 'Data'):
        self.data_store = ds

    # Reading loop
    def read(self) -> None:
        while True:
            data = self.read_data()
            Process(target=self.data_store.update, args=(data, )).start()
            # TODO: maybe a condition or delay should go here
    
    # read_data should return a dictionary containing pairs {name : value}
    @abstractmethod
    def read_data(self) -> dict:
        "read_data should return a dictionary containing pairs {name : value}"

# Data holds the current state of all the data
class Data():
    def __init__(self) -> None:
        manager = Manager()
        self.data = manager.dict()
        self.services = []
    
    # subscribe service to the data store
    # TODO: add method to remove services
    def subscribe_service(self, s : 'Service'):
        self.services.append(s)
    
    # update keeps the data with the last read values and notifies all of it's services
    def update(self, data : dict) -> None:
        for name, value in data.items():
            self.data[name] = value
        for s in self.services:
            Process(target=s.use_data, args=(self.data, )).start()

# A service is designed to receive the data, use it for a single purpose and then discard it
    
# Services could also be just a function, but rather a Class is used to optimize any startup
# process that a service could need. For example initializing a database, keeping track of a file or
# running a server.
class Service(ABC):
    
    @abstractmethod
    def use_data(self, data : Data):
        "single data usage"

# This is the standard way to initialize the whole program

# # 1. Initialize all the services
# ss = Service()

# # 2. Initialize the Data Store and subscribe the services to it
# dc = Data([ss], [ps])

# # 3. Initialize all the Readers and subscribe the Data store to them
# r = Reader(dc)

# # 4. Start all of the Readers main loop
# for temp_r in [r]:
#     Process(target=temp_r.read).start()

# 5X. Run an infinite loop to not kill all of the spawned processes
# TODO: Find a way to do this using a reader (to save 1 thread)
    
# All of this program uses number_of_readers number of threads.
# Also temporary threads are spawned to handle the Data updates and service executions.
# Meaning that for each data received by a reader, number_of_services
# temporary processes are spawned.

# TODO: Make sure that all of the spawned processes finishs before a new spawn of the processes.
