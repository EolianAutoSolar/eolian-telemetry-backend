from can_reader import CanReader
from telemetry import Telemetry
from telemetry_core import Consumer
from database import Database
from frontend import ConsoleVisualization
from remote import RemoteSender

# 
canbus = CanReader('vcan0')

xbee = RemoteSender('/dev/ttyUSB0')
db = Database('otp.txt')
front = ConsoleVisualization()
mc = Consumer([front, db, xbee])

Telemetry(canbus, mc).run()
