from multiprocessing import Process, Queue
from abc import ABC, abstractmethod
import datetime

# TODO: make everything private

# Producer connects to a data interface, receives a package and stores it in the queue.
class Producer(ABC):

    def __init__(self) -> None:
        self.queue = None

    # Execution loop
    def run(self, queue : Queue) -> None:
        while True:
            data = self.read_data()
            # print("Produced data {} at {} {}".format(data, datetime.datetime.now(), queue.put(data)))
            queue.put(data)
            # TODO: maybe a condition or delay should go here
    
    # read_data should return a dictionary containing pairs {name : value}
    @abstractmethod
    def read_data(self) -> dict:
        "read_data should return a dictionary containing pairs {name : value}"

# A process is designed to receive the data, use it for a single purpose and then discard it
# Processs could also be just a function, but rather a Class is used to optimize any startup
# process that a process could need. For example initializing a database, keeping track of a file or
# running a server.
class Process(ABC):
    
    @abstractmethod
    def use_data(self, data):
        "single data usage"

# A Consumer waits for an item in the queue and execute all of it's processes on the item.
class Consumer():

    def __init__(self, processes) -> None:
        print("Init consumer")
        self.processes = processes

    # Execution loop
    def run(self, queue : Queue):
        print("started processes")
        while True:
            data = queue.get()
            for process in self.processes:
                # print(process)
                process.use_data(data)

# To create a program following this structures:
#   1. Set up the various producers
#   2. Set up the Consumer with the producers from 1.
#   3. Set un the Producer
#   4. Call Telemetry with 3. and 2.

# You can find an example in telemetry.py