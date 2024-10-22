from database import Database
from can_reader import CanReader
from frontend import ConsoleVisualization
# from remote import RemoteSender
from telemetry import main_task

db = Database("mttest.txt")
front = ConsoleVisualization()
canreader = CanReader("vcan0")
# sender = RemoteSender("COM5")

if __name__ == '__main__':
    while True:
    # for i in range(1000):
        main_task(
            recv=canreader.read_data, 
            consumers=[db, front]
        )
