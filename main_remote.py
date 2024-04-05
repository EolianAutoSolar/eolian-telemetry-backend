from frontend import ConsoleVisualization
from remote import RemoteReceiver
from telemetry import Telemetry
from database import Database
from telemetry_core import Consumer

# 
tui = ConsoleVisualization()
db = Database('recv.txt')
#
recv = RemoteReceiver("COM3")
mc = Consumer([tui, db])

Telemetry().run()