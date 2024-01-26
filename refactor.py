from multiprocessing import Process, Manager
import time
import random

class Reader():

    # Data Store is the container of the read data
    def __init__(self, data_store) -> None:
        self.data_store = data_store

    # Reading loop
    def read(self) -> None:
        while True:
            data = self.read_data()
            Process(target=self.data_store.update, args=(data, )).start()
            # TODO: maybe a condition or delay should go here
    
    # read_data should return a dictionary containing pairs {name : value}
    @abstractmethod
    def read_data(self) -> dict:
        pass

# Data holds the current state of all the data
class Data():
    def __init__(self, single_services, permanent_services) -> None:
        manager = Manager()
        self.data = manager.dict()
        self.single_services = single_services
        self.permanent_services = permanent_services
    
    # update keeps the data with the last read values and notifies all of it's services
    def update(self, data) -> None:
        for name, value in data.items():
            self.data[name] = value
        for ps in self.permanent_services:
            Process(target=ps.update, args=(self.data, )).start()
        for ss in self.single_services:
            Process(target=ss.use_data, args=(self.data, )).start()
        
# A permanent service is designed to be always running, one example of a permanent service
# could be the visualization of the data. 
class PermanentService():
    def __init__(self) -> None:
        manager = Manager()
        # The state is the data needed to run the service, this could be a fraction of all the
        # data used in the program
        self.state = manager.dict()
    
    # updates the current state of the service
    def update(self, data) -> None:
        for name, value in data.items():
            self.state[name] = value

    # the main loop to be executed
    @abstractmethod
    def main(self):
        pass

# A single service is designed to receive the data and use it for a single purpose,
# the difference with a PS is that a SS doesn't hold a state regarding it's data usage.
# It just uses the data and then discards it.
    
# Single services could also be just a function, but rather a Class is used to optimize any startup
# process that a service could need. For example initializing a database, keeping track of a file or
# running a server.
class SingleService():
    
    @abstractmethod
    def use_data(self, data):
        pass

# This is the standard way to initialize the whole program

# 1. Initialize all the services
ss = SingleService()
ps = PermanentService()

# 2. Initialize the Data Store and subscribe the services to it
dc = Data([ss], [ps])

# 3. Initialize all the Readers and subscribe the Data store to them
r = Reader(dc)

# 4. Start all of the Permanent services main loop
for temp_ps in [ps]:
    Process(target=temp_ps.main).start()

# 5. Start all of the Readers main loop
for temp_r in [r]:
    Process(target=temp_r.read).start()

# 6X. Run an infinite loop to not kill all of the spawned processes
# TODO: Find a way to do this using either a reader or a pservice main loop (to save 1 thread)
    
# All of this program uses 1 + number_of_readers + number_of_permanent_services number of threads.
# Also temporary threads are spawned to handle the Data updates and single service executions.
# Meaning that for each data received by a reader, 1 + number_of_permanent_services + number_of_single_services
# temporary processes are spawned.

# TODO: Make sure that all of the spawned processes finishs before a new spawn of the processes.


