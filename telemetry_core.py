from multiprocessing import Process, Manager
from abc import ABC, abstractmethod

# TODO: make everything private

# Data (or data_store) holds the current state of all the data, updating it's state
# when receiving a notification from any Reader that it is subscribed to and sending a
# "data was updated" notification to every Service that subscribed to this Data.
class Data():

    def __init__(self) -> None:
        manager = Manager()
        self.data = manager.dict()
        self.services = []
    
    # subscribe service to the data store
    # TODO: add method to remove services
    def subscribe_service(self, s : 'Service'):
        self.services.append(s)
    
    # subscribe to a reader
    def subscribe_to_reader(self, r : 'Reader'):
        r.subscribe_data_store(self)
    
    # update keeps the data with the last read values and notifies all of it's services
    def update(self, data : dict) -> None:
        for name, value in data.items():
            self.data[name] = value
        for s in self.services:
            Process(target=s.use_data, args=(self.data, )).start()

# Reader connects to a data interface, receives a package, then process it and finally sends
# the "data updated" notification to it's subscribed Data. It is designed to poll data forever from it's interface.
class Reader(ABC):

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

# A service is designed to receive the data, use it for a single purpose and then discard it
# Services could also be just a function, but rather a Class is used to optimize any startup
# process that a service could need. For example initializing a database, keeping track of a file or
# running a server.
class Service(ABC):
    
    @abstractmethod
    def use_data(self, data : Data):
        "single data usage"

# This is the standard way to initialize the whole program

# # 1. Create the Data
# data_store = Data()

# # 2. Subscribe all of the services to the Data
# for s in services:
#    data_store.subscribe_service(s)

# # 3. Initialize all the Readers and subscribe the Data store to them
# for r in readers:
#    data_store.subscribe_to_reader(r)

# # 4. Start all of the Readers main loop
# for r in readers:
#     Process(target=r.read).start()
# Note: Remember to always have a running loop as the main process to not kill
#       to all of the spawned processes.
    
# All of this program uses number_of_readers number of threads.
# Also temporary threads are spawned to handle the Data updates and service executions.
# Meaning that for each data received by a reader, 1 + number_of_services
# temporary processes are spawned.

# TODO: Make sure that all of the spawned processes finishs before a new spawn of the processes.