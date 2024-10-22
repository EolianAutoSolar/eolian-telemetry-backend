from database import Database
from can_reader import CanReader
from frontend import ConsoleVisualization
# from remote import RemoteReceiver
from telemetry import main_task

db = Database("mttest.txt")
front = ConsoleVisualization()
#receiver = RemoteReceiver("/dev/ttyUSB0")

if __name__ == "__main__":
    while True:
    # for i in range(1000):
        main_task(
            # recv=receiver.read_data, 
            recv=input(), 
            consumers=[db, front]
        )
