from database import Database
from can_reader import CanReader
from frontend import ConsoleVisualization
# from remote import RemoteReceiver


db = Database("mttest.txt")
front = ConsoleVisualization()
#receiver = RemoteReceiver("/dev/ttyUSB0")

if __name__ == "__main__":
    for i in range(1000):
        main_task(
            # recv=receiver.read_data, 
            recv=inpu(), 
            consumers=[db, front]
        )
